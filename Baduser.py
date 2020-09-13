import discord
import pymysql
import requests
from bs4 import BeautifulSoup

# 별도 파일
import Write_error_log
import public_SQL


def return_location():
    return "GuildOXBot - Baduser.py"


class Report:
    def __init__(self, **kwargs):
        self.__nickname_id = None if kwargs['nickname_id'] is None else kwargs['nickname_id']
        self.__reason = None if kwargs['reason'] is None else kwargs['reason']
        self.__add_time = None if kwargs['add_time'] is None else kwargs['add_time']
        self.__add_user = None if kwargs['add_user'] is None else kwargs['add_user']
        self.__add_user_id = None if kwargs['add_user_id'] is None else kwargs['add_user_id']

    def set_nickname_id(self, id):
        self.__nickname_id = id

    def set_add_user(self, id):
        self.__add_user = id

    def reason(self):
        return self.__reason

    def add_time(self):
        return self.__add_time

    def add_user(self):
        return self.__add_user

    def __str__(self) -> str:
        result = "```추가 시간: {}\n사유: {}\n제보자: {}```".format(self.add_time(), self.reason(), self.add_user())
        return result

    def add_to_db(self):
        # REPORT 정보 INSERT
        conn = public_SQL.bless_connection()

        # REPORT 정보 INSERT
        curs = conn.cursor()
        query = "INSERT INTO report(nick_value, reason, add_user, add_user_id, add_time) values (%s, %s, %s, %s, now())"
        curs.execute(query, (self.__nickname_id, self.__reason, self.__add_user, self.__add_user_id))
        conn.commit()
        conn.close()


