from datetime import datetime


def write_log(commit):
    try:
        logfile = open("./error.txt", 'a')
        error_msg = "{}\n{}\n".format(str(datetime.now()), commit)
        logfile.write(error_msg)
        logfile.close()
        return True

    except Exception as e:
        print(e)
        return False

