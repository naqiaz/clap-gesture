import requests
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np


#phyphox configuration
PP_ADDRESS = "http://192.168.1.99:8080" # replace with your address shown in the phyphox app!!!
PP_CHANNELS = ["dB", "time", "mean"]

#global var to save timestamp
xs = []

# global array to save acceleration
dB =[]
time = []
mean = []

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
    [n_db, n_time, n_mean] = getSensorData() # get nth sample
    t = dt.datetime.now().strftime('%M:%S.%f') #%H:%M:%S.%f
    xs.append(t) 
    dB.append(n_db)
    time.append(n_time)
    mean.append(n_mean)
    return [t, n_db, n_time, n_mean]
    
# tracking number of claps

def main():
    analyze = [] #list
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
            #print('time: ', n_time, ' // dB: ', n_db, 'clap_count: ', clap_count, 'action: ',action)

        analyze.append(float(n_db))
        nums = analyze[-2:-1]

        if len(nums) >= 1:
            # was having trouble with the high resolution of this sensor... it detected 1 clap 10+ times...
            # " n_time > last_time + 0.5 "  #  -> as soon as -40 decibel threshold is passed, waits 0.5 seconds to detect again (to prevent excess detection)
            # seems to work for single and double claps... although may not be 100% accurate 
            if nums[0] > -40 and (n_time > last_time + 0.5): # -40 is a threshold value that works 
                clap_count += 1
                last_time = float(n_time)
            
            # resets the clap counter every two seconds
            if (n_time > reset_time + 2):
                reset_time = n_time
                clap_count = 0
            
            # determine which action based on clap count
            # checks the clap count every 1.5 seconds
            # 1 - clap -> play/pause
            # 2 - clap -> rewind
            # 3+ - clap -> FastForward
            if (clap_count > 0 and (n_time > clap_time + 1.5)):
                if (clap_count == 1):
                    if (action == "play"):
                        action = "pause"
                        last_action = "play"
                        # print('clap_count: ', clap_count, 'action: ', action, 'last_action: ', last_action)
                    else:
                        action = "play"
                        last_action = "pause"
                        # print('clap_count: ', clap_count, 'action: ', action, 'last_action: ', last_action)
                if (clap_count == 2):
                        action = "rewind"
                        last_action = "play"
                        # print('clap_count: ', clap_count, 'action: ', action, 'last_action: ', last_action)
                if (clap_count > 2):
                        action = "forward"
                        last_action = "play"
                        # print('clap_count: ', clap_count, 'action: ', action, 'last_action: ', last_action)
                clap_time = n_time
                        
           # when a new action is determined, the video is manipulated based on that action
            while (last_action != action):  
                #Jess's Code
                action = last_action = play            
if __name__ == '__main__':
    main()
