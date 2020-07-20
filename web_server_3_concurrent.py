import errno
import os
import signal
import socket
import time

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5

def sig_child(signum, frame):
	while True:
		try:

			pid, status = os.waitpid(
				-1, 				# Wait for any child processes
				os.WNOHANG)			# Do not block and return EWOULDBLOCK error
		except OSError:
			return

		if pid == 0: # no more zooooooooombies
			return 


def handle_request(client_connection):
	request = client_connection.recv(1024)
	print('Child PID: {pid}. Parent PID {ppid}'.format(pid=os.getpid(),
													   ppid=os.getppid()))

	print(request.decode())
	http_response = b"""
HTTP/1.1 200 OK

Hello, world!
"""
	client_connection.sendall(http_response)
	# sleep to allow parent to loop over to 'accept' signal and then block
	time.sleep(3)

def serve_forever():
	listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	listen_socket.bind(SERVER_ADDRESS)
	listen_socket.listen(REQUEST_QUEUE_SIZE)
	print('Serving HTTP on port {port} ...'.format(port=PORT))
	print('Parent PID (PPID): {pid}\n'.format(pid=os.getpid()))

	signal.signal(signal.SIGCHLD, sig_child)
	while True:
		try:
			client_connection, client_address = listen_socket.accept()
		except IOError as e:
			code, msg = e.args
			# restart 'accept' if there was an interruption
			if code == errno.EINTR:
				continue
			else:
				raise

		pid = os.fork()
		if pid == 0: # child
			listen_socket.close() # close child copy
			handle_request(client_connection)
			client_connection.close()
			os._exit(0) # child exits stage left
		else: # parent
			client_connection.close() # close parent copy and loop over it

if __name__ == '__main__':
	serve_forever()