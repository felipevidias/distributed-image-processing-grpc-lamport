import argparse
from concurrent import futures

import grpc

import image_processing_pb2
import image_processing_pb2_grpc
from common.image_codec import png_bytes_to_image, image_to_png_bytes
from common.image_ops import apply_operation
from common.lamport_clock import LamportClock


class WorkerService(image_processing_pb2_grpc.WorkerServiceServicer):
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.clock = LamportClock(worker_id)

    def ProcessBlock(self, request, context):
        # Recebimento de mensagem: atualiza relógio lógico com timestamp recebido.
        self.clock.update(request.lamport_time)
        self.clock.log(
            f"recebeu bloco {request.block_id} "
            f"({request.width}x{request.height}) para operação '{request.operation}'"
        )

        try:
            block_image = png_bytes_to_image(request.image_data)
            processed = apply_operation(block_image, request.operation)
            processed_bytes = image_to_png_bytes(processed)
        except Exception as exc:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(exc))
            return image_processing_pb2.BlockReply()

        # Envio de resposta: incrementa relógio lógico.
        send_time = self.clock.tick()
        self.clock.log(f"enviou bloco {request.block_id} processado")

        return image_processing_pb2.BlockReply(
            block_id=request.block_id,
            width=processed.width,
            height=processed.height,
            image_data=processed_bytes,
            worker_id=self.worker_id,
            lamport_time=send_time,
        )


def serve(port: int, worker_id: str):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    image_processing_pb2_grpc.add_WorkerServiceServicer_to_server(
        WorkerService(worker_id), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Worker '{worker_id}' escutando na porta {port}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    serve(args.port, args.id)
