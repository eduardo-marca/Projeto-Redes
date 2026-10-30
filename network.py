import socket


PORT = 50000


class NetworkConnection:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.sock.settimeout(0.01)

        self.buffer = ""

    @classmethod
    def create_server(cls, port=PORT):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind(("0.0.0.0", port))
        server.listen(1)

        print(f"Waiting for a player on port {port}...")

        conn, address = server.accept()
        print(f"Player connected from {address}")

        server.close()

        return cls(conn)

    @classmethod
    def connect_to_server(cls, host, port=PORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print(f"Connecting to {host}:{port}...")
        sock.connect((host, port))

        print("Connected to server!")

        return cls(sock)

    def send_message(self, message: str):
        data = (message + "\n").encode("utf-8")
        self.sock.sendall(data)

    def receive_messages(self) -> list[str]:
        messages = []

        while True:
            try:
                data = self.sock.recv(4096)

                if not data:
                    raise ConnectionError("The other player disconnected.")

                self.buffer += data.decode("utf-8")

            except socket.timeout:
                break

        while "\n" in self.buffer:
            message, self.buffer = self.buffer.split("\n", 1)
            messages.append(message)

        return messages

    def close(self):
        self.sock.close()
        