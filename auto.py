import time
import submit

while(True):
    try:
        submit()
    except:
        pass
    time.sleep(60*60)
    print('Hour:', hour)
