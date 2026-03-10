import urllib.request
from urllib.error import HTTPError

try:
    response = urllib.request.urlopen('http://127.0.0.1:8000/')
    with open('error.html', 'wb') as f:
        f.write(response.read())
except HTTPError as e:
    with open('error.html', 'wb') as f:
        f.write(e.read())
