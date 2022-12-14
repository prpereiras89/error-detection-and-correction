# First of all import the socket library
import socket
import argparse

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--error", action='store_true',
        help="The algorithm to detect or correct error (types supported: parity, crc, hamming, reed).")
    args = vars(ap.parse_args())

    if args["error"]:
        print("Router with error!")
    else:
        print("Router with no error!")

    # Creating Socket Server
    socket_server = socket.socket()
    print("Socket server successfully created")

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port_server = 12345

    socket_server.connect(('127.0.0.1', port_server))
    print("socket server connected to %s" % (port_server))
    # put the socket into listening mode

    # Creating Socket Client
    socket_client = socket.socket()
    print("Socket client successfully created")

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port_client = 12346

    socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_client.bind(('', port_client))
    print("socket client binded to %s" % (port_client))
    # put the socket into listening mode
    socket_client.listen(5)
    print("socket client is listening")

    try:
        while True:
            # Establish connection with client.
            client, addr = socket_client.accept()
            print('Got connection from', addr)

            # Get data from client
            data = client.recv(1024)
            print("Received data from client:", data.decode())
            
            if not data:
                break

            # flipping one bit
            if args["error"]:
                print(args["error"])
                ans = list(data.decode())

                if ans[4] == '1':
                    ans[4] = '0'
                else:
                    ans[4] = '1'
                                    
                if ans[5] == '1':
                    ans[5] = '0'
                else:
                    ans[5] = '1'


                data = ''.join(ans).encode()


            # send to server
            socket_server.sendto(data,('127.0.0.1', port_server))
            # get from server
            data = socket_server.recv(1024)

            # send to clint
            client.sendto(data, ('127.0.0.1', port_server))
            client.close()

    except KeyboardInterrupt:
        print("\n\nShutdown...")

