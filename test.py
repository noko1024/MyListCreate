import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def login():
    url= "https://account.nicovideo.jp/login"


    #ログインサイトと接続
    response = requests.get(url)
    #bs4解析準備
    print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    source = soup.find('input', {'name': 'auth_id', 'type': 'hidden'})
    print(source)



login()


