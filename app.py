from flask import Flask, jsonify, request,send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json, uuid
from datetime import datetime

app = Flask(__name__)
@app.route('/auth' , methods=['GET'])
def auth():
    hwid = request.json.get('hwid')
    with open("data/database.json", "r+") as f:
        data = json.load(f)
    if hwid in data:
        if hwid in data and data[hwid]['status'] == 'blacklisted':
            return jsonify({"Info":"Your hwid has been blacklisted."}), 400
        else:
            if data[hwid]["expire"] <  datetime.today().strftime('%Y-%m-%d'):
                return  jsonify({"Status":"Error","Info":"Your subcription has expired"}),400
            else:
                return jsonify({"Status":'Succes',"Info":"Whitelisted"}), 200
    else:
        return jsonify({"Info":"Not whitelisted"})
            


@app.route('/create', methods=['POST'])
def createdata():
    userkey = request.json.get('key')
    hwid = request.json.get('hwid')
    with open("data/keys.json", "r") as f:
        keys_data = json.load(f)
    with open("data/database.json", "r+") as f:
        data = json.load(f)
        if userkey not in keys_data:
            return jsonify({"Status":"Error","Info":"This key does not exist or it has expired"}), 400
        elif keys_data[userkey]["expire"] < datetime.today().strftime('%Y-%m-%d'):
            return jsonify({"Status": "Error" ,"Info":"This key has expired"}), 400
        else:
            data[hwid] = {
                "key": userkey,
                "expire": keys_data[userkey]["expire"],
                "status":"Whitelisted"
            }
            f.seek(0)
            json.dump(data, f)
            with open("data/keys.json", "w") as f:
                keys_data[userkey]["used"] = True
                json.dump(keys_data, f)
            return jsonify({"Status":"Success","Info":"Your hwid has been whitelisted"}), 200




    
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080)

    
    

    
