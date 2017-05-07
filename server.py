from flask import Flask 
import simplejson as json 
import time, sys, requests
from tinydb import TinyDB, Query

HOST = None
TIME_DELAY = 300
DB_ADDRESS = "db.json"

if len(sys.argv)>1 and sys.argv[1] == "prod":
        HOST = '0.0.0.0'

app = Flask(__name__)
db = TinyDB(DB_ADDRESS)

url = ""
with open("keys.json") as infile:
    url = json.load(infile)['url']

@app.route('/')
def hello():
    return "the server is up"

@app.route('/init_db')
def init_db():
    db.insert({"building" : "b21", "status" : "True"})
    return "done"

@app.route('/poll')
def poll():
    q = Query()
    while(True):
        curr_status = requests.get('https://b21.jerrington.me/api/status').json()['status']
        old_status = db.all()[0]['status'] #this can later be changed for multiple locations
        if old_status != str(curr_status):
            db.update({"status" : str(curr_status)}, q.building=="b21")
            post_slack()
        time.sleep(TIME_DELAY)

def post_slack():
    message = '"Someone is here, come on over! :) "'
    stat = db.all()[0]['status']
    if stat == "False":
        message = '"Sadly, nobody is here :("'
    payload = '{"text" :' + message + '}'
    print(payload)
    r = requests.post(url, data=payload)
    print(r.content)

if __name__ == "__main__":
    app.run(debug=True, port=43001, threaded=True, host=HOST)
