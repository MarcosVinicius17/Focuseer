import psutil, time


def check_youtube():
    for proc in psutil.process_iter():
        try:
            if proc.name() in ["chrome", "firefox", "brave"]:
                if "youtube" in proc.cmdline():
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


while True:
    if check_youtube():
        print("A browser is currently accessing YouTube.")
        
        break
    else:
        print("No browser is currently accessing YouTube.")
        time.sleep(1)
