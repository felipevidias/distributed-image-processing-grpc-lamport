# Distributed Image Processing with gRPC and Lamport Clocks

A distributed image processing system built with **Python**, **gRPC**, **Protocol Buffers**, and **Lamport logical clocks**.

This project was developed as part of the first assignment for the **Distributed Computing** course. Its main purpose is to demonstrate how a computational task can be divided into smaller units, distributed across multiple nodes, processed in parallel, and coordinated through remote procedure calls.

---

## Table of Contents

- [Overview](#overview)
- [Main Features](#main-features)
- [Distributed Computing Concepts](#distributed-computing-concepts)
- [Distributed Computing Requirements](#distributed-computing-requirements)
- [System Architecture](#system-architecture)
- [Communication Flow](#communication-flow)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation on Windows](#installation-on-windows)
- [Generating gRPC Files](#generating-grpc-files)
- [Creating a Test Image](#creating-a-test-image)
- [Running the Distributed System](#running-the-distributed-system)
- [Available Image Operations](#available-image-operations)
- [Expected Outputs](#expected-outputs)
- [Example Execution](#example-execution)
- [Lamport Clock Logs](#lamport-clock-logs)
- [Preliminary Failure Test](#preliminary-failure-test)
- [Troubleshooting](#troubleshooting)
- [How to Stop the System](#how-to-stop-the-system)
- [Assignment Context](#assignment-context)
- [Evidence for the Report](#evidence-for-the-report)
- [Possible Future Improvements](#possible-future-improvements)
- [Authors](#authors)
- [License](#license)

---

## Overview

The system processes an image in a distributed way.

A **client** sends an image to a **coordinator server** using gRPC. The coordinator splits the image into horizontal blocks and distributes these blocks among available **worker nodes**. Each worker processes its assigned block independently and returns the processed block to the coordinator. Finally, the coordinator merges all processed blocks and sends the final image back to the client.

The system also implements **Lamport logical clocks** to record the logical order of distributed events, such as:

- client request submission;
- message sending;
- message receiving;
- block distribution;
- worker-side image processing;
- processed block return;
- final image reconstruction.

This makes the project useful for demonstrating basic distributed computing principles in a practical and visual way.

---

## Main Features

- Distributed image processing using a coordinator-worker architecture.
- Remote communication using gRPC.
- Service definition using Protocol Buffers.
- Multiple worker nodes processing image blocks.
- Lamport logical clock implementation.
- Console logs showing the logical order of distributed events.
- Support for multiple image processing operations.
- Simple preliminary test for worker unavailability.
- Windows-compatible execution instructions.

---

## Distributed Computing Concepts

This project demonstrates the following distributed computing concepts:

| Concept | How it appears in the project |
|---|---|
| Distributed system | The system is composed of separate processes: client, coordinator, and workers |
| RPC | The nodes communicate using gRPC remote procedure calls |
| Parallel task execution | The image is split into blocks and processed by different workers |
| Coordinator-worker architecture | The coordinator distributes tasks and merges the results |
| Message passing | Nodes exchange requests and responses through gRPC |
| Logical clocks | Lamport clocks are used to order distributed events |
| Fault awareness | A simple test can be performed by stopping one worker |

---

## Distributed Computing Requirements

This project implements two main requirements for the first assignment.

### 1. Remote Procedure Calls with gRPC

The communication between the client, coordinator, and workers is implemented using **gRPC**.

Main communication flow:

```text
Client -> Coordinator
Coordinator -> Worker 1
Coordinator -> Worker 2
Worker 1 -> Coordinator
Worker 2 -> Coordinator
Coordinator -> Client
```

The gRPC service is defined in:

```text
proto/image_processing.proto
```

From this `.proto` file, Python gRPC files are generated:

```text
image_processing_pb2.py
image_processing_pb2_grpc.py
```

These generated files are required for the Python programs to communicate using gRPC.

### 2. Lamport Logical Clocks

Each process maintains a Lamport logical clock.

The clock is updated when:

- a local event occurs;
- a message is sent;
- a message is received.

The Lamport clock does not measure real physical time. Instead, it provides a logical ordering of events across distributed processes.

Example:

```text
[Lamport=001] [client] Sending image to coordinator
[Lamport=002] [coordinator] Received image from client
[Lamport=003] [coordinator] Sending block 0 to worker localhost:50061
[Lamport=004] [worker1] Received block 0
```

---

## System Architecture

```text
+---------+
| Client  |
+---------+
     |
     | Sends image using gRPC
     v
+----------------+
|  Coordinator   |
+----------------+
     |        |
     |        |
     v        v
+----------+ +----------+
| Worker 1 | | Worker 2 |
+----------+ +----------+
     |        |
     |        |
     v        v
+----------------+
|  Coordinator   |
+----------------+
     |
     | Returns processed image
     v
+---------+
| Client  |
+---------+
```

### Components

| Component | Responsibility |
|---|---|
| Client | Sends the input image and receives the final processed image |
| Coordinator | Splits the image, sends blocks to workers, receives results, and rebuilds the final image |
| Worker 1 | Processes assigned image blocks |
| Worker 2 | Processes assigned image blocks |
| Protocol Buffers | Defines the message and service structure |
| Lamport Clock | Registers the logical order of distributed events |

---

## Communication Flow

The execution follows this sequence:

```text
1. The client loads an input image.
2. The client sends the image to the coordinator through gRPC.
3. The coordinator receives the image.
4. The coordinator splits the image into horizontal blocks.
5. The coordinator sends each block to an available worker.
6. Each worker processes its block.
7. Each worker returns the processed block to the coordinator.
8. The coordinator merges all processed blocks.
9. The coordinator sends the final processed image back to the client.
10. The client saves the output image in the results folder.
```

---

## Project Structure

```text
distributed-image-processing-grpc-lamport/
│
├── proto/
│   └── image_processing.proto
│
├── common/
│   ├── lamport_clock.py
│   ├── image_codec.py
│   └── image_ops.py
│
├── worker_server.py
├── coordinator_server.py
├── client.py
│
├── tools/
│   └── create_test_image.py
│
├── images/
│   └── entrada.png
│
├── results/
│
├── requirements.txt
├── .gitignore
└── README.md
```

### File Description

| File or Folder | Description |
|---|---|
| `proto/image_processing.proto` | Defines the gRPC services and messages |
| `common/lamport_clock.py` | Implements the Lamport logical clock |
| `common/image_codec.py` | Converts images to bytes and bytes to images |
| `common/image_ops.py` | Implements image processing operations |
| `worker_server.py` | Starts a worker server responsible for processing image blocks |
| `coordinator_server.py` | Starts the coordinator server responsible for task distribution |
| `client.py` | Sends an image processing request to the coordinator |
| `tools/create_test_image.py` | Creates a sample input image |
| `images/` | Stores input images |
| `results/` | Stores output images |
| `requirements.txt` | Lists Python dependencies |
| `.gitignore` | Prevents unnecessary files from being committed |

---

## Technologies Used

- Python
- gRPC
- Protocol Buffers
- Pillow
- Lamport logical clocks
- PowerShell / Windows terminal

---

## Requirements

Before running the project, make sure you have:

- Windows 10 or Windows 11;
- Python installed;
- Git installed, if you want to clone or push the project;
- Internet connection for installing Python dependencies.

Check Python:

```powershell
python --version
```

Check Git:

```powershell
git --version
```

---

## Installation on Windows

### 1. Open PowerShell

Open PowerShell and enter the project directory:

```powershell
cd "C:\Users\USER\PUC\2026-1_6P\COMP_DISTRIBUIDA\entrega1_sistema_distribuido"
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Allow script execution for the current PowerShell session

PowerShell may block virtual environment activation. To allow it only for the current session, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 4. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, the terminal should look like this:

```powershell
(venv) PS C:\Users\USER\PUC\2026-1_6P\COMP_DISTRIBUIDA\entrega1_sistema_distribuido>
```

### 5. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Generating gRPC Files

The gRPC Python files must be generated from the `.proto` file.

Run:

```powershell
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/image_processing.proto
```

Expected generated files:

```text
image_processing_pb2.py
image_processing_pb2_grpc.py
```

These files are automatically generated and are required by the client, coordinator, and workers.

---

## Creating a Test Image

To create a sample image for testing, run:

```powershell
python tools/create_test_image.py
```

Expected output in the terminal:

```text
Imagem de teste criada em: images\entrada.png
```

Expected file:

```text
images\entrada.png
```

---

## Running the Distributed System

The system must be executed in **four different PowerShell terminals**:

```text
Terminal 1: Worker 1
Terminal 2: Worker 2
Terminal 3: Coordinator
Terminal 4: Client
```

In each terminal, first enter the project folder and activate the virtual environment:

```powershell
cd "C:\Users\USER\PUC\2026-1_6P\COMP_DISTRIBUIDA\entrega1_sistema_distribuido"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

---

### Terminal 1 — Start Worker 1

```powershell
python worker_server.py --port 50061 --id worker1
```

Expected behavior:

```text
Worker worker1 running on port 50061
```

Keep this terminal open.

---

### Terminal 2 — Start Worker 2

```powershell
python worker_server.py --port 50062 --id worker2
```

Expected behavior:

```text
Worker worker2 running on port 50062
```

Keep this terminal open.

---

### Terminal 3 — Start Coordinator

```powershell
python coordinator_server.py --port 50050 --workers localhost:50061,localhost:50062
```

Expected behavior:

```text
Coordinator running on port 50050
Workers: localhost:50061, localhost:50062
```

Keep this terminal open.

---

### Terminal 4 — Run Client

Run one of the following commands.

#### Grayscale

```powershell
python client.py --image images\entrada.png --operation grayscale --output results\saida_grayscale.png
```

#### Invert colors

```powershell
python client.py --image images\entrada.png --operation invert --output results\saida_invert.png
```

#### Blur

```powershell
python client.py --image images\entrada.png --operation blur --output results\saida_blur.png
```

#### Edge detection

```powershell
python client.py --image images\entrada.png --operation edges --output results\saida_edges.png
```

---

## Available Image Operations

| Operation | Description | Example Output |
|---|---|---|
| `grayscale` | Converts the image to grayscale | `results\saida_grayscale.png` |
| `invert` | Inverts the image colors | `results\saida_invert.png` |
| `blur` | Applies a blur filter | `results\saida_blur.png` |
| `edges` | Applies edge detection | `results\saida_edges.png` |

---

## Expected Outputs

After running the client, the processed images will be saved in the `results` folder.

Expected files:

```text
results\saida_grayscale.png
results\saida_invert.png
results\saida_blur.png
results\saida_edges.png
```

To check the folder from PowerShell:

```powershell
dir results
```

To open the output folder:

```powershell
explorer results
```

---

## Example Execution

### Step 1: Start both workers

Worker 1:

```powershell
python worker_server.py --port 50061 --id worker1
```

Worker 2:

```powershell
python worker_server.py --port 50062 --id worker2
```

### Step 2: Start the coordinator

```powershell
python coordinator_server.py --port 50050 --workers localhost:50061,localhost:50062
```

### Step 3: Run the client

```powershell
python client.py --image images\entrada.png --operation grayscale --output results\saida_grayscale.png
```

### Step 4: Check the output

```powershell
dir results
```

Expected result:

```text
saida_grayscale.png
```

---

## Lamport Clock Logs

During execution, each process prints logs with Lamport timestamps.

Example:

```text
[Lamport=001] [client] Sending image to coordinator
[Lamport=002] [coordinator] Received image from client
[Lamport=003] [coordinator] Sending block 0 to worker localhost:50061
[Lamport=004] [worker1] Received block 0
[Lamport=005] [worker1] Finished processing block 0
[Lamport=006] [coordinator] Received processed block 0
[Lamport=007] [coordinator] Rebuilding final image
[Lamport=008] [client] Received final processed image
```

These logs are useful because they show the logical order of events across distributed processes.

---

## Preliminary Failure Test

Although full fault tolerance is expected to be expanded in a later stage, this version can be used to perform a simple worker availability test.

### Test procedure

1. Start Worker 1.
2. Start Worker 2.
3. Start the Coordinator.
4. Stop Worker 2 by pressing `CTRL + C`.
5. Run the client again.

Example:

```powershell
python client.py --image images\entrada.png --operation grayscale --output results\saida_failure_test.png
```

Expected output:

```text
results\saida_failure_test.png
```

If the system still processes the image using the available worker, this can be described as a preliminary test of worker unavailability.

---

## Troubleshooting

### Problem: PowerShell blocks virtual environment activation

Error example:

```text
running scripts is disabled on this system
```

Solution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

---

### Problem: `pip` is not recognized

Use:

```powershell
python -m pip --version
```

If needed:

```powershell
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

---

### Problem: `grpc_tools` module not found

Install dependencies again:

```powershell
python -m pip install -r requirements.txt
```

Or install gRPC tools manually:

```powershell
python -m pip install grpcio grpcio-tools
```

---

### Problem: `PIL` module not found

Install Pillow:

```powershell
python -m pip install pillow
```

---

### Problem: Connection refused

This usually means the coordinator or workers are not running.

Check if you started the system in this order:

```text
1. Worker 1
2. Worker 2
3. Coordinator
4. Client
```

---

### Problem: Port already in use

If a port is already being used, stop the previous process with `CTRL + C`.

Default ports:

| Process | Port |
|---|---|
| Coordinator | `50050` |
| Worker 1 | `50061` |
| Worker 2 | `50062` |

You can also change the ports manually:

```powershell
python worker_server.py --port 50063 --id worker1
```

Then start the coordinator with the updated worker port:

```powershell
python coordinator_server.py --port 50050 --workers localhost:50063,localhost:50062
```

---

## How to Stop the System

To stop any running process, go to its terminal and press:

```text
CTRL + C
```

Stop the processes in any order.

---

## Assignment Context

This project was created for the first practical assignment of a Distributed Computing course.

The assignment requires the development of a distributed system with at least two distributed computing mechanisms. This project implements:

- gRPC-based RPC communication;
- Lamport logical clocks.

The project also demonstrates:

- distributed task decomposition;
- message passing;
- coordinator-worker architecture;
- parallel processing;
- logical event ordering.

---

## Evidence for the Report

For the assignment report, the following evidence can be collected:

| Evidence | Description |
|---|---|
| Screenshot of Worker 1 terminal | Shows Worker 1 receiving and processing blocks |
| Screenshot of Worker 2 terminal | Shows Worker 2 receiving and processing blocks |
| Screenshot of Coordinator terminal | Shows image splitting, task distribution, and result merging |
| Screenshot of Client terminal | Shows client request and output generation |
| Screenshot of `results` folder | Shows generated processed images |
| Screenshot of Lamport logs | Shows logical ordering of distributed events |
| Screenshot of failure test | Shows behavior when a worker is stopped |

---

## Possible Future Improvements

Possible improvements for the second assignment include:

- robust failure detection;
- automatic task redistribution when a worker fails;
- leader election;
- distributed mutual exclusion;
- performance comparison between local and distributed execution;
- support for multiple physical machines in a local network;
- dynamic worker discovery;
- coordinator replication;
- task retry mechanism;
- execution time measurement;
- scalability analysis with more workers.

---

## Authors

Developed by the group as part of the Distributed Computing course.

Suggested role division:

| Role | Responsibility |
|---|---|
| Architecture | Define the distributed system structure |
| gRPC implementation | Define `.proto` services and implement communication |
| Coordinator | Implement image splitting and result merging |
| Workers | Implement distributed image processing |
| Lamport Clock | Implement logical clock updates and event logs |
| Testing | Execute functional and preliminary failure tests |
| Documentation | Write README and assignment report |
| Presentation | Prepare system demonstration and explanation |

---

## License

This project is intended for academic purposes.
