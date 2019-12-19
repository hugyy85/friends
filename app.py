from flask import Flask
from connection import VkApiUse
from models import show_info_about_id, how_long_in_online

app = Flask(__name__)


@app.route('/show_history/<vk_name>/<limit>')
def show_history(vk_name, limit):
    ckecked_user = VkApiUse()
    vk_id = ckecked_user.uid_to_id(vk_name)
    return show_info_about_id(vk_id, limit)

@app.route('/show_history/friends_is_online/<limit>')
def show_how_long_in_online(limit):
    return how_long_in_online(limit)


if __name__ == '__main__':
    app.run()
