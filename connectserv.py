import socket
import struct

SERVER_HOST = "localhost"
SERVER_PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    valueWelcome = "dany"
    client_socket.sendall((valueWelcome + "\n").encode())

    #Send int
    servIndexUser = 1
    servIndexUser_bytes = struct.pack('>I', servIndexUser)
    client_socket.sendall(servIndexUser_bytes)

    try:
        #Revice an int 
        servIndex = client_socket.recv(1024)
        servIndex = struct.unpack('>I', servIndex)[0]
        print(servIndex)
        welcomeMessage = client_socket.recv(1024)
        welcomemsg = welcomeMessage.decode()
        print(welcomemsg)
    except socket.timeout:
        # Gérer l'erreur de timeout ici
        pass

except ConnectionRefusedError:
    # Gérer l'erreur de connexion refusée ici
    pass
