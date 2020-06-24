import time
import submit

while(True):
    try:
        submit()
    except:
        pass
    time.sleep(1)
    time.sleep(60*60-1)
