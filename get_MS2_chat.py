from bs4 import BeautifulSoup
from selenium import webdriver
from collections import defaultdict
import time


def make_webdriver():
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument("disable-gpu")  # 가속 사용 x
        options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument(
            'user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1')
        # user-agent 이름 설정

        chrome = webdriver.Chrome('chromedriver.exe', options=options)
    except Exception as e:
        print(e)

    return chrome


def get_world_chat(driver, chattype):
    try:
        # driver.get("http://maplestory2.nexon.com/MNow/Index")
        html = BeautifulSoup(driver.page_source, 'html.parser')

        chat = html.find_all("li", id=True)
        chat_list = []
        # driver.quit()

        for i in range(0, len(chat)):
            chat_imf = defaultdict(str)
            chat_imf['time'] = chat[i].find("span").get_text()
            chat_imf['type'] = chat[i].find_all("span")[1].get_text()
            chat_imf['author'] = "[" + chat[i].find_all("span")[2].get_text() + "]"
            chat_imf['content'] = chat[i].find_all("span")[3].get_text().replace(": ", "", 1)
            tmp = chat_imf['time'] + chat_imf['type'] + chat_imf['author'] + chat_imf['content']
            print(tmp)

            if chat_imf['type'] == chattype:
                chat_list.append(chat_imf)

        msg_list = []

        for num in chat_list:
            tmp = "```" + num['time'] + num['type'] + num['author'] + num['content'] + "```"
            msg_list.append(tmp)

        msg = ""
        for i in msg_list:
            msg += i

    except Exception as e:
        print(e)
        msg = "서버 내 문제로 인해 불러올 수 없습니다."

    return msg


def get_recent_chat(driver, chattype, index):
    try:
        html = BeautifulSoup(driver.page_source, 'html.parser')

        chat = html.find_all("li", id="50")
        chat_list = []
        # driver.quit()

        for i in range(index, len(chat)):
            chat_imf = defaultdict(str)
            chat_imf['time'] = chat[i].find("span").get_text()
            chat_imf['type'] = chat[i].find_all("span")[1].get_text()
            chat_imf['author'] = "[" + chat[i].find_all("span")[2].get_text() + "]"
            chat_imf['content'] = chat[i].find_all("span")[3].get_text().replace(": ", "", 1)
            tmp = chat_imf['time'] + chat_imf['type'] + chat_imf['author'] + chat_imf['content']
            print(tmp)

            if chat_imf['type'] == chattype:
                chat_list.append(chat_imf)

        msg_list = []

        for num in chat_list:
            tmp = "```" + num['time'] + num['type'] + num['author'] + num['content'] + "```"
            msg_list.append(tmp)

        msg = ""
        for i in msg_list:
            msg += i

    except Exception as e:
        print(e)
        msg = "서버 내 문제로 인해 불러올 수 없습니다."

    return msg


if __name__ == "__main__":
    li_index = 0
    driver = make_webdriver()
    driver.get("http://maplestory2.nexon.com/MNow/Index")
    print(get_world_chat(driver, "월드"))
    time.sleep(100)
    print("===========================")
    print(get_world_chat(driver, "월드"))
    time.sleep(100)
    print("===========================")
    print(get_recent_chat(driver, "월드"))

