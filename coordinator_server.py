import argparse
from concurrent import futures
from typing import List, Tuple

import grpc
from PIL import Image

import image_processing_pb2
import image_processing_pb2_grpc
from common.image_codec import png_bytes_to_image, image_to_png_bytes
from common.image_ops import apply_operation
from common.lamport_clock import LamportClock


class CoordinatorService(image_processing_pb2_grpc.CoordinatorServiceServicer):
    def __init__(self, worker_addresses: List[str]):
        self.worker_addresses = worker_addresses
        self.clock = LamportClock("coordenador")

    def _split_image(self, image: Image.Image, parts: int) -> List[Tuple[int, Image.Image]]:
        """Divide a imagem em faixas horizontais."""
        width, height = image.size
        parts = max(1, min(parts, height))
        block_height = height // parts
        blocks = []

        for block_id in range(parts):
            y0 = block_id * block_height
            y1 = height if block_id == parts - 1 else (block_id + 1) * block_height
            block = image.crop((0, y0, width, y1))
            blocks.append((block_id, block))

        return blocks

    def _process_block_remote(self, block_id: int, block: Image.Image, operation: str, worker: str):
        """Envia um bloco para um worker usando gRPC."""
        send_time = self.clock.tick()
        self.clock.log(f"enviando bloco {block_id} para worker {worker}")

        with grpc.insecure_channel(worker) as channel:
            stub = image_processing_pb2_grpc.WorkerServiceStub(channel)
            request = image_processing_pb2.BlockRequest(
                block_id=block_id,
                width=block.width,
                height=block.height,
                image_data=image_to_png_bytes(block),
                operation=operation,
                lamport_time=send_time,
            )
            response = stub.ProcessBlock(request, timeout=10)

        self.clock.update(response.lamport_time)
        self.clock.log(
            f"recebeu bloco {response.block_id} processado por {response.worker_id}"
        )
        return response.block_id, png_bytes_to_image(response.image_data)

    def _process_block_local_fallback(self, block_id: int, block: Image.Image, operation: str):
        """Fallback simples caso um worker falhe.

        Isto não substitui o tratamento completo de falhas da Entrega 2,
        mas evita que a execução quebre por indisponibilidade de um worker.
        """
        self.clock.tick()
        self.clock.log(f"fallback local para bloco {block_id}")
        return block_id, apply_operation(block, operation)

    def ProcessImage(self, request, context):
        # Recebimento da imagem pelo cliente.
        self.clock.update(request.lamport_time)
        self.clock.log(
            f"recebeu imagem '{request.filename}' para operação '{request.operation}'"
        )

        try:
            image = png_bytes_to_image(request.image_data)
        except Exception as exc:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Erro ao abrir imagem: {exc}")
            return image_processing_pb2.ImageReply()

        if not self.worker_addresses:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details("Nenhum worker configurado.")
            return image_processing_pb2.ImageReply()

        blocks = self._split_image(image, len(self.worker_addresses))
        processed_blocks = []

        # Processamento paralelo: cada bloco é enviado a um worker.
        with futures.ThreadPoolExecutor(max_workers=len(self.worker_addresses)) as executor:
            future_to_block = {}
            for block_id, block in blocks:
                worker = self.worker_addresses[block_id % len(self.worker_addresses)]
                fut = executor.submit(
                    self._process_block_remote, block_id, block, request.operation, worker
                )
                future_to_block[fut] = (block_id, block)

            for fut in futures.as_completed(future_to_block):
                block_id, original_block = future_to_block[fut]
                try:
                    processed_blocks.append(fut.result())
                except grpc.RpcError as exc:
                    self.clock.log(
                        f"falha ao chamar worker no bloco {block_id}: {exc.code()}"
                    )
                    processed_blocks.append(
                        self._process_block_local_fallback(
                            block_id, original_block, request.operation
                        )
                    )
                except Exception as exc:
                    self.clock.log(f"erro no bloco {block_id}: {exc}")
                    processed_blocks.append(
                        self._process_block_local_fallback(
                            block_id, original_block, request.operation
                        )
                    )

        processed_blocks.sort(key=lambda item: item[0])
        final_width = image.width
        final_height = sum(block.height for _, block in processed_blocks)
        final_image = Image.new("RGB", (final_width, final_height))

        y = 0
        for _, block in processed_blocks:
            final_image.paste(block, (0, y))
            y += block.height

        send_time = self.clock.tick()
        self.clock.log("enviou imagem final ao cliente")

        return image_processing_pb2.ImageReply(
            message="Imagem processada com sucesso pelo sistema distribuído.",
            image_data=image_to_png_bytes(final_image),
            lamport_time=send_time,
        )


def serve(port: int, workers: List[str]):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    image_processing_pb2_grpc.add_CoordinatorServiceServicer_to_server(
        CoordinatorService(workers), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Coordenador escutando na porta {port}", flush=True)
    print(f"Workers configurados: {workers}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=50050)
    parser.add_argument(
        "--workers",
        type=str,
        default="localhost:50061,localhost:50062",
        help="Lista de workers separada por vírgula. Ex: localhost:50061,localhost:50062",
    )
    args = parser.parse_args()
    workers = [w.strip() for w in args.workers.split(",") if w.strip()]
    serve(args.port, workers)
