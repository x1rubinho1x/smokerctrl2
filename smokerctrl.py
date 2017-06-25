import os
import time
import math
from flask import Flask, render_template
from threading import Thread, Event, Timer
from movingaverage import MovingAverage
from PID import PID
import pi_switch

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

ctrlevent = Event()

smokertemptarget = 107.0

smokerpid = PID(10.0, 0.01, 200.0, smokertemptarget)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

VREF = 3.3
ADCTOVOLTS = 1023.0

smokertempadcchannel = 3
smokertempR2 = 10000.0

smokertempA = -0.183608851e-3
smokertempB = 3.575173627e-4
smokertempC = -3.548314967e-7

meattempadcchannel = 4
meattempR2 = 10000.0

meattempA = -0.7547494631e-3
meattempB = 4.444103914e-4
meattempC = -6.343963549e-7

zerokelvin = -273.15

meattemptarget = 95

# rc-switch setup - must be run sudo
SWITCHTXPIN = 3
SWITCHGROUP = 3
SWITCHID = 2
switch = pi_switch.RCSwitchB(SWITCHGROUP, SWITCHID)
switch.enableTransmit(SWITCHTXPIN)

def temp_celcius(A, B, C, resistance):
    """Steinhart-Hart equation"""
    tempkelvin = 1.0 / (A + B * math.log(resistance) + C * pow(math.log(resistance), 3))
    return(tempkelvin + zerokelvin)

def adc_voltage(adccounts):
    """Convert ADC counts to voltage"""
    if adccounts < 1:
        adccounts = 1
    return (float((adccounts * VREF) / ADCTOVOLTS))

def adc_resistance(adc_voltage, ref_resistance):
    """Calculate potential divider resistance"""
    resitance = ref_resistance * ((VREF/adc_voltage) - 1.0)
    return (resitance)

smokertempavg = MovingAverage(100)
meattempavg = MovingAverage(100)

dutycycle = 0
ontime = 0

heateron = False

timedata = []
smokertempdata = []
meattempdata = []
ontimedata = []

def ctrlfunc():
    quickcounter = 0
    slowcounter = 0

    smokerpid.setSampleTime(5.0)
    smokerpid.setSetPoint(110.0)

    global dutycycle
    global ontime
    global heateron

    while (1):
        # start/stop lock
        ctrlevent.wait()

        starttime = time.time()
        quickcounter = quickcounter + 1
        slowcounter = slowcounter + 1

        # Read all the ADC channel values
        smokertempadc = mcp.read_adc(smokertempadcchannel)
        meattempadc = mcp.read_adc(meattempadcchannel)

        # Calculate smoker temp
        smokertempvoltage = adc_voltage(smokertempadc)
        smokertempresistance = adc_resistance(smokertempvoltage, smokertempR2)
        smokertempcelcius = temp_celcius(smokertempA, smokertempB, smokertempC, smokertempresistance)
        smokertempavg.movingaveragecalc(smokertempcelcius)

        # Calculate meat temp
        meattempvoltage = adc_voltage(meattempadc)
        meattempresistance = adc_resistance(meattempvoltage, meattempR2)
        meattempcelcius = temp_celcius(meattempA, meattempB, meattempC, meattempresistance)
        meattempavg.movingaveragecalc(meattempcelcius)

        if quickcounter == 10:
            # do 1s things
##            timedata.append(round((time.time() - time.altzone)* 1000, 0))
##            smokertempdata.append(round(smokertempavg.movingaverage, 2))
##            meattempdata.append(round(meattempavg.movingaverage, 2))
##            ontimedata.append(round(ontime, 2))

            quickcounter = 0


        if slowcounter == 50:
            # do 5s things
            smokerpid.update(smokertempavg.movingaverage)
            dutycycle = max(min(smokerpid.output, 100),0)
            ontime = 50 * (dutycycle / 100)
            if meattempavg.movingaverage >= meattemptarget:
                smokerpid.setSetPoint(meattemptarget)

            if ontime > 0 and ontime < 10:
                ontime = 10

            if ontime > 90 and ontime < 100:
                ontime = 100

            timedata.append(round((time.time() - time.altzone)* 1000, 0))
            smokertempdata.append(round(smokertempavg.movingaverage, 2))
            meattempdata.append(round(meattempavg.movingaverage, 2))
            ontimedata.append(round(ontime, 2))

            slowcounter = 0

        if slowcounter < ontime and heateron == False:
            switch.switchOn()
            heateron = True

        if slowcounter > ontime and heateron == True:
            switch.switchOff()
            heateron = False

        endtime = time.time()
        sleeptime = 0.1 - (endtime - starttime)
        if sleeptime < 0:
            sleeptime = 0
        time.sleep(sleeptime)


app = Flask(__name__)
ctrlthread = Thread(group = None, target = ctrlfunc)

@app.route('/')
def webindex():
    timestamp = time.strftime("%c", time.localtime())

    smokerdatastring = "["
    meatdatastring = "["
    ontimedatastring = "["
    for i, item in enumerate(timedata):
        smokerdatastring += "["
        smokerdatastring += str(timedata[i])
        smokerdatastring += ","
        smokerdatastring += str(smokertempdata[i])
        smokerdatastring += "],"
        meatdatastring += "["
        meatdatastring += str(timedata[i])
        meatdatastring += ","
        meatdatastring += str(meattempdata[i])
        meatdatastring += "],"
        ontimedatastring += "["
        ontimedatastring += str(timedata[i])
        ontimedatastring += ","
        ontimedatastring += str(ontimedata[i])
        ontimedatastring += "],"
    smokerdatastring = smokerdatastring[:-1] + "]"
    meatdatastring = meatdatastring[:-1] + "]"
    ontimedatastring = ontimedatastring[:-1] + "]"

    #print (smokerdatastring)

    return render_template('index.html',
                           timestamp = timestamp,
                           smokertemp = round(smokertempavg.movingaverage, 1),
                           meattemp = round(meattempavg.movingaverage,1),
                           heaterstate = heateron,
                           set_point = smokerpid.SetPoint,
                           Kp = smokerpid.Kp,
                           Ki = smokerpid.Ki,
                           Kd = smokerpid.Kd,
                           PTerm = round(smokerpid.PTerm, 2),
                           ITerm = round(smokerpid.ITerm, 2),
                           DTerm = round(smokerpid.DTerm, 2),
                           output = round(smokerpid.output, 2),
                           ontime = round(ontime,0),
                           smokerdatastring = smokerdatastring,
                           meatdatastring = meatdatastring,
                           ontimedatastring = ontimedatastring,
                           meattemptarget = round(meattemptarget, 2))

@app.route('/start')
def webstart():
    ctrlevent.set()
    return render_template('start.html')

@app.route('/stop')
def webstop():
    global heateron
    global ontime
    smokertempavg.reset()
    meattempavg.reset()
    ontime = 0
    heateron = False
    switch.switchOff()
    smokerpid.clear()
    smokerpid.setSetPoint(50.0)
    ctrlevent.clear()
    return render_template('stop.html')

# Main function
if __name__ == "__main__":
    ctrlthread.daemon = False
    ctrlthread.start()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0")
