import requests
import datetime as dt
import time
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import pyautogui as pg

# To use with youtube workout video:
# 1.) Have youtube open in browser of choice behind python window, with python open in bottom half of screen
# 2.) Start playing video
# 3.) Use claps to manipulate video

# phyphox configuration
PP_ADDRESS = "http://192.168.1.77"  # replace with your address shown in the phyphox app!!!
PP_CHANNELS = ["dB", "time", "mean"]

# global var to save timestamp
xs = []

# global array to save acceleration
dB = []
time = []
mean = []
clapStarts = []


# make one of them true at a time
# isAnimate = False
# isCollectData = True


def getSensorData():
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS)) + "=full"
    data = requests.get(url=url).json()
    dB = data["buffer"][PP_CHANNELS[0]]["buffer"][0]
    time = data["buffer"][PP_CHANNELS[1]]["buffer"][0]
    mean = data["buffer"][PP_CHANNELS[2]]["buffer"][0]
    # print (accX, ' ', accY, ' ', accY)
    return [dB, time, mean]


def getData():
    [n_db, n_time, n_mean] = getSensorData()  # get nth sample
    t = dt.datetime.now().strftime('%M:%S.%f')  # %H:%M:%S.%fj
    xs.append(t)
    dB.append(n_db)
    time.append(n_time)
    mean.append(n_mean)
    return [t, n_db, n_time, n_mean]

def main():
    # click on youtube browser window
    pg.click(717, 100)  # Point(x=717, y=100) is the location of mouse to click on YouTube browser behind python

    analyze = []  # list
    clap_count = 0
    last_time = 0.0
    reset_time = 0.0
    clap_time = 0.0
    action = ""
    last_action = ""
    while True:
        [t, n_db, n_time, n_mean] = getData()
        # prints out data collected every 1 seconds
        # if(n_time > last_time + 1):
        #     print('time: ', n_time, ' // dB: ', n_db, ' // clap_count: ', clap_count, ' // action: ',action)
        #     last_time = n_time

        threshold = -70 # threshold for dB

        if (n_db > threshold and (n_time > last_time + .5)):  # clap crosses threshold
            clap_count += 1  # increment clap count
            print('time: ', n_time, ' // last time: ', last_time, ' // dB: ', n_db, ' // clap_count: ',
                  clap_count,
                  '// clap time: ', clap_time)
            last_time = n_time  # last time will always save the last clap

        if (n_time > reset_time + 3.0):
            reset_time = float(n_time)
            claps = clap_count
            clap_count = 0;
            if (claps == 1):  # 1  - clap -> play/pause
                if (action == "play"):
                    action = "pause"
                    last_action = "play"
                    print('claps: ', claps, ' action: ', action)
                    # pause video
                    pg.hotkey('space')
                else:
                    action = "play"
                    last_action = "pause"
                    print('claps: ', claps, ' action: ', action)
                    # play video
                    pg.hotkey('space')
            if (claps == 2):  # 2  - clap -> rewind
                action = "rewind"
                last_action = "play"
                print('claps: ', claps, ' action: ', action)
                # rewind 10 seconds
                pg.hotkey('j')
            if (claps > 2):  # 3+ - clap -> FastForward
                action = "forward"
                last_action = "play"
                print('claps: ', claps, ' action: ', action)
                # fast forward 10 seconds
                pg.hotkey('l')

if __name__ == '__main__':
    main()