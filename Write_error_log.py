from datetime import datetime


def write_log(location, commit):
    try:
        logfile = open("./error.txt", 'a')
        error_msg = "{} at {}\n{}\n\n".format(str(datetime.now()), location, commit)
        logfile.write(str(error_msg))
        logfile.close()
        return True

    except Exception as e:
        print(e)
        return False

