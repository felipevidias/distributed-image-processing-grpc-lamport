# Distributed Image Processing with gRPC and Lamport Clocks

A distributed image processing system built with **Python**, **gRPC**, **Protocol Buffers**, and **Lamport logical clocks**.

This project was developed as part of the first assignment for the **Distributed Computing** course. Its main goal is to demonstrate how a computational task can be divided among multiple distributed nodes, processed in parallel, and coordinated through remote procedure calls.

---

## Overview

The system processes an image in a distributed way.

A client sends an image to a coordinator server. The coordinator splits the image into horizontal blocks and distributes those blocks among available worker nodes. Each worker processes its assigned block and returns the result to the coordinator. Finally, the coordinator merges all processed blocks and sends the final image back to the client.

The system also implements Lamport logical clocks to record the logical order of distributed events, such as message sending, message receiving, block distribution, worker processing, and image reconstruction.

---

## Distributed Computing Requirements

This project implements two main distributed computing requirements:

### 1. Remote Procedure Calls with gRPC

The communication between the client, coordinator, and workers is implemented using gRPC.

Main communication flow:

```text
Client -> Coordinator
Coordinator -> Worker 1
Coordinator -> Worker 2
Worker 1 -> Coordinator
Worker 2 -> Coordinator
Coordinator -> Client
