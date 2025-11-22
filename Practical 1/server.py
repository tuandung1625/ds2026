import socket
import os
import struct

HOST = '127.0.0.1'
PORT = 65432     
BUFFER_SIZE = 1024

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Server is listening on {HOST}:{PORT}...")

        conn, addr = s.accept()
        with conn:
            print(f"Connected successfully with Client: {addr}")

            # Part 1 : Received Metadata
            file_info_raw = conn.recv(8)
            if not file_info_raw:
                print("Error: Don't receive file's information.")
                return

            file_info = struct.unpack('>Ii', file_info_raw)
            filename_len = file_info[0]
            filesize = file_info[1]

            filename = conn.recv(filename_len).decode('utf-8')

            output_filename = "RECEIVED_" + os.path.basename(filename)
            print(f"Receive file: {output_filename} ({filesize} bytes)")

            # Part 2 : Receive file's information
            
            bytes_received = 0
            with open(output_filename, 'wb') as f:
                while bytes_received < filesize:
                    data_to_receive = min(BUFFER_SIZE, filesize - bytes_received) 
                    
                    chunk = conn.recv(data_to_receive)
                    if not chunk:
                        break 
                    
                    f.write(chunk)
                    bytes_received += len(chunk)

            print(f"File received. Total: {bytes_received} bytes.")

if __name__ == "__main__":
    start_server()