import re
import urllib.request
import cv2
import requests
from bs4 import BeautifulSoup
import numpy

# 별도 파일
import Write_error_log


def return_location():
    return "GuildOXBot - get_ranking.py"


def html_source_request(url):
    return requests.get(url).text


# 유형, 타입, 검색어 여부에 따라 URL을 구성하고 HTML 구조를 리턴
def return_html_source(mode, type, keyword):
    if mode == "Guild":
        # 실시간 이냐 아니냐
        if type == "realtime":
            # 검색어가 있었는지 여부
            if len(keyword) > 0:
                # 특정 길드의 실시간 순위를 원하는 경우
                url = "http://maplestory2.nexon.com/Rank/Guild?tp=realtime&k={}".format(keyword)
            else:
                # 실시간 길드 순위 1페이지를 요청한 경우
                url = "http://maplestory2.nexon.com/Rank/Guild?tp=realtime"
        # 종합 순위를 요청한 경우 (1일 1회 갱신)
        else:
            if len(keyword) > 0:
                # 특정 길드의 종합 순위를 원하는 경우
                url = "http://maplestory2.nexon.com/Rank/Guild?tp=daily&k={}".format(keyword)
            else:
                # 종합 길드 순위 1페이지를 요청한 경우
                url = "http://maplestory2.nexon.com/Rank/Guild?tp=daily"

    # 개인 순위를 요청한 경우
    else:
        # 실시간 이냐 아니냐
        if type == "realtime":
            # 검색어가 있었는지 여부
            if len(keyword) > 0:
                # 특정 캐릭터의 실시간 순위를 원하는 경우
                url = "http://maplestory2.nexon.com/Rank/Character?tp=realtime&k={}".format(keyword)
            else:
                # 실시간 개인 트로피 순위 1페이지를 요청한 경우
                url = "http://maplestory2.nexon.com/Rank/Character?tp=realtime"
        # 종합 순위를 요청한 경우 (1일 1회)
        else:
            # 검색어가 있었는지 여부
            if len(keyword) > 0:
                # 특정 캐릭터의 종합 순위를 원하는 경우
                url = "http://maplestory2.nexon.com/Rank/Character?tp=daily&k={}".format(keyword)
            else:
                # 종합 개인 트로피 순위 1페이지를 요청한 경우
                url = "http://maplestory2.nexon.com/Rank/Character?tp=daily"

    # 위에서 구성한 url을 토대로 html 구조를 가져옴
    return BeautifulSoup(html_source_request(url), 'html.parser').select("tbody")[0]


# 길드 랭킹 1페이지
def get_guild_ranking(gettype):
    try:
        if gettype == "realtime":
            html = return_html_source("Guild", "realtime", "")
        else:
            html = return_html_source("Guild", "", "")

        ranking = html.find_all("tr")
        ranking_table = []
        # 1, 2, 3위는 html element에 순위가 표시되지 않으므로 int로 구성함
        count = 1

        # 결과 set 구성
        result = {'status': 'success', 'msg': ''}

        for i in ranking:
            guild_name = i.find_all("td")[1].get_text()
            guild_leader = i.find_all("td")[2].get_text()
            guild_trop = i.find_all("td")[3].get_text()

            if not i.find_all("td")[0].get_text() == "":
                ranking_num = i.find_all("td")[0].get_text()
                tmp = "```[{}위] {}\n길드장: {}\n길드 트로피: {}개```".format(ranking_num, guild_name, guild_leader, guild_trop)

            else:
                ranking_num = str(count)
                tmp = "```[{}위] {}\n길드장: {}\n길드 트로피: {}개```".format(str(ranking_num), guild_name, guild_leader, guild_trop)

            count += 1
            ranking_table.append(tmp)

        for i in ranking_table:
            result['msg'] += i

        return result

    # 1페이지는 무조건 존재하므로 에러가 발생하면, 코드 또는 서버 문제임
    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))

        result = {'status': 'error', 'msg': "서버 내 문제로 인해 불러올 수 없습니다."}

        return result


# 주어진 키워드를 기반으로 길드 순위를 찾는 함수
def get_guild_ranking_search_by_keyword(gettype, keyword):
    try:
        if gettype == "realtime":
            html = return_html_source("Guild", "realtime", keyword)
        else:
            html = return_html_source("Guild", "", keyword)

        result = {'status': 'success'}
        # tr에 있는 것들은 모두 순위임
        ranking = html.find_all("tr")

        # 이름으로 검색하는 경우, 일치 검색이므로 결과는 하나 뿐임
        # 길드 순위 -> 1,2,3위의 경우 순위 부분이 "길드이미지"라고 되어 있어서 다른 부분에서 순위와 이미지를 갖고옴.
        if ranking[0].find_all("img")[0]['alt'] == "길드이미지":
            # 순위 -> 1, 2, 3위는 "위"라는 글자까지 저장되므로 숫자만 추출함.
            result['rank'] = re.findall("\d+", ranking[0].find_all("td")[0].get_text())[0]

            if not html.find_all("img")[0]['src'] == "http://ua.maplestory2.nx.com/":
                result['imgurl'] = html.find_all("img")[0]['src']
            else:
                result['imgurl'] = "http://s.nx.com/S2/Game/maplestory2/MAVIEW/data/character/ico_defalt.gif"
        else:
            result['rank'] = re.findall("\d+", ranking[0].find_all("img")[0]['alt'])[0]

            try:
                result['imgurl'] = html.find_all("img")[1]['src']
            except:
                result['imgurl'] = "http://s.nx.com/S2/Game/maplestory2/MAVIEW/data/character/ico_defalt.gif"

        # 길드 이름
        result['name'] = ranking[0].find_all("td")[1].get_text()
        # 길드 장
        result['leader'] = ranking[0].find_all("td")[2].get_text()
        # 길드 트로피
        result['trop'] = ranking[0].find_all("td")[3].get_text()

        urllib.request.urlretrieve(result['imgurl'], result['name'] + ".png")

        # 파일 이름이 한글인 경우, openCV에서 읽을 수 없음.
        stream = open((result['name'] + ".png").encode("utf-8"), "rb")
        bytes = bytearray(stream.read())
        numpyArray = numpy.asarray(bytes, dtype=numpy.uint8)

        myimg = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)

        avg_color_per_row = numpy.average(myimg, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)

        result['r'] = int(avg_color[0])
        result['g'] = int(avg_color[1])
        result['b'] = int(avg_color[2])

        return result

    # 찾는 길드가 없는 경우 IndexError가 발생
    except IndexError:
        return {'status': 'error', 'msg': "찾는 길드는 없는 길드 입니다."}

    # 기타 에러인 경우, 서버 또는 코드 문제임
    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))

        return {'status': 'error', 'msg': "서버 내 문제로 인헤 불러올 수 없습니다."}


