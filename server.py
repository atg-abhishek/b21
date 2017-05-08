from flask import Flask 
import simplejson as json 
import time, sys, requests
from tinydb import TinyDB, Query

HOST = None
TIME_DELAY = 5
DB_ADDRESS = "db.json"

if len(sys.argv)>1 and sys.argv[1] == "prod":
        HOST = '0.0.0.0'

app = Flask(__name__)
db = TinyDB(DB_ADDRESS)

url_b21 = ""
url_aifred = ""
with open("keys.json") as infile:
    temp = json.load(infile)
    url_aifred = temp['url_aifred']
    url_b21 = temp['url_b21']

@app.route('/')
def hello():
    return "the server is up"

# needs to be run the first time to kickstart with an entry in the DB
@app.route('/init_db')
def init_db():
    db.insert({"building" : "b21", "status" : "True"})
    return "done"

@app.route('/poll')
def poll():
    q = Query()
    while(True):
        curr_status = requests.get('https://b21.jerrington.me/api/status').json()['status']
        print(type(curr_status))
        old_status = db.all()[0]['status'] #this can later be changed for multiple locations
        print("old " + old_status)
        print("curr " + str(curr_status))
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
    r1 = requests.post(url_aifred, data=payload)
    r2 = requests.post(url_b21, data=payload)
    print(r1.content)
    print(r2.content)

if __name__ == "__main__":
    app.run(debug=True, port=43001, threaded=True, host=HOST)
