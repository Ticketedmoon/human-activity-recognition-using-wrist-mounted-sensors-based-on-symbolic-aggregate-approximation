from datetime import datetime
from drawnow import *

import serial
import time
import numpy as np              #import numpy
import matplotlib.pyplot as plt #import matplotlib library

class Arduino:

    samples = []
    microvolts = []

    plt.ion()  # Tell matplotlib you want interactive mode to plot live data
    axes = plt.gca()

    def read_from_ppg(self):
        with serial.Serial('COM3', 19200, bytesize=serial.EIGHTBITS, timeout=0) as ser, open("voltages.csv", 'w') as text_file:
            data_row_sample = 0
            text_file.write("{}, {}\n".format("Samples", "Microvolts(mV)"))
            while True:
                voltage_reading = ser.readline().decode().strip("\n").strip("\r\n")
                if (voltage_reading != ""):
                    print(str(data_row_sample), voltage_reading) 
                    data = [str(data_row_sample), voltage_reading]
                    text_file.write("{}, {}\n".format(data_row_sample, voltage_reading))
                    text_file.flush()

                    self.samples.append(data_row_sample)      #Build our temperatureF array by appending temp readings
                    self.microvolts.append(voltage_reading)
                    self.sample = voltage_reading

                    drawnow(self.makeFig)                       #Call drawnow to update our live graph
                    #plt.pause(.000000001)                     # Pause Briefly. Important to keep drawnow from crashing

                    if(data_row_sample >= 50):                            #If you have 50 or more points, delete the first one from the array
                        self.microvolts = []
                        self.samples = []
                        data_row_sample = 0

                    data_row_sample += 1
                    ser.flushInput()
                    ser.flushOutput()
                    #time.sleep(0.000001)
    
    def makeFig(self): # Create a function that makes our desired plot
        plt.title('My Live Streaming Sensor Data')             # Plot the title
        #plt.plot(np.random.randn(100), np.random.randn(100))
        # plt.plot(self.samples, self.microvolts, '-')       # plot the temperature
        # plt.axes([0, 50, 0, 2500])
        # plt.legend(loc='upper left')                           # plot the legend
        # plt.show()
        plt.mpl_connect('close_event', handle_close)
        plt.plot(self.samples, self.microvolts, '-')
        plt.axis([0, 50, 0, 100])
        plt.show()

    def handle_close(self, evt):
        evt.canvas.figure.axes[0].has_been_closed = True
        print ('Closed Figure')

def main():
    ppg = Arduino()
    ppg.read_from_ppg()

if __name__ == "__main__":
    main()
    