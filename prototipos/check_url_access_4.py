import psutil


def check_browser_url(url):
    for proc in psutil.process_iter():
        try:
            if proc.name() in ["chrome", "brave," "firefox"]:
                for conn in proc.connections(kind="inet"):
                    if conn.status == "ESTABLISHED":
                        if url in conn.raddr.ip:
                            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


url = "https://www.hltv.org/"
if check_browser_url(url):
    print(f"Browser is currently accessing {url}")
else:
    print("Browser is not accessing the specified URL")
