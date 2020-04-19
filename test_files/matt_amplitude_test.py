import requests
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as anim

#phyphox configuration
PP_ADDRESS = "http://192.168.50.199:8080" # replace with your address shown in the phyphox app!!!
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
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
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
    clap_count = 0

    while True:
        [t, n_db, n_time, n_mean] = getData()
        print('time: ', t, ' // dB: ', n_db, ' // ', n_time, ' // ', n_mean, 'clap_count: ', clap_count)
        #time.sleep(INTERVALS/1000)   # Delays for INTERVALS seconds.
        if n_db > -25: # -25 is a random threshold value I chose
            clap_count += 1

if __name__ == '__main__':
    main()
