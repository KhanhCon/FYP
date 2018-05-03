import SimpleHTTPServer
import SocketServer
import os

def http_server():
    os.chdir('static')
    PORT = 9000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "serving at port", PORT
    httpd.serve_forever()

if __name__ == "__main__":
    http_server()