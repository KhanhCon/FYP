
import requests
import time
start = time.time()
for i in range(30):
    requests.get('http://localhost:5000/top?date=2018-02-03&numberof_libraries=100')
end = time.time()
print(end - start)



