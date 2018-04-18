import logging
import sys

from rocket import Rocket
from FlaskApp import app

def run_server():
    # Setup logging
    log = logging.getLogger('Rocket')
    log.setLevel(logging.INFO)
    log.addHandler(logging.StreamHandler(sys.stdout))

    # Set the configuration of the web server
    server = Rocket(interfaces=('0.0.0.0', 5000), method='wsgi',
                    app_info={"wsgi_app": app})

    # Start the Rocket web server
    server.start()

if __name__ == "__main__":
    run_server()