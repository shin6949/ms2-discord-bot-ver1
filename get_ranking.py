from bs4 import BeautifulSoup
import math
from collections import defaultdict
import requests

# 별도 파일
import Write_error_log


def return_location():
    return "GuildOXBot - get_ranking.py"


def html_source_request(url):
    return requests.get(url).text


def get_guild_ranking(gettype):
    try:
        if gettype == "realtime":
            url = "http://maplestory2.nexon.com/Rank/Guild?tp=realtime"
        else:
            url = "http://maplestory2.nexon.com/Rank/Guild"

        html = BeautifulSoup(html_source_request(url), 'html.parser').select("tbody")[0]
        ranking = html.find_all("tr")

        ranking_table = []
        count = 1
        for ranking_list in ranking:
            if not ranking_list.find_all("td")[0].get_text() == "":
                tmp = "```[" + ranking_list.find_all("td")[0].get_text() + "위]" + \
                      ranking_list.find_all("td")[1].get_text() + \
                      "\n길드장: " + ranking_list.find_all("td")[2].get_text() + "" \
                      "\n길드 트로피: " + ranking_list.find_all("td")[3].get_text() + "개```"
            else:
                tmp = "```[" + str(count) + "위]" + ranking_list.find_all("td")[1].get_text() + \
                      "\n길드장: " + ranking_list.find_all("td")[2].get_text() + "" \
                       "\n길드 트로피: " + ranking_list.find_all("td")[3].get_text() + "개```"
                count += 1

            ranking_table.append(tmp)

        msg = ""
        for i in ranking_table:
            msg += i

        return msg

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return "서버 내 문제로 인해 불러올 수 없습니다."


def get_guild_ranking_search_by_keyword(gettype, keyword):
    try:
        if gettype == "realtime":
            url = "http://maplestory2.nexon.com/Rank/Guild?tp=realtime&k=" + keyword
        else:
            url = "http://maplestory2.nexon.com/Rank/Guild?tp=daily&k=" + keyword

        html = BeautifulSoup(html_source_request(url), 'html.parser').select("tbody")[0]
        try:
            ranking = html.find_all("tr")

            ranking_table = []

            for ranking_list in ranking:
                guild = defaultdict(str)
                print(ranking_list)
                if ranking_list.find_all("img")[0]['alt'] == "길드이미지":
                    guild_name = ranking_list.find_all("td")[1].get_text()
                    tmp = "```[" + ranking_list.find_all("td")[0].get_text() + "위] " + guild_name + \
                          "\n길드장: " + ranking_list.find_all("td")[2].get_text() + "" \
                          "\n길드 트로피: " + ranking_list.find_all("td")[3].get_text() + "개```"

                    if not html.find_all("img")[0]['src'] == "http://ua.maplestory2.nx.com/":
                        imgurl = html.find_all("img")[0]['src']
                    else:
                        imgurl = "http://s.nx.com/S2/Game/maplestory2/MAVIEW/data/character/ico_defalt.gif"
                else:
                    guild_name = ranking_list.find_all("td")[1].get_text()
                    tmp = "```[" + ranking_list.find_all("img")[0]['alt'] + "] " + guild_name + \
                          "\n길드장: " + ranking_list.find_all("td")[2].get_text() + "" \
                          "\n길드 트로피: " + ranking_list.find_all("td")[3].get_text() + "개```"

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
            url = "http://maplestory2.nexon.com/Rank/Character?tp=realtime"
        else:
            url = "http://maplestory2.nexon.com/Rank/Character"

        html = BeautifulSoup(html_source_request(url), 'html.parser').select("tbody")[0]
        ranking = html.find_all("tr")

        ranking_table = []

        count = 1
        for ranking_list in ranking:
            if not ranking_list.find_all("td")[0].get_text() == "":
                tmp = "```[" + ranking_list.find_all("td")[0].get_text() + "위] " + ranking_list.find_all("td")[1].get_text() + \
                  "\n트로피: " + ranking_list.find_all("td")[2].get_text() + "개```"
            else:
                tmp = "```[" + str(count) + "위] " + ranking_list.find_all("td")[1].get_text() + \
                  "\n트로피: " + ranking_list.find_all("td")[2].get_text() + "개```"
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
            url = "http://maplestory2.nexon.com/Rank/Character?tp=realtime&k=" + keyword
        else:
            url = "http://maplestory2.nexon.com/Rank/Character?tp=daily&k=" + keyword

        html = BeautifulSoup(html_source_request(url), 'html.parser').select("tbody")[0]
        try:
            ranking = html.find_all("tr")

            ranking_table = []
            for ranking_list in ranking:
                person = defaultdict(str)

                if ranking_list.find_all("td")[0].get_text() == "":
                    person_name = ranking_list.find_all("td")[1].get_text()
                    tmp = "```[" + ranking_list.find_all("img")[0]['alt'] + "] " + ranking_list.find_all("td")[1].get_text() + \
                          "\n트로피: " + ranking_list.find_all("td")[2].get_text() + "개```"

                    try:
                        imgurl = html.find_all("img")[1]['src']
                    except:
                        imgurl = "http://s.nx.com/S2/Game/maplestory2/MAVIEW/data/character/ico_defalt.gif"
                else:
                    person_name = ranking_list.find_all("td")[1].get_text()
                    tmp = "```[" + ranking_list.find_all("td")[0].get_text() + "위] " + ranking_list.find_all("td")[1].get_text() + \
                          "\n트로피: " + ranking_list.find_all("td")[2].get_text() + "개```"

                    try:
                        imgurl = html.find_all("img")[0]['src']
                    except:
                        imgurl = "http://s.nx.com/S2/Game/maplestory2/MAVIEW/data/character/ico_defalt.gif"

                person['name'] = person_name
                person['personmsg'] = tmp
                person['imgurl'] = imgurl

                ranking_table.append(person)

            return ranking_table

        except:
            return "찾는 캐릭터는 없는 캐릭터 입니다."

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))

        return "서버 내 문제로 인해 불러올 수 없습니다."


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