# 차단 유저의 정보를 담는 클래스
class BadUser:
    def __init__(self, **kwargs):
        self.__conn = public_SQL.bless_connection()
        self.__report_list = []
        self.__nickname_id = None

        if kwargs['nickname'] is None:
            raise Exception("nickname empty")
        else:
            self.__nickname = kwargs['nickname']

        if kwargs['requested_user'] is None:
            raise Exception("Request_user Empty")
        else:
            self.__request_user = kwargs['requested_user']

        if kwargs['requested_user_id'] is None:
            raise Exception("Request_user_id Empty")
        else:
            self.__requested_user_id = kwargs['requested_user_id']

        self.__load_user_imf()

        if kwargs['reason'] is not None:
            tmp_report = Report(reason=kwargs['reason'], nickname_id=None, add_time=None,
                                add_user=self.__request_user, add_user_id=kwargs['requested_user_id'])
            self.__report_list.append(tmp_report)

    def __str__(self):
        result = "nickname = {}\nrequested_user = {}\njob = {}\nlen(report_list) = {}" \
            .format(self.nickname(), self.__request_user, self.job(), len(self.__report_list))

        count = 1
        for i in self.__report_list:
            result += "\n{}번째 Report\n{}".format(count, i.__str__())
            count += 1

        return result

    def __del__(self):
        self.__nickname_id = None
        self.__job = None
        self.__report_list = None
        self.__nickname = None
        self.__requested_user_id = None
        self.__request_user = None
        if self.__conn.open:
            self.__conn.close()

    def nickname(self):
        return self.__nickname

    def job(self):
        return self.__job

    def report_num(self):
        return self.__get_report_num()

    def records_text(self):
        records = self.__get_clear_record()
        result = ""

        for i in records:
            tmp = "{} (Lv.{}): {}회\n".format(i['boss_name'], i['boss_level'], i['record'])
            result += tmp

        return result

    # 크롤링을 통해 직업을 알아오는 함수
    def __get_job_info_from_website(self):
        find_boss = self.__get_boss_list()
        for i in find_boss:
            url = "http://maplestory2.nexon.com/Rank/Boss3?b={}&k={}".format(i['boss_id'], self.__nickname)
            html = BeautifulSoup(requests.get(url).text, 'html.parser') \
                .select(
                "#ranking_page > div.board_list4.rank_list_boss3 > div.board > table > tbody > tr > td.character > img.class")

            try:
                job = self.__judge_job(html[0]['src'])
                return job
            except:
                pass

        raise Exception("No User")

    # DB에 등록된 보스 id, 이름을 받아오는 함수
    def __get_boss_list(self):
        curs = self.__conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT id, boss_id, boss_name, boss_level FROM boss_value ORDER BY id ASC"
        curs.execute(query)
        rows = curs.fetchall()

        return rows

    # 가져온 값을 토대로 직업을 판단하는 함수
    def __judge_job(self, src):
        if src == "http://s.nx.com/S2/Game/maplestory2/MAVIEW/ranking/ico_assassin.png":
            return "어쌔신"
        elif src == "http://s.nx.com/S2/Game/maplestory2/MAVIEW/ranking/ico_knight.png":
            return "나이트"
        elif src == "http://s.nx.com/S2/Game/maplestory2/MAVIEW/ranking/ico_thief.png":
            return "시프"
        elif src == "http://s.nx.com/S2/Game/maplestory2/MAVIEW/ranking/ico_soulbinder.png":
            return "소울 바인더"
        elif src == "http://s.nx.com/S2/Game/maplestory2/MAVIEW/ranking/ico_wizard.png":
            return "위자드"
        elif src == "http://s.nx.com/S2/Game/maplestory2/MAVIEW/ranking/ico_archer.png":
            return "레인저"
        elif src == "http://s.nx.com/S2/Game/maplestory2/MAVIEW/ranking/ico_berserker.png":
            return "버서커"
        elif src == "http://s.nx.com/S2/Game/maplestory2/MAVIEW/ranking/ico_priest.png":
            return "프리스트"
        elif src == "http://s.nx.com/S2/Game/maplestory2/MAVIEW/ranking/ico_striker.png":
            return "스트라이커"
        elif src == "http://s.nx.com/S2/Game/maplestory2/MAVIEW/ranking/ico_heavygunner.png":
            return "헤비거너"
        elif src == "http://s.nx.com/S2/Game/maplestory2/MAVIEW/ranking/ico_runeblader.png":
            return "룬 블레이더"
        else:
            return "초보자"

    # 크롤링을 통해 던전 클리어 횟수를 알아오는 함수
    def __get_clear_record(self):
        find_boss = self.__get_boss_list()
        records = []

        for i in find_boss:
            if i['id'] <= 4:
                url = "http://maplestory2.nexon.com/Rank/Boss3?b={}&k={}".format(i['boss_id'], self.nickname())
                html = BeautifulSoup(requests.get(url).text, 'html.parser') \
                    .select(
                    "#ranking_page > div.board_list4.rank_list_boss3 > div.board > table > tbody > tr > td.record")

                try:
                    record = {"boss_name": i['boss_name'], "boss_level": i['boss_level'], "record": html[0].text}
                    records.append(record)

                except:
                    record = {"boss_name": i['boss_name'], "boss_level": i['boss_level'], "record": 0}
                    records.append(record)

        return records

    def __get_nickname_id(self):
        result = ""

        try:
            # 등록된 USER ID 받아오기
            curs = self.__conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT id FROM user WHERE nickname = %s"
            curs.execute(query, (self.nickname()))
            rows = curs.fetchall()

            self.__nickname_id = rows[0]['id']
            result = rows[0]['id']

        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))

        return result

    # DB에 추가하는 함수
    def add_to_db(self):
        try:
            # 이미 등록된 사람인지 확인
            curs = self.__conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT nickname FROM user WHERE nickname = %s"
            curs.execute(query, self.nickname())

            # 등록된 사람이 아니라면...
            if len(curs.fetchall()) == 0:
                # 직업 값 받아오기
                curs = self.__conn.cursor(pymysql.cursors.DictCursor)
                query = "SELECT id, name FROM job_value WHERE name = %s"
                curs.execute(query, self.job())
                rows = curs.fetchall()

                try:
                    # user 정보 insert
                    curs = self.__conn.cursor(pymysql.cursors.DictCursor)
                    query = "INSERT INTO user(nickname, job, add_time) values (%s, %s,now())"
                    curs.execute(query, (self.nickname(), rows[0]['id']))
                    self.__conn.commit()

                except Exception as e:
                    Write_error_log.write_log(return_location(), str(e))
                    raise Exception("DB Error")

            # report INSERT
            for i in self.__report_list:
                i.set_nickname_id(self.__get_nickname_id())
                i.set_add_user(self.__request_user)
                i.add_to_db()

            return True

        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))
            raise Exception("DB Error")

    # DB에서 유저 정보를 불러옴
    def __load_user_imf(self):
        try:
            # USER ID 받아오기
            curs = self.__conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT id FROM user WHERE nickname = %s"
            curs.execute(query, (self.nickname()))
            rows = curs.fetchall()

            # USER 정보가 있을 경우
            if len(rows) > 0:
                curs = self.__conn.cursor(pymysql.cursors.DictCursor)
                query = "SELECT u.id as nickname_id, j.name as job FROM user as u join job_value as j on u.job = j.id WHERE u.nickname = %s"
                curs.execute(query, (self.nickname()))
                rows = curs.fetchall()

                self.__nickname_id = rows[0]['nickname_id']
                self.__job = rows[0]['job']

            # 유저 정보가 없을 경우
            else:
                try:
                    self.__job = self.__get_job_info_from_website()

                except Exception as e:
                    Write_error_log.write_log(return_location(), str(e))
                    if str(e) == "No User":
                        raise Exception("No User")
                    else:
                        raise Exception("WEB Error")

        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))

            if str(e) == "No User":
                raise Exception("No User")
            elif str(e) == "WEB Error":
                raise Exception("WEB Error")
            else:
                raise Exception("DB Error")

    def __get_reports(self):
        try:
            # 유저가 있는지 찾기
            curs = self.__conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT id FROM user WHERE nickname = %s"
            curs.execute(query, self.nickname())
            rows = curs.fetchall()

            # 유저가 등록되어 있지 않다면, 등록된 적이 없는 것
            if len(rows) == 0:
                return False

            # 유저가 있다면, report 수집
            curs = self.__conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT nick_value, reason, add_user, add_user_id, add_time FROM report WHERE nick_value = %s ORDER BY add_time DESC LIMIT 3"
            curs.execute(query, rows[0]['id'])
            rows = curs.fetchall()

            self.__report_list = []

            for i in rows:
                self.__report_list.append(
                    Report(nickname_id=i['nick_value'], reason=i['reason'], add_user=i['add_user'],
                           add_time=i['add_time'], add_user_id=i['add_user_id']))

            return True

        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))
            raise Exception("DB Error")

    def __get_report_num(self):
        try:
            # 유저가 있는지 찾기
            curs = self.__conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT count(*) as count FROM report WHERE nick_value = %s GROUP BY nick_value"
            curs.execute(query, (self.__get_nickname_id()))
            rows = curs.fetchall()

            return rows[0]['count']

        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))
            raise Exception("DB Error")

    def get_add_result_text(self):
        result_text = "<@{}>님의 요청을 등록하였습니다.".format(self.__requested_user_id)
        embed = discord.Embed(title="캐릭터 등록 정보", description="  ", color=0xff0000)
        embed.add_field(name="닉네임", value=self.nickname(), inline=True)
        embed.add_field(name="직업", value=self.job(), inline=True)
        embed.add_field(name="누적 리포트 수", value=str(self.__get_report_num()) + "개", inline=True)

        return {"text": result_text, "embed": embed}

    def get_info(self):
        # 등록되어 있지 않다면
        if not self.__get_reports():
            return {"status": False, "text": "검색하신 캐릭터는 레이드 클리어 기록이 없거나 없는 유저로 판단됩니다."}

        # 등록되어 있다면
        embed = discord.Embed(title="캐릭터 등록 정보", description="  ", color=0xff0000)
        embed.add_field(name="닉네임", value=self.nickname(), inline=True)
        embed.add_field(name="직업", value=self.job(), inline=True)
        embed.add_field(name="리포트 수", value=str(self.__get_report_num()) + "개", inline=True)

        records_text = "최근 3건의 내역을 표시합니다."

        for i in self.__report_list:
            records_text += i.__str__()

        records_text += "\n70레벨 이상 보스 클리어 횟수 현황```"
        for i in self.__get_clear_record():
            tmp = "{}(LV.{}): {}회\n".format(i['boss_name'], i['boss_level'], i['record'])
            records_text += tmp

        records_text += "```"
        return {"status": True, "text": "<@{}>님이 요청하신 내용입니다.".format(self.__requested_user_id),
                "embed": embed, "records": records_text}


def get_all_user():
    try:
        conn = public_SQL.bless_connection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT u.nickname as nickname, JOB.name as job, count(*) as count " \
                "FROM report as r " \
                "JOIN user as u ON r.nick_value = u.id " \
                "JOIN (SELECT id, name FROM job_value)JOB ON u.job = JOB.id " \
                "GROUP BY nick_value " \
                "ORDER BY count(*) DESC " \
                "LIMIT 30"
        curs.execute(query)
        rows = curs.fetchall()
        conn.close()

        if len(rows) == 0:
            return {"status": False, "message": "검색 결과가 없습니다."}

        result = "리포트 많은 30명을 표시합니다.\n닉네임 / 직업 / 리포트 수```"
        for i in rows:
            result += "{} / {} / {}회\n".format(i['nickname'], i['job'], i['count'])

        result += "```"

        return {"status": True, "message": result}

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return {"status": False, "message": "내부 서버 오류로 인해 결과를 표시할 수 없습니다."}
