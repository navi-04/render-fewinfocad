from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/')
def home():
    return "✅ Hello, this Flask app is running on Render for FREE!"

@app.route('/todos', methods=['GET', 'POST'])
def todo_list():
    global todos

    if request.method == 'POST':
        task = request.json.get('task')
    elif request.method == 'GET' and 'task' in request.args:
        task = request.args.get('task')
    else:
        task = None

    if task:
        todos.append(task)
        return jsonify({"message": "Task added", "todos": todos})

    return jsonify(todos)


if __name__ == '__main__':
    app.run(debug=True)