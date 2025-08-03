from flask import Flask, request, jsonify

app = Flask(__name__)
todos = []

@app.route('/')
def home():
    return "✅ Hello, this Flask app is running on Render for FREE!"

@app.route('/todos', methods=['GET', 'POST'])
def todo_list():
    if request.method == 'POST':
        task = request.json.get('task')
        if task:
            todos.append(task)
            return jsonify({"message": "Task added", "todos": todos})
        else:
            return jsonify({"error": "Task is required"}), 400
    return jsonify(todos)

if __name__ == '__main__':
    app.run(debug=True)