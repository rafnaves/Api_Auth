from flask import Flask
from flask_sqlachemy import SQLAlchemy


#__name__ = __main__
app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

tasks = []
task_id_control = 1

@app.route('/hello_world', methods=['GET'])
def hello_world():
    return "Hello World"



if __name__ == "__main__":
    app.run(debug=True)


