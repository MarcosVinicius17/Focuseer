import psutil

for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=["pid", "name", "cmdline"])
    except psutil.NoSuchProcess:
        pass
    else:
        if "youtube" in pinfo["cmdline"]:
            print(f"Process {pinfo['pid']} ({pinfo['name']}) is accessing YouTube")
        else:
            print("nothing there")
