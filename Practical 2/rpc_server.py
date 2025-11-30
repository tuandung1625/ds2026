from xmlrpc.server import SimpleXMLRPCServer
import os
import base64

HOST = '127.0.0.1'
PORT = 8000
OUTPUT_DIR = 'received_rpc_files'

if not os.path.exists(OUTPUT_DIR):
	os.makedirs(OUTPUT_DIR)

file_handles = {}

def start_transfer(filename):
	try:
		if filename in file_handles:
			# close previous file (if exist)
			file_handles[filename].close()

		output_filename = os.path.join(OUTPUT_DIR, "RPC_RECEIVED_" + os.path.basename(filename))
		file_handles[filename] = open(output_filename, 'wb')
		print(f"SERVER ready to receive file: {output_filename}")
		return True
	except Exception as e:
		print(f"SERVER Erro starting transfer: {e}")
		return False

def transfer_chunk(filename, encoded_data, is_final):
	if filename not in file_handles:
		print(f"SERVER error: transfer not started for {filename}")
		return False
	try:
		chunk = base64.b64decode(encoded_data)

		# Write data
		file_handles[filename].write(chunk)

		if is_final:
			file_handles[filename].close()
			del file_handles[filename]
			print(f"[SERVER] Successfully closed and saved file: {filename}")
		return True
	except Exception as e:
		print(f"[SERVER] Error receiving chunk: {e}")
		if filename in file_handles:
			file_handles[filename].close()
			del file_handles[filename]
		return False

# Initialize and register Server
def start_rpc_server():
	try:
		with SimpleXMLRPCServer((HOST, PORT), logRequests=False, allow_none=True) as server:
			print(f"RPC Server listening on {HOST}:{PORT}...")

			# Register remote function
			server.register_function(start_transfer, 'start_transfer')
			server.register_function(transfer_chunk, 'transfer_chunk')

			# Run Server
			server.serve_forever()
	except OSError as e:
		print(f"Error: {e}. Port {PORT} might be in use.")
	except KeyboardInterrupt:
		print("\n SERVER Server stopped by user.")

if __name__ == "__main__":
	start_rpc_server()
