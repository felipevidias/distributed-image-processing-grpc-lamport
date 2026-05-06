# Entrega 1 - Sistema Distribuído de Processamento de Imagens

## Tema
Sistema distribuído de processamento de imagens usando gRPC e relógio lógico de Lamport.

## Requisitos da Entrega 1 atendidos

1. Uso de RPC com gRPC.
2. Implementação de relógio lógico de Lamport.

## Arquitetura

- Cliente: envia uma imagem ao coordenador.
- Coordenador: recebe a imagem, divide em blocos horizontais e envia blocos para workers.
- Workers: processam os blocos recebidos e devolvem ao coordenador.
- Coordenador: junta os blocos processados e devolve a imagem final ao cliente.

## Instalação

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Gerar os arquivos Python do gRPC

```bash
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/image_processing.proto
```

Esse comando gera:

- image_processing_pb2.py
- image_processing_pb2_grpc.py

## Criar imagem de teste

```bash
python tools/create_test_image.py
```

## Executar o sistema

Abra quatro terminais na pasta do projeto.

### Terminal 1 - Worker 1

```bash
source venv/bin/activate
python worker_server.py --port 50061 --id worker1
```

### Terminal 2 - Worker 2

```bash
source venv/bin/activate
python worker_server.py --port 50062 --id worker2
```

### Terminal 3 - Coordenador

```bash
source venv/bin/activate
python coordinator_server.py --port 50050 --workers localhost:50061,localhost:50062
```

### Terminal 4 - Cliente

```bash
source venv/bin/activate
python client.py --image images/entrada.png --operation grayscale --output results/saida_grayscale.png
```

Outras operações possíveis:

```bash
python client.py --image images/entrada.png --operation invert --output results/saida_invert.png
python client.py --image images/entrada.png --operation edges --output results/saida_edges.png
python client.py --image images/entrada.png --operation blur --output results/saida_blur.png
```

## Como observar o relógio lógico de Lamport

Cada processo imprime logs como:

```text
[Lamport=001] [cliente] enviando imagem 'entrada.png' ao coordenador
[Lamport=002] [coordenador] recebeu imagem 'entrada.png' para operação 'grayscale'
[Lamport=003] [coordenador] enviando bloco 0 para worker localhost:50061
[Lamport=004] [worker1] recebeu bloco 0
```

Esses logs mostram a ordem lógica dos eventos distribuídos.

## Observação sobre falhas

O coordenador possui um fallback simples: se um worker falhar, o bloco correspondente é processado localmente. Na Entrega 2, esse ponto pode ser expandido com redistribuição automática para outro worker, replicação, timeout mais detalhado e análise de desempenho.
