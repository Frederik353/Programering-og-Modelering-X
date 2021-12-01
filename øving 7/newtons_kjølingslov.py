from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import csv


class System():

    def __init__(self, initT = None, volume = None, r = None, tEnv = None, tEnd = None, dT= None):
        self.initT = initT
        self.volume= volume
        self.r = r
        self.tEnv = tEnv
        self.tEnd =tEnd
        self.dT = dT


    def getSystem(self):
        print ("#System state")
        print ("init : ", self.initT)
        print ("volume:", self.volume)
        print ("r :    ", self.r)
        print ("tEnv : ", self.tEnv)
        print ("tEnd : ", self.tEnd)
        print ("dT   : ", self.dT)


    def setInit(self, t=None):
        self.initT = t


    def roundInit(self):
        return round(self.initT,2)


    def updateState(self):
        T = self.initT
        T += -self.r*(T -self.tEnv)*self.dT
        return self.setInit(t=T)

def main():

    # start the process
    initT = 27
    coffee = System(initT=initT, volume=1,r=0.2, tEnv=-13, tEnd=3, dT=3)

    ## follow the process
    x = [0]; y = [initT];
    for i in range(1, 11):
        coffee.updateState()
        x.append(i)
        y.append(coffee.roundInit())


    data = []

    with open("./temperature_10min.txt" , "r" ) as f:
        for element in f:
            data.append(int(element))
        data = np.array(data)

    t = np.array(range(0, len(data)))/ 60

    plt.plot(t,data, c="red", label="Temperatur")
    plt.xlabel("Tid [min]", fontsize = 16)
    plt.ylabel("Temperatur [\u00b0C]", fontsize = 16)
    plt.title("Temperatur fall etter lagt i fryser", fontsize = 16)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Temperatureplot.png", dpi = 300)

    plt.plot(x,y,'-r',label='Total', linewidth=2.5)
    plt.title("Coolling coffee model")
    plt.xlabel("Time, min.")
    plt.ylabel("Temperature, Celcius deg..")
    plt.legend(loc='best')
    plt.grid(b=True, linewidth=0.5)
    plt.show()


    data = [['Time', 'Temperture']]
    for row in range(len(x)):
        data.append([x[row],y[row]])

    with open('coolingCoffeModel/cooling_coffee_model.csv', 'w') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)
        f.close()

main()

