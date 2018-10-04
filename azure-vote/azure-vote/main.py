from flask import Flask, request, render_template
import os
import random
import redis
import socket
import sys
import requests

app = Flask(__name__)

# Load configurations
app.config.from_pyfile('config_file.cfg')
button1 =       app.config['VOTE1VALUE']  
button2 =       app.config['VOTE2VALUE']
title =         app.config['TITLE']

# Redis configurations
redis_server = os.environ['REDIS']

# Redis Connection
try:
    if "REDIS_PWD" in os.environ:
        r = redis.StrictRedis(host=redis_server,
                        port=6379, 
                        password=os.environ['REDIS_PWD'])
    else:
        r = redis.Redis(redis_server)
    r.ping()
except redis.ConnectionError:
    exit('Failed to connect to Redis, terminating.')

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

# Init Redis
if not r.get(button1): r.set(button1,0)
if not r.get(button2): r.set(button2,0)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        # Get current values
        vote1 = r.get(button1).decode('utf-8')
        vote2 = r.get(button2).decode('utf-8')            

        # Return index with values
        return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':
            
            # Empty table and return results
            r.set(button1,0)
            r.set(button2,0)
            vote1 = r.get(button1).decode('utf-8')
            vote2 = r.get(button2).decode('utf-8')
            return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)
        
        else:

            # Insert vote result into DB
            vote = request.form['vote']
            r.incr(vote,1)
            
            # Get current values
            vote1 = r.get(button1).decode('utf-8')
            vote2 = r.get(button2).decode('utf-8')  
                
            # Return results
            # return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)

            # Get the top vote
            # http://azure-calculator-api:8080 for local docker testing
            # http://azure-calculator-api.default:8080 for K8S
            #resp = requests.get('http://azure-calculator-api:8080/api/calculator/max?x=' + vote1 + '&y=' + vote2)
            resp = requests.get('http://azure-calculator-api.default:8080/api/calculator/max?x=' + vote1 + '&y=' + vote2)
    	    
            if resp.status_code != 200:
                # This means something went wrong.
                raise ApiError('GET /api/calculator/max {}'.format(resp.status_code))
            result = resp.json()["result"]

            if int(result) == int(vote1):
                topvote = button1
            else:
                topvote = button2            
    
            # Return results
            return render_template("index.html", topvote=topvote, value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)
if __name__ == "__main__":
    app.run()
