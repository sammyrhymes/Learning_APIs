from flask import Flask, request, jsonify, url_for

app = Flask(__name__)

data_list = []
list_endpoints = []

@app.route('/api/add_data/', methods = ['POST'])
def add_data():

    try:
        data = request.get_json()
        data_list.append(data)
    
        return jsonify({'message' : 'Data Added Successfully'})
    
    except Exception as e:
        return jsonify({'error' : f'{e}'})

@app.route('/api/get_data/', methods = ['GET'])
def get_data():
    
    return jsonify(data_list)
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
    app.run(debug=True, port=5001)
@app.route('/api/get_data/<int:data_id>/', methods = ['GET'])
def get_name_data(data_id):
    
    if data_id < len(data_list):
        return jsonify({'item' : data_list[data_id]})
    
    return jsonify({'error' : 'Record not found'}, 404)

@app.route('/api/get_data/delete/<int:data_id>/', methods = ['DELETE'])
def delete_record(data_id):
    if data_id < len(data_list):
        data_list.pop(data_id)
        return jsonify({'success' : 'Item deleted successfully'})
    return jsonify({'warning' : 'delete successful'})

@app.route('/api/get_data/update/<int:data_id>/' , methods = ['PUT'])
def update_record(data_id):
    
    if data_id < len(data_list):
        data = request.get_json()
        data_list[data_id] = data
        return jsonify({'success' : 'Record Updated'})
    
    return jsonify({"error" : 'id beyond bounds'}, 404)

@app.route('/api/get_data/partial_update/<int:data_id>', methods = ['PATCH'])
def partial_update(data_id):
    
    if data_id < len(data_list):
        data = request.get_json()
        item = data_list[data_id]
    
        for key, value in data.items():
            item[key] = value
    
        return jsonify({'success' : 'Partial update complete'})
    
    return jsonify({'error' : 'partial update failed'})

@app.route('/api/headers/', methods = ['HEAD'])
def get_headers():
    headers = {
        "COntent-Type" : "Html/css",
        "content-size" : "1234"
    }
    response = jsonify({'message' : 'Rescource Metadata'})
    response.headers = headers
    return response

@app.route('/api/options/', methods = ['OPTIONS'])
def options():
    allowed_methods = ['GET', 'PUT', 'POST', 'PATCH', 'HEAD', 'OPTIONS', 'DELETE']
    headers = {'allowed methods' : f", ".join(allowed_methods)}
    return jsonify(headers, 200)

@app.route("/api/", methods =['GET'])
def endpoints():
    endpoint_list = ["add_data", "get_data", "get_headers", "get_name_data/<int:data_id>", "delete_record/<int:data_id>", "update_record/<int:data_id>", "partial_update/<int:data_id>", "options", ""]
    results = {"endpoints" : ["http://127.0.0.1:5000/api/" + url for url in endpoint_list]}
    return jsonify(results)


if __name__ == '__main__':
    app.run()
