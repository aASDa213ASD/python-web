""" Server """
from http.server import CGIHTTPRequestHandler, HTTPServer

address = "127.0.0.1"
port = 9999

print("Starting local web server...")
print(f"Feel free to visit {address}:{port}.")

httpd = HTTPServer((address, port), CGIHTTPRequestHandler)
httpd.serve_forever()
