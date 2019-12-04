# -*- coding: utf-8 -*-
import requests, json, time
import smtplib
import datetime
import logging
from models import User, add_data_to_db
from config import TOKEN, GMAIL_PASSWORD, GMAIL_USER


logging.basicConfig(filename='log.txt', level=logging.INFO)
log = logging.getLogger('MAIN')


def logger(func):
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            with open('time.txt', 'a') as f:
                f.write(result)
        return result

    return wrap


class VkApiUse:
    def __init__(self):
        # with requests.Session() as self.session:
        #     # self.session.proxies = proxy
        self.session = requests.Session()
        self.data = ''
        self.id = ''
        self.token = TOKEN
        self.base_url = 'https://api.vk.com/method/{}.get?v=5.92&access_token={}'
        self.online = 0

    def connection(self, user_id):
        method = 'friends'
        f = self.session.get(self.base_url.format(method, self.token) + '&user_id={}&fields=online'.format(user_id))
        data = json.loads(f.text)
        return data

    def uid_to_id(self, friend_id):
        method = 'users'
        r = self.session.get(self.base_url.format(method, self.token) + '&user_ids={}'.format(friend_id))
        data = json.loads(r.text)
        user_id = int(data['response'][0]['id'])
        return user_id

    def time_beauty(self):
        time = datetime.datetime.now()
        day = time.day
        hour = time.hour + 7
        minute = time.minute

        if hour >= 24:
            hour -= 24
            day += 1
        if minute < 10:
            minute = '0{}.format(minute)'
        if hour < 10:
            hour = '0{}.format(hour)'

        return '{}.{} {}:{}'.format(day, time.month, hour, minute)

    @logger
    def is_online(self, data, friend_id):
        list_of_friends = data['response']['items']
        result = ''
        email = Email('antonbat125a@yandex.ru')
        friends_online = []
        for i in list_of_friends:
            if i['online']:
                first_name = i.get('first_name')
                last_name = i.get('last_name')
                mobile = i.get('online_mobile')
                app = i.get("online_app")
                vk_id = i.get('id')
                date_time = datetime.datetime.now()
                friends_online.append(User(first_name, last_name, mobile, app, date_time, vk_id))

            if i['id'] == friend_id:
                if i['online'] == 1 and 'online_mobile' in i and 'online_app' in i:
                    result = 'mobile: {} app: {} {}\n'.format(i.get("online_mobile"), i.get("online_app"), datetime.datetime.now())

                elif i['online'] == 1 and 'online_mobile' not in i:
                    result = 'Desktop  {}\n'.format(datetime.datetime.now())
                    email.send_email(result)

                elif i['online'] == 1 and i.get('online_mobile') == 1 and 'online_app' not in i:
                    result = 'only Mobile desktop version, without app_version {}\n'.format(datetime.datetime.now())
                    email.send_email(result)
                else:
                    continue

            else:
                continue
        add_data_to_db(friends_online)

        return result
# 2274003 android 3140623-iphone maybe Natalia, 2685278, 12274003, 12685278, 13140623
# 13395158


class Email:

    def __init__(self, email):
        self.email = email

    def send_email(self, message=None):
        sent_from = GMAIL_USER
        to = self.email
        subject = 'OMG Super Important Message'
        body = message

        email_text = """\
        From: %s
        To: %s
        Subject: %s
        %s
        """ % (sent_from, to, subject, body)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')


if __name__ == '__main__':
    try:
        while True:
            user = VkApiUse()
            user_id = user.uid_to_id('id11706070')
            data_user = user.connection(user_id)
            friend_id = user.uid_to_id('natali_lomova')
            user.is_online(data_user, friend_id)
            time.sleep(60)
    except Exception as e:
        log.exception('MAIN_ERROR')
        Email('antonbat125a@yandex.ru').send_email("Exception: {} ".format(e))
