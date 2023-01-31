import psutil


def check_youtube():
    for proc in psutil.process_iter():
        try:
            # Check if process has a connection to youtube.com
            if "www.youtube.com/" in str(proc.connections()):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


if check_youtube():
    print("A browser is currently accessing YouTube.")
else:
    print("No browser is currently accessing YouTube.")
