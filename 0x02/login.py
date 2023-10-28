from flask import Flask, render_template, session, flash \
    , request, redirect, url_for

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

user_list = [
    {
        "username" : "samuel",
        'password' : "12345678"
    },
    {
        "username" : "joshua",
        'password' : "12345678"
    }
]

@app.route('/')
def index():
    error = None
    if 'username' not in session:
        flash("Not logged in")
    return render_template("index.html", error = error)

@app.route('/login/', methods = ['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        for user in user_list:
            if username == user['username'] and password == user['password']:
                session['username'] = username
                flash('Successfully logged in')
                flash(f"Logged in as {session['username']}")
                return redirect(url_for('index'))
        error = 'inavlid username or password'
        return render_template("login.html", error = error)
    else:
        return render_template("login.html", error = error)
    
@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")

@app.route('/create_user/', methods = ['POST', 'GET'])
def add_user():
    error = None
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        for user in user_list:
            if username.strip('') == user["username"]:
                error = "User already exists"
                return redirect(url_for("add_user"), error = error)
    
        user_list.append({'username' : f'{username}', 
                        "password" : f"{password}"
                        })
        
        flash(f"account successfully created, logged in as {username}")
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('create_user.html')

@app.route("/admin/", methods = ['POST', 'GET'])
def admin():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get("password")
        if username == 'admin' and password == 'admin':
            session["username"] = username
            return redirect(url_for("admin"))
        else:
            error = "invalid username or Password"
            return redirect(url_for("admin"), error = error)
    return render_template("admin.html", user_list=user_list)



if __name__ == "__main__":
    app.run(debug=True)