from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
import statistics
import sqlite3
import json
import time
import re
import sys
import os
import pathlib
import getpass

#初期設定
mode = input("mode>")
checkword = input("checkword>")
#カレントディレクトリを取得
cwd = os.path.split(os.path.realpath(__file__))[0]
jsonPath = cwd + "/pivot.json"

USER = input("LoginID>")
PASS = getpass.getpass("LoginPassword>")

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome("D:\download\chrome\chromedriver.exe",chrome_options=options)
browser.implicitly_wait(1)

rootURL = "https://www.nicovideo.jp"
page = 1

#Pivotの読み込み
with open(jsonPath) as d:
    f = d.read()
    data = json.loads(f)

#json内部に検索キャッシュが存在したら利用する。
if not checkword in data.keys():
    pivot = 0
    myListCount = 0
    mylistName = checkword
else:
    pivot = data[checkword]["pivot"]
    myListCount = data[checkword]["count"]
    mylistName = data[checkword]["name"]

#ニコニコ動画へのログイン
def login():
    url_login = "https://account.nicovideo.jp/login?site=niconico&next_url=%2F&sec=header_pc&cmnhd_ref=device%3Dpc%26site%3Dniconico%26pos%3Dheader_login%26page%3Dtop"
    browser.get(url_login)
    e = browser.find_element_by_name("mail_tel")
    e.clear()
    e.send_keys(USER)
    e = browser.find_element_by_name("password")
    e.clear()
    e.send_keys(PASS)
    btn = browser.find_element_by_id('login__submit')
    btn.click()

#マイリスの生成
def mylistCreate():
    global mylistName
    mylistName = "%sその%s" % (checkword,str(int(myListCount/500+1)))
    while True:
        try:
            btn = browser.find_elements_by_css_selector('button.ActionButton.VideoMenuContainer-button')
            btn[1].click()
            btn = browser.find_element_by_xpath('//*[@data-mylist-id="-2"]')
            btn.click()
            e = browser.find_element_by_css_selector('input.AddingMylistModal-nameInput')
            e.send_keys(mylistName)
            btn = browser.find_element_by_css_selector('button.ActionButton.AddingMylistModal-submit')
            btn.click()
            print("mylistCreate:success")
            break
        except:
            time.sleep(10)
            browser.refresh()

#マイリス追加
def mylistAdd():
    while True:
        try:
            btn = browser.find_elements_by_css_selector('button.ActionButton.VideoMenuContainer-button')
            btn[1].click()
            btn = browser.find_element_by_xpath('//*[@data-mylist-name="%s"]' % mylistName)
            btn.click()
            btn = browser.find_element_by_css_selector("button.ActionButton.AddingMylistModal-submit")
            btn.click()
            print("mylistAdd:success")
            break
        except:
            time.sleep(10)
            browser.refresh()

#タグ固定のチェック
def TagCheck(tag):
    while True:
        check = False
        if not browser.page_source:
            time.sleep(1)
            browser.refresh()
            continue
        soup = BeautifulSoup(browser.page_source, "lxml")
        lookTagList = soup.select(".TagItem.is-locked.is-nicodicAvailable")
        if not lookTagList:
            access = soup.find("h1").text
            print(access)
            if access == "短時間での連続アクセスはご遠慮ください":
                time.sleep(70)
                browser.refresh()
                continue
            else:
                break
        for lookTag in lookTagList:
            tagName = lookTag.find("a",{"class":"Link TagItem-name"}).text
            if tagName == tag:
                check = True
                break
        print("TagCheck:"+str(check))
        break
    return check

#htmlからのデータ取得
def MainScraping(URL):
    global myListCount
    browser.get(rootURL + URL)
    time.sleep(0.5)
    name = None
    if TagCheck(checkword) == True:
        if myListCount % 500 == 0 and myListCount != 0 and mylistName != "%sその%s" % (checkword,str(int(myListCount/500+1))):
            mylistCreate()
        else:
            mylistAdd()
        name = mylistName
        myListCount += 1
    time.sleep(10)
    conn = sqlite3.connect('niconico.db')
    c = conn.cursor()

    c.execute('insert into ids(id,tag,name) values (?,?,?)',(int(URL[9:17]),checkword,name))

    conn.commit()
    conn.close()
    print(URL[9:17]+"finish")

