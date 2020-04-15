import time


def configure(start_time, msg, message):
    if str(message.author.id) == "{DEVELOPER_USER_ID}":
        process_time = "\n연산 시간: {}".format(str(time.time() - start_time))
    else:
        process_time = ""

    return msg + process_time
