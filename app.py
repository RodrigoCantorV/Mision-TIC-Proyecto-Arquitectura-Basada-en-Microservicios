from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from waitress import serve
import requests
import json

app = Flask(__name__)

cors = CORS(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-api-gateway"]+":" + str(dataConfig["puerto-gateway"]))
    serve(app,host=dataConfig["url-api-gateway"],port=dataConfig["puerto-gateway"])

