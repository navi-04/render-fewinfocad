from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Heroku! Your Python app is running globally.'

if __name__ == '__main__':
    app.run(debug=True)
