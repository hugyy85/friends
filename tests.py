import requests


def test_urls():
    base_url = 'http://localhost:5000'
    urls = [
        '/show_history/13025815/10',
        '/show_history/natali_lomova/1',
        '/show_history/friends_is_online/30',
        '/show_history/friend_time/13025815'
    ]
    for url in urls:
        response = requests.get(base_url + url)
        assert response.status_code == 200


if __name__ == '__main__':
    test_urls()