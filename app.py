from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return "Hello, this Flask app is running on Render"

USERS = {
    "naveen": "mySecret123",
    "john": "pass456"
}

@app.route("/check-login", methods=["POST"])
def check_login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    # Validate
    if username in USERS and USERS[username] == password:
        return jsonify({"result": True})
    else:
        return jsonify({"result": False})

# @app.route('/todos', methods=['GET', 'POST'])
# def todo_list():
#     global todos

#     task = None

#     if request.method == 'POST':
#         task = request.json.get('task')
#     elif request.method == 'GET' and 'task' in request.args:
#         task = request.args.get('task')
#     else:
#         task = None

#     if task:
#         todos.append(task)
#         return jsonify({"message": "Task added", "todos": todos})

#     return jsonify(todos)


if __name__ == '__main__':
    app.run(debug=True)