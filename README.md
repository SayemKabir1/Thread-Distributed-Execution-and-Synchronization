# Distributed Task Execution in Python

This project demonstrates a distributed task execution system using Python sockets. Multiple nodes (A, B, C) coordinate to execute tasks in a specific sequence, passing messages to synchronize execution. Each node runs independently, listening on specific ports and triggering the next node when its tasks are done.

## Features
- **Distributed Execution**: Tasks are divided across three nodes (A, B, C) and executed in a specific order.
- **Peer-to-Peer Communication**: Nodes communicate using sockets, sending and receiving messages to control task flow.
- **Message Passing**: Each node notifies the next when its tasks are complete, ensuring proper execution order.

## Execution Order

The tasks are executed in the following sequence:


Each node handles specific tasks:
- **Node A**: Executes tasks a1, a2, a3, a4
- **Node B**: Executes tasks b1, b2, b3, b4
- **Node C**: Executes tasks c1, c2, c3

## Prerequisites

- Python 3.x installed
- Basic understanding of socket programming

## How to Run

1. Clone the repository:
https://github.com/SayemKabir1/Thread-Distributed-Execution-and-Synchronization/blob/main/distributed_task_execution.py
   
