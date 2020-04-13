from datetime import datetime


def write_log(commit):
    try:
        logfile = open("./error.txt", 'a')
        logfile.write(str(datetime.now()))
        logfile.write("\n")
        logfile.write(commit)
        logfile.write("\n")
        logfile.close()
        return True

    except Exception as e:
        print(e)
        return False

