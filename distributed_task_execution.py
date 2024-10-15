import socket
import threading
import time
import argparse

class Node:
    def __init__(self, node_id, tasks, next_node_ip, next_node_port, listen_port):
        self.node_id = node_id
        self.tasks = tasks  # List of tasks (e.g., ["a1", "a2", "a3"])
        self.next_node_ip = next_node_ip  # IP of the next node to notify
        self.next_node_port = next_node_port  # Port of the next node
        self.listen_port = listen_port  # Port for receiving task completion messages
        self.server_socket = None
    
    def run_server(self):
        # Setting up the server to receive messages from other nodes
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.listen_port))  # Listen on the specified port
        self.server_socket.listen(5)
        print(f"Node {self.node_id} listening on port {self.listen_port}...")

        while True:
            client_socket, addr = self.server_socket.accept()
            message = client_socket.recv(1024).decode()
            print(f"Node {self.node_id} received message: {message}")
            self.handle_message(message)
            client_socket.close()

    def handle_message(self, message):
        # Handle incoming messages (Task Done notifications)
        if message.startswith("Task done"):
            _, task_id = message.split(": ")
            if task_id == self.tasks[0]:
                # Execute next task
                self.execute_task()

    def execute_task(self):
        # Execute the first task in the list
        if self.tasks:
            task = self.tasks.pop(0)
            print(f"Node {self.node_id} executing {task}")
            time.sleep(2)  # Simulate task execution
            self.notify_next_node(task)

    def notify_next_node(self, task):
        # Notify the next node that the task is done
        if self.next_node_ip:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.next_node_ip, self.next_node_port))  # Connect to the next node's IP and port
                message = f"Task done: {task}"
                sock.sendall(message.encode())
                print(f"Node {self.node_id} sent message: {message}")

    def start(self):
        # Run the server in a separate thread
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

        # Start executing the first task immediately
        if self.tasks:
            self.execute_task()

def main():
    parser = argparse.ArgumentParser(description="Start a distributed node (A, B, or C).")
    parser.add_argument("node", choices=["A", "B", "C"], help="The node to start (A, B, or C).")
    args = parser.parse_args()

    # Assuming localhost IPs for simplicity; replace with actual IPs for different machines
    if args.node == "A":
        # Node A communicates with Node C
        node_a = Node(node_id="A", tasks=["a1", "a2", "a3", "a4"], next_node_ip='127.0.0.1', next_node_port=5001, listen_port=5000)
        node_a.start()

    elif args.node == "B":
        # Node B communicates with Node A
        node_b = Node(node_id="B", tasks=["b1", "b2", "b3", "b4"], next_node_ip='127.0.0.1', next_node_port=5000, listen_port=5002)
        node_b.start()

    elif args.node == "C":
        # Node C communicates with Node B
        node_c = Node(node_id="C", tasks=["c1", "c2", "c3"], next_node_ip='127.0.0.1', next_node_port=5002, listen_port=5001)
        node_c.start()

if __name__ == "__main__":
    main()
