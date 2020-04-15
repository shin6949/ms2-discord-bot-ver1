import Write_error_log


def return_location(mode):
    if mode == "Public":
        return "PublicOXBot - OX_Quiz_Result.py"
    elif mode == "Guild":
        return "GuildOXBot - OX_Quiz_Result.py"
    else:
        return "Unknown Mode - OX_Quiz_Result.py"


def cal(message, mode):
    try:
        cal = message.content.replace("!연산 ", "")
        python_cal = cal.replace("x", "*").replace("X", "*").replace("÷", "/")

        try:
            msg = '"{}"의 연산 결과\n{}'.format(cal, eval(python_cal))
            return msg
        except:
            msg = '"{}"의 연산 결과\n{}'.format(cal, "올바른 식을 입력하지 않아 계산이 되지 않았습니다.")
            return msg
    except Exception as e:
        Write_error_log.write_log(return_location(mode), str(e))
        print(e)
