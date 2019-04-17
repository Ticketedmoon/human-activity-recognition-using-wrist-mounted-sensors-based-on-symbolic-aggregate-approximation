import serial # import Serial Library
import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *

class Arduino:

    plt.ion() #Tell matplotlib you want interactive mode to plot live data

    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.samples, self.microvolts = [], []
        self.ln = self.ax.plot(self.samples, self.microvolts, 'ro')
        plt.show()

    def read_from_ppg(self):
        with serial.Serial('COM3', 19200, bytesize=serial.EIGHTBITS, timeout=0) as ser, open("voltages.csv", 'w') as text_file:
            text_file.write("{}, {}\n".format("Samples", "Microvolts(mV)"))
            data_row_sample = 0
            while True:
                voltage_reading = str(ser.readline().decode(encoding='utf-8', errors='strict')).strip("\n").strip("\r\n")
                if (voltage_reading != "" and voltage_reading.isdigit() and float(voltage_reading) > 100):
                    data = [str(data_row_sample), voltage_reading]
                    text_file.write("{}, {}\n".format(data_row_sample, voltage_reading))
                    text_file.flush()
                    self.samples.append(float(data_row_sample))
                    self.microvolts.append(float(voltage_reading))
                    drawnow(self.makeFig)
                    #plt.pause(.000001)                     #Pause Briefly. Important to keep drawnow from crashing
                    data_row_sample += 1

                    if(data_row_sample > 25):                            #If you have 50 or more points, delete the first one from the array
                        self.samples.pop(0)                       #This allows us to just see the last 50 data points
                        self.microvolts.pop(0)

                    ser.flushInput()
                    ser.flushOutput()
    
    def makeFig(self): # Create a function that makes our desired plot
        plt.ylim(0, 2500)                           # Set limits of second y axis- adjust to readings you are getting
        plt.title('My Live Streaming Sensor Data')      # Plot the title
        plt.grid(True)                                  # Turn the grid on
        plt.ylabel('Microvolts(mV)')                    # Set ylabels
        plt.xlabel('Samples')                           # Set ylabels
        plt.plot(self.samples, self.microvolts, 'g-', label='Pulse Rate Microvolts(mV)')       #plot the temperature
        plt.legend(loc='upper left')                    

def main():
    ppg = Arduino()
    ppg.read_from_ppg()

if __name__ == "__main__":
    main()
    