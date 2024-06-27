import socket
import threading

# Server configuration
HOST = 'localhost'
PORT = 5555

# List to store connected clients
clients = []

# Function to handle each client's connection
def handle_client(client_socket):
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                # If no message received, client disconnected
                remove_client(client_socket)
                break
            print(f"Received message: {message}")

            # Broadcast message to all clients
            broadcast(message, client_socket)
        except:
            # If error occurs, client disconnected
            remove_client(client_socket)
            break

# Function to broadcast message to all clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # If error occurs, client disconnected
                client.close()
                remove_client(client)

# Function to remove client from list
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        print("Client disconnected.")
        client_socket.close()
      # Function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server started on {HOST}:{PORT}")

    while True:
        # Accept new client connection
        client_socket, client_address = server.accept()
        print(f"Client connected from {client_address}")

        # Add client to list
        clients.append(client_socket)

        # Create thread to handle client communication
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Start the server
start_server()
