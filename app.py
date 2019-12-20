from flask import Flask
from models import last_time_in_online, how_long_in_online

app = Flask(__name__)


@app.route('/show_history/<vk_name>/<limit>')
def show_last_time_in_online(vk_name, limit):
    return last_time_in_online(vk_name, limit)


@app.route('/show_history/friends_is_online/<limit>')
def show_how_long_in_online(limit):
    return how_long_in_online(limit)


if __name__ == '__main__':
    app.run()