# 개인 트로피 1페이지를 구해오는 함수
def get_person_ranking(gettype):
    try:
        if gettype == "realtime":
            html = return_html_source("Person", "realtime", "")
        else:
            html = return_html_source("Person", "", "")

        ranking = html.find_all("tr")
        ranking_table = []
        # 1, 2, 3위는 html element에 순위가 표시되지 않으므로 int로 구성함
        count = 1

        result = {'status': 'success', 'msg': ''}

        for ranking_list in ranking:
            nickname = ranking_list.find_all("td")[1].get_text()
            personal_trop = ranking_list.find_all("td")[2].get_text()

            if not ranking_list.find_all("td")[0].get_text() == "":
                ranking = ranking_list.find_all("td")[0].get_text()
                tmp = "```[{}위] {}\n트로피: {}개```".format(ranking, nickname, personal_trop)

            # 1, 2, 3위인 경우 순위를 소스에서 가져올 수 없음. 그러므로 자체 카운트로 기재
            else:
                ranking = str(count)
                tmp = "```[{}위] {}\n트로피: {}개```".format(ranking, nickname, personal_trop)

                count += 1

            ranking_table.append(tmp)

        for i in ranking_table:
            result['msg'] += i

        return result

    # 1페이지는 무조건 존재하므로 에러가 발생하면, 코드 또는 서버 문제임
    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))

        return {'result': 'error', 'msg': "서버 내 문제로 인해 불러올 수 없습니다."}


# 키워드 기반 캐릭터 순위 검색
def get_person_ranking_search_by_keyword(gettype, keyword):
    try:
        if gettype == "realtime":
            html = return_html_source("Person", "realtime", keyword)
        else:
            html = return_html_source("Person", "", keyword)

        result = {'status': 'success'}
        # tr에 있는 것들은 모두 순위임
        ranking = html.find_all("tr")

        result['num'] = len(ranking)

        """
        닉네임 초기화로 인해, 닉네임 하나에 2개의 캐릭터가 검색되는 경우가 있음.
        이 봇을 통해 닉네임을 검색하는 경우는 트로피를 비교하기 위해서이므로, 대부분 트로피가 많을 것임. 그러므로 많은 사람을 기준으로 검색
        캐릭터는 트로피가 많은 순으로 등장하기 때문에 index 0를 기준으로 가져오면 됨
        """

        # 닉네임
        result['nickname'] = ranking[0].find_all("td")[1].get_text()
        # 트로피 개수
        result['trop'] = ranking[0].find_all("td")[2].get_text()

        # 1, 2, 3위의 경우 문제가 있으므로 예외 처리
        if ranking[0].find_all("td")[0].get_text() == "":
            # 순위 -> 1, 2, 3위는 "위"라는 글자까지 저장되므로 숫자만 추출함.
            result['rank'] = re.findall("\d+", ranking[0].find_all("img")[0]['alt'])[0]

            # 프로필 사진 링크
            try:
                result['imgurl'] = html.find_all("img")[1]['src']
            except:
                result['imgurl'] = "http://s.nx.com/S2/Game/maplestory2/MAVIEW/data/character/ico_defalt.gif"
        else:
            # 순위 -> 1, 2, 3위는 "위"라는 글자까지 저장되므로 숫자만 추출함.
            result['rank'] = re.findall("\d+", ranking[0].find_all("td")[0].get_text())[0]

            # 프로필 사진 링크
            try:
                result['imgurl'] = html.find_all("img")[0]['src']
            except:
                result['imgurl'] = "http://s.nx.com/S2/Game/maplestory2/MAVIEW/data/character/ico_defalt.gif"

        urllib.request.urlretrieve(result['imgurl'], result['nickname'] + ".png")

        # 파일 이름이 한글인 경우, openCV에서 읽을 수 없음.
        stream = open((result['nickname'] + ".png").encode("utf-8"), "rb")
        bytes = bytearray(stream.read())
        numpyArray = numpy.asarray(bytes, dtype=numpy.uint8)

        myimg = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)

        avg_color_per_row = numpy.average(myimg, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)

        result['r'] = int(avg_color[0])
        result['g'] = int(avg_color[1])
        result['b'] = int(avg_color[2])

        return result

    except IndexError:
        return {'status': 'IndexError', 'msg': "찾는 캐릭터는 없는 캐릭터 입니다."}

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))

        return {'status': 'error', 'msg': "서버 내 문제로 인해 불러올 수 없습니다."}