#データベースへの登録
def DataBaseAdd(HLIdList):
    conn = sqlite3.connect('niconico.db')
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS ids_high''')
    c.execute('''DROP TABLE IF EXISTS ids_low''')
    c.execute("create table ids_high(id int,tag text)")
    c.execute("create table ids_low(id int,tag text)")
    c.executemany('insert into ids_high(id,tag) values (?,?)',HLIdList[0])
    c.executemany('insert into ids_low(id,tag) values (?,?)',HLIdList[1])
    conn.commit()
    conn.close()

#過去に登録したことがあるか
def Authentication(id):
    #Pivotの読み込み
    with open(jsonPath) as d:
        f = d.read()
        data = json.loads(f)

    #json内部に検索キャッシュが存在したら利用する。
    if not checkword in data.keys():
        pivot = 0
        myListCount = 0
        mylistName = checkword
    else:
        pivot = data[checkword]["pivot"]
        myListCount = data[checkword]["count"]
        mylistName = data[checkword]["name"]

    conn = sqlite3.connect('niconico.db')
    c = conn.cursor()

    if id >= pivot:
        print("high")
        c.execute("select id from ids_high where id = ? and tag = ?",(id,checkword))
    else:
        print("low")
        c.execute("select id from ids_low where id = ? and tag = ?",(id,checkword))
    check = c.fetchone()
    print(check)
    if check:
        print("Authentication:True")
        return True
    else:
        print("Authentication:False")
        return False

#Pivotの生成
def PivotCreate():
    conn = sqlite3.connect('niconico.db')
    c = conn.cursor()

    c.execute('select id,tag from ids where tag == ?',(checkword,))
    rawIdList = c.fetchall()
    rawIdList.sort()

    idList = [id[0] for id in rawIdList]

    with open(jsonPath) as d:
        f = d.read()
        data = json.loads(f)

    pivot = statistics.median_high(idList)
    pivotPoint = idList.index(pivot)
    data[checkword] = {}
    data[checkword]["pivot"] = pivot
    data[checkword]["count"] = myListCount
    data[checkword]["name"] = mylistName
    ids = [rawIdList[pivotPoint:],rawIdList[:pivotPoint]]
    with open(jsonPath,mode="w") as f:
    	json.dump(data,f,indent=4)

    conn.close()
    print(pivot)
    print(pivotPoint)
    return ids

#追加処理-発火ポイント
def AddMain():
    page = 1

    login()

    checkurl = "https://www.nicovideo.jp/tag/%s?page=%s&sort=f&order=a" % (checkword,page)

    browser.get(checkurl)

    while True:
        soup = BeautifulSoup(browser.page_source, "lxml")
        maindiv = soup.find("div",{"class":"contentBody video uad videoList videoList01"})
        if not maindiv:
            print("finish")
            break
        rawList = maindiv.select(".itemThumbWrap")

        URLs = []

        for raw in rawList:
            URLs.append(raw.get("href"))

        URLs = [x for x in URLs if x != "#" and "api" not in x]

        for URL in URLs:
            print(URL[9:17]+"start")
            if Authentication(int(URL[9:17])) == True:
                continue
            MainScraping(URL)

        page += 1
        checkurl = "https://www.nicovideo.jp/tag/%s?page=%s&sort=f&order=a" % (checkword,page)
        browser.get(checkurl)
        time.sleep(10)

    ids = PivotCreate()
    DataBaseAdd(ids)
    browser.quit()

#レギュ違反DB登録
def IdAdd(id):
    conn = sqlite3.connect('niconico.db')
    c = conn.cursor()

    c.execute('select id from ids where tag == ?',(checkword,))
    rawIdList = c.fetchall()
    rawIdList.append((id,checkword))
    rawIdList.sort()

    idList = [id[0] for id in rawIdList]

    with open(jsonPath) as d:
        f = d.read()
        data = json.loads(f)

    pivot = statistics.median_high(idList)
    pivotPoint = idList.index(pivot)
    if not checkword in data.keys():
        pivot = 0
        myListCount = 0
        mylistName = checkword
    else:
        pivot = data[checkword]["pivot"]
        myListCount = data[checkword]["count"]
        mylistName = data[checkword]["name"]
    ids = [rawIdList[pivotPoint:],rawIdList[:pivotPoint]]
    with open(jsonPath,mode="w") as f:
    	json.dump(data,f,indent=4)

    conn.close()
    print(pivot)
    print(pivotPoint)
    return ids

#動画データのマイリス保存先検索
def Check(id):
    conn = sqlite3.connect('niconico.db')
    c = conn.cursor()

    c.execute('select id,name from ids where tag == ? and id == ?',(checkword,id))
    data = c.fetchone()
    if data[1]:
        return data[1]
    else:
        return None

#削除発火ポイント
def RemoveMain():
    passid = int(input("id>"))
    if Authentication(passid) == True:
        answer = Check(passid)
        if not answer:
            print("This ID has not been added")
        else:
            print("Already added\nPlease delete it manually\nmylistName:" + answer)
    else:
        ids = IdAdd(passid)
        DataBaseAdd(ids,[(passid,checkword,None)])


if __name__ == "__main__":
    if mode == "add":
        AddMain()
    elif mode == "remove":
        RemoveMain()
    elif mode == "pivot":
        ids = PivotCreate()
        DataBaseAdd(ids)
