from flask import Flask 
import requests
import simplejson as json 

app = Flask(__name__)
url = ""
with open("keys.json") as infile:
    url = json.load(infile)['url']

@app.route('/')
def hello():
    
    r = requests.post(url, json={"text" : "i'm being built"} )
    return "hello"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=43001)