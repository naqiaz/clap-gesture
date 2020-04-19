import requests
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as anim



#phyphox configuration
PP_ADDRESS = "http://172.25.18.76:8080"
PP_CHANNELS = ["recording", 
                "recordingSquared", 
                # "sum", 
                # "mean", 
                # "dB"
                ]


#global var to save timestamp
xs = []

# global array to save acceleration
recording =[]
recordingSquared = []
# sum = []
# mean = []
# dB = []




def getSensorData():
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
    data = requests.get(url=url).json()
    recording = data["buffer"][PP_CHANNELS[0]]["buffer"][0]
    recordingSquared = data["buffer"][PP_CHANNELS[1]]["buffer"][0]
    # sum = data["buffer"][PP_CHANNELS[2]]["buffer"][0]
    # mean = data["buffer"][PP_CHANNELS[2]]["buffer"][0]
    # dB = data["buffer"][PP_CHANNELS[2]]["buffer"][0]
    return [recording, recordingSquared]
    
    
def getData():
    [nrecording, nrecordingSquared] = getSensorData() # get nth sample
    t = dt.datetime.now().strftime('%M:%S.%f') #%H:%M:%S.%f
    xs.append(t) 
    recording.append(nrecording)
    recordingSquared.append(nrecordingSquared)
    return [t, nrecording, nrecordingSquared]
    
    
def main():
   while True:
      [t, nrecording, nrecordingSquared] = getData()
      print(t, ' ', nrecording, ' ', nrecordingSquared)
      #time.sleep(INTERVALS/1000)   # Delays for INTERVALS seconds.

if __name__ == '__main__':
    main()


