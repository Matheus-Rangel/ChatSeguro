import socket
import select
from crypto import s_des, d_hell
import json
HEADER_LENGTH = 10

IP = "0.0.0.0"
PORT = 1234
# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind, so server informs operating system that it's going to use given IP and port
# For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
server_socket.bind((IP, PORT))

# This makes server listen to new connections
server_socket.listen()

# List of sockets for select.select()
sockets_list = [server_socket]

# List of connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Handles message receiving
def receive_message(client_socket):

    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False
        try:
            u = clients[client_socket]
            decifred_header = s_des.decipher_text(message_header, u['privateKey'])
        except KeyError:
            decifred_header = message_header
        # Convert header to int value
        message_length = int(decifred_header.decode('utf-8').strip())
        # Return an object of message header and message data
        data = client_socket.recv(message_length)
        return {'header': message_length, 'data': data}
    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False

while True:

    # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    # Iterate over notified sockets
    for notified_socket in read_sockets:

        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()

            # Client should send his name right away, receive it
            message = receive_message(client_socket)
            if message is False:
                continue
            user = json.loads(message['data'], encoding='utf-8')
            # If False - client disconnected before he sent his name
            hellman = d_hell.Dhell()

            user['privateKey'] = hellman.generate_key(user['publicKey'])
            print(user['privateKey'])
            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)
            message = json.dumps({'publicKey': hellman.public_key}).encode('utf-8')
            header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            user['header'] = f"{len(user['username']):<{HEADER_LENGTH}}".encode('utf-8')
            message = header + message
            client_socket.send(message)
            # Also save username and username header
            clients[client_socket] = user
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['username']))
        # Else existing socket is sending a message
        else:
            # Receive message
            message = receive_message(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['username']))
                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue
            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]
            message = message['data']
            message = s_des.decipher_text(message, user['privateKey'])
            print(f'Received message from {user["username"]}: {message}')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            # Iterate over connected clients and broadcast message
            for client_socket in clients:

                # But don't sent it to sender
                if client_socket != notified_socket:
                    user_d = clients[client_socket]
                    # Send user and message (both with their headers)
                    # We are reusing here message header sent by sender, and saved username header send by user when he connected
                    data = user['header'] + user['username'].encode('utf-8') + message_header + message
                    cipher_message = s_des.cipher_text(data, user_d['privateKey'])
                    client_socket.send(cipher_message)

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]
