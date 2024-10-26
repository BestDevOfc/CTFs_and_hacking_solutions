users_db = {
    'guest': 'guest',
    'admin': os.environ.get('PASSWORD', 'TEST_PWD')
}

def valid_user(user):
    # compares the password in users_db with our supplied password
    return users_db.get(user['username']) == user['password']

if not session or 'user_data' not in session:
    return render_template("login.html", message="Login Please :D")

user = json.loads(session['user_data'])

if valid_user(user):
    if user['flag'] == True and user['username'] != 'guest':
        return FLAG
    else:
        return render_template("welcome.html", username=user['username'])


# solution put in oiuheigytdfegd as username and leave &password= (just empty) so it will be None and when Db search happens it will also be none,
  # so None == None = True so valid_user will give us the flag !
