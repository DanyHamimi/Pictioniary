import socket
import struct
import time
import threading
from PIL import Image

SERVER_HOST = 'localhost'
SERVER_PORT = 12345

def send_image(client_socket):
    try:
        with open('Imgs/canvas.jpg', 'rb') as file:
            image_data = file.read()
        
        size = len(image_data)
        size_bytes = size.to_bytes(4, byteorder='big')
        client_socket.sendall(size_bytes)
        client_socket.sendall(image_data)

        print(f'Image sent with size {size/1024} bytes.')
    except Exception as e:
        print(e)

    
def receive_and_process_images(client_socket):
    while True:
        data = client_socket.recv(4)
        if not data: break
        length = struct.unpack('>I', data)[0]
        img_data = b''
        while len(img_data) < length:
            img_data += client_socket.recv(min(length - len(img_data), 4096))
        # Process the received image here, e.g., save it to disk or display it.
        print('Image received.')
        #Create a new file and write the image data into it
        with open('Imgs/canvasR.jpg', 'wb') as file:
            file.write(img_data)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    threading.Thread(target=receive_and_process_images, args=(client_socket,)).start()

    while True:
        send_image(client_socket)
        time.sleep(0.1)  # Adjust the sleep time based on your needs.

if __name__ == '__main__':
    main()
