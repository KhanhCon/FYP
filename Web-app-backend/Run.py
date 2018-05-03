import os
import subprocess
from multiprocessing import Process

from RocketServer import rocket_server
from TwistedServer import twisted_server


def twisted_server():
  subprocess.call('python TwistedServer.py', shell=True)

def rocket_server():
  subprocess.call('python -O RocketServer.py', shell=True)

if __name__ == '__main__':
  # subprocess.call('python -m pip install -r require_pypi.txt', shell=True)

  # os.chdir('app')
  p1 = Process(target=rocket_server)
  p1.start()
  p2 = Process(target=twisted_server)
  p2.start()
  p1.join()
  p2.join()