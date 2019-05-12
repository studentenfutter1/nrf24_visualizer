#!/usr/bin/python

import sys, os, time

# Add path to pyRadioHeadNRF24 module
sys.path.append(os.path.dirname(__file__)+ "/../" ) #+ "/../"

import pyRadioHeadNRF24 as radio
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation



x_len = 200         # Number of points to display
y_range = [0, 4095]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

# Add labels
plt.title('Received data')
plt.xlabel('Samples')
plt.ylabel('data')


nrf24 = radio.nRF24()

nrf24.init()
nrf24.setChannel(1)
nrf24.setRF(radio.nRF24.DataRate2Mbps, radio.nRF24.TransmitPower0dBm)

print("StartUp Done!")
print("Receiving...")


          
# This function is called periodically from FuncAnimation
def animate(i, ys):
        if nrf24.available():
                adc_value = 0;
                (msg, l) = nrf24.recv() # bytearray, hört auf bei 0x00
                print(msg)      # ->wenn  0x00 übertragen wird kommt msg == b''
                

                #if msg == bytearray('', 'utf-8'):
                      #  print("DEBUG")
                     #   msg = bytearray(0)

                msgList = list(msg)
                msgLen = len(msgList)

                if  msgLen > 28:
                        msgList = msgList[:28] # cut off after 28
                
                elif msgLen == 0: # fill empty list
                        c=msgLen
                        while c < 28:
                                msgList.append(0) # append 0 to empty list
                                c = c+1
                
                
                c = 0 
                while c < len(msgList)/2 - 1: # for loop 
                        highByte = msgList[c*2]
                        lowByte = msgList[(c*2) +1]
                        adc_value = (highByte << 8) | lowByte
                        ys.append(adc_value) # add value to ys list
                        print(adc_value)
                        c = c+1 # increment loop counter

        # Limit y list to set number of items
        ys = ys[-x_len:]
        # Update line with new Y values
        line.set_ydata(ys)
        return line,

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=50,
    blit=True)
plt.show()

