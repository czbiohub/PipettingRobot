import requests

serveradress = 'http://ip-of-pc-where-server.py-is-running:8080/update/'
def webrequest(step):
    # Send a GET request to serveradress/step until a 'done' is returned.
    done = False
    while not done:
        r = requests.get(serveradress + step)
        done = r.json()['done']

webrequest('capture_image')