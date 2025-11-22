import socket
import os
import struct

HOST = '172.25.224.1'
PORT = 5000
BUFFER_SIZE = 1024

def send_file(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File not found at: {filepath}")
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"Connected successfully to Server {HOST}:{PORT}")
        except ConnectionRefusedError:
            print("Error: Server is not running or listening.")
            return

        # Part 1 : Send Metadata
        filename_len = len(filename)
        file_info = struct.pack('>Ii', filename_len, filesize)
        
        s.sendall(file_info) 
        s.sendall(filename.encode('utf-8')) 

        print(f"Sent Metadata: {filename} ({filesize} bytes). Start sending...")

        # Send file's information
        
        bytes_sent = 0
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(BUFFER_SIZE)
                if not chunk:
                    break
                s.sendall(chunk)
                bytes_sent += len(chunk)

        print(f"File sent successfully. Total: {bytes_sent} bytes.")

if __name__ == "__main__":
    file_path = input("Enter file you want to send: ")
    send_file(file_path)
