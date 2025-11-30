import xmlrpc.client
import os
import base64

HOST = '127.0.0.1'
PORT = 8000
BUFFER_SIZE = 1024

def send_file_rpc(filepath):
	if not os.path.exists(filepath):
		print(f"Error: File not found at: {filepath}")
		return

	filename = os.path.basename(filepath)

	# Create Proxy
	server_url = f"http://{HOST}:{PORT}"
	try:
		proxy = xmlrpc.client.ServerProxy(server_url)
	except ConnectionRefusedError:
		print("Error: Could not connect to the RPC server.")
		return

	print(f"Connected to RPC Server at {server_url}. Starting file transfer...")

	# Call remote function
	if not proxy.start_transfer(filename):
		print(f"Error starting transfer on server for {filename}")
		return

	bytes_sent = 0
	with open(filepath, 'rb') as f:
		while True:
			chunk = f.read(BUFFER_SIZE)
			is_final = not chunk  # True if chunk empty

			if not chunk and not is_final:
				break

			encoded_chunk = base64.b64encode(chunk).decode('utf-8')

			# Remote Procedure Call
			success = proxy.transfer_chunk(filename, encoded_chunk, is_final)
			if not success:
				print("Error during chunk transfer. Stopping.")
				break

			bytes_sent += len(chunk)

			if is_final:
				break
	print(f"File transfer complete. Total bytes sent: {bytes_sent}.")

if __name__ == "__main__":
	file_path = input("Enter file you want to send: ")
	send_file_rpc(file_path)
