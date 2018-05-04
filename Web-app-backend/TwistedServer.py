from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor, endpoints
import os

def twisted_server():
    dirname = os.path.dirname(os.path.abspath(__file__))
    resource = File(os.path.join(dirname,'app/reactApp/build'))
    factory = Site(resource)
    PORT = 9000
    endpoint = endpoints.TCP4ServerEndpoint(reactor, PORT)
    endpoint.listen(factory)
    print "serving at port", PORT
    reactor.run()

if __name__ == "__main__":
    twisted_server()