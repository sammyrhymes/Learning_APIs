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
