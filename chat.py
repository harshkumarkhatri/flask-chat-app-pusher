#importing the essentials
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pusher

#creating the pusher api with the essential details
pusher_client = pusher.Pusher(
  app_id='974496',
  key='1f5ffe8bac2c87112428',
  secret='1887c333a82fe31626d0',
  cluster='ap2',
  ssl=True
)

#instantiating the flask app
app = Flask(__name__)

#creating the database.db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

#instantiating the database
db = SQLAlchemy(app)

#creating the database model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    message = db.Column(db.TEXT())
    posted = db.Column(db.DateTime, default=datetime.now())


#displaying the messages from the database
@app.route('/')
def hello_world():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)


#taking the username and the messab=ge and storing it into the database.
@app.route('/message', methods=['POST'])
def message():
    try:
        username = request.form.get('username')
        message = request.form.get('message')
        pusher_client.trigger('chat-channel', 'new-message', {'username': username, 'message': message})
        save_message = Message(name=username, message=message)
        print(username)
        print(message)
        print(save_message)
        db.session.add(save_message)
        db.session.commit()
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'failure'})


#this will run our app.
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
