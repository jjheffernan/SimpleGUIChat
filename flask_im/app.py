import flask as fl
from flask import Flask

app = Flask(__name__)


@app.route('/')
def message_home():
    return fl.render_template('IM_home.html')


@app.route('/chat')
def chat_app():
    username = fl.request.args.get('username')
    room = fl.request.args.get('room')

    if username and room:
        return fl.render_template('chat.html')
    else:
        return fl.redirect(fl.url_for('home'))


if __name__ == '__main':
    # @app.run(debug=True)
    pass
