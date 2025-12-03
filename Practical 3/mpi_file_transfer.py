from mpi4py import MPI
import os
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

SENDER_RANK = 0
RECEIVER_RANK = 1
BUFFER_SIZE = 1024
OUTPUT_DIR = 'received_mpi_files'

# Run only on the process with Rank = 0
def sender_process(filepath):
	if size < 2:
		print(f"Error: MPI requires at least 2 processes. Current size: {size}")
		return

	if not os.path.exists(filepath):
		print(f"[RANK {rank}] Error: File not found at: {filepath}")
		return

	filename = os.path.basename(filepath)
	filesize = os.path.getsize(filepath)

	print(f"[RANK {rank}] Starting transfer of '{filename}' ({filesize} bytes) to RANK {RECEIVER_RANK}")

	# 1. Send Metadata
	comm.send(filename, dest=RECEIVER_RANK, tag=1)
	comm.send(filesize, dest=RECEIVER_RANK, tag=2)

	# Wait comfirm from Receiver
	ack = comm.recv(source=RECEIVER_RANK, tag=3)
	if ack != "READY":
		print(f"[RANK {rank}] Receiver not ready. Aborting.")
		return

	bytes_sent = 0
	with open(filepath, 'rb') as f:
		while True:
			chunk = f.read(BUFFER_SIZE)
			if not chunk:
				break

			comm.send(chunk, dest=RECEIVER_RANK, tag=4)
			bytes_sent += len(chunk)

	# Send termination signal
	comm.send(None, dest=RECEIVER_RANK, tag=5)
	print(f"[RANK {rank}] File sent successfully. Total: {bytes_sent} bytes.")

# Run only on process with Rank = 1
def receiver_process():
	if not os.path.exists(OUTPUT_DIR):
		os.makedirs(OUTPUT_DIR)
	print(f"[RANK {rank}] Waiting for file transfer from RANK {SENDER_RANK}...")

	try:
		# Receive Metadata
		filename = comm.recv(source=SENDER_RANK, tag=1)
		filesize = comm.recv(source=SENDER_RANK, tag=2)

		output_filename = os.path.join(OUTPUT_DIR, "MPI_RECEIVED_" + os.path.basename(filename))
		print(f"[RANK {rank}] Receiving file: {output_filename} ({filesize} bytes)")

		comm.send("READY", dest=SENDER_RANK, tag=3)

		bytes_received = 0
		with open(output_filename, 'wb') as f:
			while bytes_received < filesize:
				status = MPI.Status()
				comm.Probe(source=SENDER_RANK, tag=MPI.ANY_TAG, status=status)

				incoming_tag = status.Get_tag()

				# Signal terminate
				if incoming_tag == 5:
					comm.recv(source=SENDER_RANK, tag=5)
					break

				chunk = comm.recv(source=SENDER_RANK, tag=4)

				if not chunk:
					break

				f.write(chunk)
				bytes_received += len(chunk)

		print(f"[RANK {rank}] File received successfully. Total: {bytes_received} bytes.")
	except Exception as e:
		print(f"[RANK {rank}] An error occured during receive: {e}")

# Main Logic: assign tasks base on Rank
if __name__ == "__main__":
	if rank == SENDER_RANK:
		default_file = 'test_file.txt'
		if not os.path.exists(default_file):
			with open(default_file, 'w') as f:
				f.write("This is a test file for MPI transfer. " * 50)
			print(f"Created a temporary test file: {default_file}")

		sender_process(default_file)

	elif rank == RECEIVER_RANK:
		receiver_process()
	elif size == 1:
		print("Run MPI with 'mpiexec -n 2 python mpi_file_transfer.py' for two processes.")
	else:
		pass

	comm.Barrier()
