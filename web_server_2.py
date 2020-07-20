import io
import socket
import sys

class WSGIServer(object):

	address_family = socket.AF_INET
	socket_type = socket.SOCK_STREAM
	request_queue_size = 1

	def __init__(self, server_address):
		# Create a listening socket
		self.listen_socket = listen_socket = socket.socket(self.address_family,
														   self.socket_type)

		# Allow the reuse of the same address
		listen_socket.setsockopt(socket.SOL_SOCKET, socket.SOREUSEADDR, 1)

		# Bind the address to the socket
		listen_socket.bind(server_address)

		# Activate listening for a request on the socket
		listen_socket.listen(self.request_queue_size)

		# Get server hostname and port
		host, port = self.listen_socket.getsockname()[:2]
		self.server_name = socket.getfqdn(host)
		self.server_port = port

		# Headers set by web framework/application
		self.headers_set = []

	def set_app(self, application):
		self.application = application

	def serve_forever(self):
		listen_socket = self.listen_socket
		while True:
			# Accept a new client connection
			 self.client_connection, client_address = listen_socket.accept()

			# Handle one request and close the client connection. Then
			# loop over to wait for another client connection

			self.handle_one_request()

	def handle_one_request(self):
		request_data = self.client_connection.recv(1024)
		self.request_data = request_data = request_data.decode('utf-8')

		# Print formatted request data ~ 'curl -v'
		print(''.join(
			f'< {line}/n' for line in request_data.splitlines()))

