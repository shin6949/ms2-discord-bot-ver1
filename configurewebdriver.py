# webdriver 옵션 정의
from selenium import webdriver


def make_webdriver():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("disable-gpu")  # 가속 사용 x
        options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument(
            'user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1')
        # user-agent 이름 설정

        chrome = webdriver.Chrome('chromedriver', options=options)
    except Exception as e:
        print(e)

    return chrome
