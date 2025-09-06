from lib import memu
while True:
    bootopt = memu.memu_start()
    if bootopt == "exit":
        break
    if bootopt == "new":
        while True:
            nwn = "New World"
            nwopt = memu.memu_newworld(nwn,"")
            if nwopt == "back":
                break
    