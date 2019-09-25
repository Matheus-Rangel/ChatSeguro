import socket
import select
import errno
from crypto import s_des, d_hell
import sys
import json
HEADER_LENGTH = 10

IP = "localhost"
PORT = 1234
username = input("Username: ")
# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well

h = d_hell.Dhell()
user = {'username': username, 'publicKey': h.public_key}
message = json.dumps(user).encode('utf-8')
header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
message = header + message
client_socket.send(message)
while True:
    try:
        res_lenght = int(client_socket.recv(HEADER_LENGTH).decode('utf-8').strip())
        message = client_socket.recv(res_lenght)
        break
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue
message = json.loads(message.decode('utf-8'))
pk = message['publicKey']
key = h.generate_key(pk)
while True:
    # Wait for user to input a message
    message = input(f'{username} > ')

    # If message is not empty - send it
    if message:
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        data = message_header + message
        c_data = s_des.cipher_text(data, key)
        client_socket.send(c_data)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            d_data = client_socket.recv(HEADER_LENGTH)
            username_header = s_des.decipher_text(d_data, key)
            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            data = client_socket.recv(username_length)
            username_c = s_des.decipher_text(data, key)
            username_c = username_c.decode('utf-8')
            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            data = client_socket.recv(HEADER_LENGTH)
            message_header = s_des.decipher_text(data, key)
            message_length = int(message_header.decode('utf-8').strip())
            
            data = client_socket.recv(message_length)
            message = s_des.decipher_text(data, key)
            message = message.decode('utf-8')

            # Print message
            print(f'{username_c} > {message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()