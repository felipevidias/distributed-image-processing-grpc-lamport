import argparse
from pathlib import Path

import grpc

import image_processing_pb2
import image_processing_pb2_grpc
from common.lamport_clock import LamportClock


def process_image(server: str, image_path: Path, output_path: Path, operation: str):
    clock = LamportClock("cliente")

    if not image_path.exists():
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    image_data = image_path.read_bytes()

    with grpc.insecure_channel(server) as channel:
        stub = image_processing_pb2_grpc.CoordinatorServiceStub(channel)

        send_time = clock.tick()
        clock.log(f"enviando imagem '{image_path.name}' ao coordenador")

        request = image_processing_pb2.ImageRequest(
            filename=image_path.name,
            image_data=image_data,
            operation=operation,
            lamport_time=send_time,
        )

        response = stub.ProcessImage(request, timeout=30)

    clock.update(response.lamport_time)
    clock.log("recebeu imagem final do coordenador")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.image_data)
    print(response.message)
    print(f"Imagem salva em: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default="localhost:50050")
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", default="results/saida.png")
    parser.add_argument(
        "--operation",
        default="grayscale",
        choices=["grayscale", "invert", "edges", "blur"],
    )
    args = parser.parse_args()

    process_image(
        server=args.server,
        image_path=Path(args.image),
        output_path=Path(args.output),
        operation=args.operation,
    )
