# flask-unsign --unsign --cookie eyJ2ZXJ5X2F1dGgiOiJibGFuayJ9.YGHZvg.hvmOT3C_J1RVk3yrj7zA9Dxo8lA --wordlist wordlist.txt
#!/usr/bin/env python3

from flask import Flask, request, render_template, jsonify, abort, redirect, session
import uuid
import os
from datetime import datetime, timedelta
import hashlib
app = Flask(__name__)

server_start_time = datetime.now()
server_start_str = server_start_time.strftime('%Y%m%d%H%M%S')

print(f"[***  SERVER START STRING: {server_start_str} ***]")

secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()

print(f"[*** SECURE_KEY {secure_key} ***]")


app.secret_key = secure_key

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=300)
flag = os.environ.get('FLAG', "flag{this_is_a_fake_flag}")
secret = uuid.UUID('31333337-1337-1337-1337-133713371337')

@app.route('/user/<uid>')
def user_page(uid):
    """Display the user's session page based on their UUID."""
    try:
        uid = uuid.UUID(uid)
    except ValueError:
        abort(404)
    session['is_admin'] = False
    return 'Welcome Guest! Sadly, you are not admin and cannot view the flag.'

@app.route('/admin')
def admin_page():
    """Display the admin page if the user is an admin."""
    print(f"SESSION ADMIN in admin_page() --> {session.keys()}")
    if session.get('is_admin') and uuid.uuid5(secret, 'administrator') and session.get('username') == 'administrator':
        return flag
    else:
        abort(401)

@app.route('/status')
def status():
    current_time = datetime.now()
    uptime = current_time - server_start_time
    formatted_uptime = str(uptime).split('.')[0]
    formatted_current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    status_content = f"""Server uptime: {formatted_uptime}<br>
    Server time: {formatted_current_time}
    """
    return status_content
if __name__ == '__main__':
    app.run("0.0.0.0", port=9999)
