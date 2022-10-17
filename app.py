from flask import Flask, render_template, redirect
import requests
import os
import logging

# Log only errors
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/home')


#########################
#  HOME/Service Status  #
#########################
def f2b_status():
    f = os.popen('sudo systemctl status fail2ban')
    status = f.read()
    if ("inactive" in status or "not running" in status):
        return "Not running"
    elif ("active" in status):
        return "Running"

@app.route('/home', methods=['GET', 'POST'])
def home():
    status = f2b_status()
    return render_template('index.html', status=status)

@app.route('/start', methods=['GET', 'POST'])
def start():
    s = os.popen('sudo systemctl start fail2ban')
    
    return redirect('/')

@app.route('/stop', methods=['GET', 'POST'])
def stop():
    s = os.popen('sudo systemctl stop fail2ban')

    return redirect('/')

@app.route('/restart', methods=['GET', 'POST'])
def restart():
    s = os.popen('sudo systemctl restart fail2ban')

    return redirect('/')


################
#  Banned IPs  #
################
def getcountry(ip):
	r = requests.get(f'http://ip-api.com/json/{ip}')
	parsed_json=r.json()
	return parsed_json

@app.route('/banned', methods=['GET', 'POST'])
def banned():
    lines = []
    with open('/var/log/fail2ban.log', 'r') as f:
        for line in f.readlines():
            if ('Ban') in line:
                lines.append(line)

    return render_template('banned.html', lines=lines, getcountry=getcountry)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
