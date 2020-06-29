import time
import submit
import os

while(True):
    try:
        submit.submitall()
    except:
        pass
    time.sleep(1)
    time.sleep(60*60-1)
