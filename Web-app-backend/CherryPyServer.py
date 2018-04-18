from cherrypy import wsgiserver
import cherrypy
from FlaskApp import app
from paste.translogger import TransLogger


from flask import Flask
import cherrypy
from paste.translogger import TransLogger

def run_server():
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5000,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()


# d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
# server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 5000), d)

if __name__ == '__main__':
    try:
        # run_server()
        # server.start()
        run_server()
    except KeyboardInterrupt:
        # server.stop()
        cherrypy.engine.stop()
