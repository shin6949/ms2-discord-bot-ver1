from bs4 import BeautifulSoup
import math
from collections import defaultdict
import requests

# 별도 파일
import Write_error_log


# TODO: 소스 정리 필요
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

    return BeautifulSoup(html_source_request(url), 'html.parser').select("tbody")[0]


def get_guild_ranking(gettype):
    try:
        if gettype == "realtime":
            html = return_html_source("Guild", "realtime", "")
        else:
            html = return_html_source("Guild", "", "")

        ranking = html.find_all("tr")
        ranking_table = []
        count = 1

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

        msg = ""
        for i in ranking_table:
            msg += i

        return msg

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        print(e)
        return "서버 내 문제로 인해 불러올 수 없습니다."


def get_guild_ranking_search_by_keyword(gettype, keyword):
    try:
        if gettype == "realtime":
            html = return_html_source("Guild", "realtime", keyword)
        else:
            html = return_html_source("Guild", "", keyword)

        try:
            ranking = html.find_all("tr")

            ranking_table = []
            for ranking_list in ranking:
                guild = defaultdict(str)
                guild_name = ranking_list.find_all("td")[1].get_text()
                guild_leader = ranking_list.find_all("td")[2].get_text()
                guild_trop = ranking_list.find_all("td")[3].get_text()

                if ranking_list.find_all("img")[0]['alt'] == "길드이미지":
                    ranking = ranking_list.find_all("td")[0].get_text()
                    
                    tmp = "```[{}위] {}\n길드장: {}\n길드 트로피: {}개```".format(ranking, guild_name, guild_leader, str(guild_trop))

                    if not html.find_all("img")[0]['src'] == "http://ua.maplestory2.nx.com/":
                        imgurl = html.find_all("img")[0]['src']
                    else:
                        imgurl = "http://s.nx.com/S2/Game/maplestory2/MAVIEW/data/character/ico_defalt.gif"
                else:
                    ranking = ranking_list.find_all("img")[0]['alt']
                    tmp = "```[{}] {}\n길드장: {}\n길드 트로피: {}개```".format(ranking, guild_name, guild_leader, str(guild_trop))

                    try:
                        imgurl = html.find_all("img")[1]['src']
                    except:
                        imgurl = "http://s.nx.com/S2/Game/maplestory2/MAVIEW/data/character/ico_defalt.gif"

                guild['name'] = guild_name
                guild['guildmsg'] = tmp
                guild['imgurl'] = imgurl

                ranking_table.append(guild)

            return ranking_table

        except:
            return "찾는 길드는 없는 길드 입니다."

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))

        return "서버 내 문제로 인해 불러올 수 없습니다."


# 현재는 사용하지 않는 코드 (특정 순위 길드 찾기)
def get_guild_ranking_search_by_number(gettype, num):
    # ex) 465위 = 47페이지에서 찾아야함.

    page = math.trunc((int(num) / 10) + 1)

    try:
        url = "http://maplestory2.nexon.com/Rank/Guild"
        url += "?page=" + str(page)

        if gettype == "realtime":
            url += "&tp=realtime"

        html = BeautifulSoup(html_source_request(url), 'html.parser').select("tbody")[0]
        try:
            ranking = html.find_all("tr")

            ranking_table = []
            for ranking_list in ranking:
                if ranking_list.find_all("td")[0].get_text() == str(num):
                    tmp = "```[" + ranking_list.find_all("td")[0].get_text() + "위] " + ranking_list.find_all("td")[1].get_text() + \
                          "\n길드장: " + ranking_list.find_all("td")[2].get_text() + "" \
                          "\n길드 트로피: " + ranking_list.find_all("td")[3].get_text() + "개```"

                    ranking_table.append(tmp)

            msg = ""
            for i in ranking_table:
                msg += i

            return msg

        except:
            return "찾는 길드는 없는 길드 입니다."

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return "서버 내 문제로 인해 불러올 수 없습니다."


def get_person_ranking(gettype):
    try:
        if gettype == "realtime":
            html = return_html_source("Person", "realtime", "")
        else:
            html = return_html_source("Person", "", "")

        ranking = html.find_all("tr")
        ranking_table = []
        count = 1

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

        msg = ""
        for i in ranking_table:
            msg += i

        return msg

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))

        return "서버 내 문제로 인해 불러올 수 없습니다."


def get_person_ranking_search_by_keyword(gettype, keyword):
    try:
        if gettype == "realtime":
            html = return_html_source("Person", "realtime", keyword)
        else:
            html = return_html_source("Person", "", keyword)

        try:
            ranking = html.find_all("tr")
            ranking_table = []

            for ranking_list in ranking:
                person = defaultdict(str)
                nickname = ranking_list.find_all("td")[1].get_text()
                person_trop = ranking_list.find_all("td")[2].get_text()

                if ranking_list.find_all("td")[0].get_text() == "":
                    ranking_num = ranking_list.find_all("img")[0]['alt']
                    tmp = "```[{}위] {}\n트로피: {}개```".format(ranking_num, nickname, person_trop)

                    try:
                        imgurl = html.find_all("img")[1]['src']
                    except:
                        imgurl = "http://s.nx.com/S2/Game/maplestory2/MAVIEW/data/character/ico_defalt.gif"
                else:
                    ranking_num = ranking_list.find_all("td")[0].get_text()
                    tmp = "```[{}위] {}\n트로피: {}개```".format(ranking_num, nickname, person_trop)

                    try:
                        imgurl = html.find_all("img")[0]['src']
                    except:
                        imgurl = "http://s.nx.com/S2/Game/maplestory2/MAVIEW/data/character/ico_defalt.gif"

                person['name'] = nickname
                person['personmsg'] = tmp
                person['imgurl'] = imgurl
                print(imgurl)

                ranking_table.append(person)

            return ranking_table

        except:
            return "찾는 캐릭터는 없는 캐릭터 입니다."

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))

        return "서버 내 문제로 인해 불러올 수 없습니다."


# 지금은 사용하지 않는 기능 (순위로 찾기)
def get_person_ranking_search_by_number(gettype, num):
    # ex) 465위 = 47페이지에서 찾아야함.

    page = math.trunc((int(num) / 10) + 1)

    try:
        url = "http://maplestory2.nexon.com/Rank/Character"
        url += "?page=" + str(page)

        if gettype == "realtime":
            url += "&tp=realtime"

        html = BeautifulSoup(html_source_request(url), 'html.parser').select("tbody")[0]
        try:
            ranking = html.find_all("tr")

            ranking_table = []
            for ranking_list in ranking:
                if ranking_list.find_all("td")[0].get_text() == str(num):
                    tmp = "```[" + ranking_list.find_all("td")[0].get_text() + "위] " + ranking_list.find_all("td")[1].get_text() + \
                          "\n트로피: " + ranking_list.find_all("td")[2].get_text() + "개```"

                    ranking_table.append(tmp)

            msg = ""
            for i in ranking_table:
                msg += i

            return msg

        except:
            return "찾는 캐릭터는 없는 캐릭터 입니다."

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return "서버 내 문제로 인해 불러올 수 없습니다."

