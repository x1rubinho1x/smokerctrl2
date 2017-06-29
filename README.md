# smokerctrl2
Raspberry Pi PID temperature controller for electric BBQ smokers written in Python

For smokers of the style sold by:-
* [GEM Smokers](https://www.gemsmokers.co.uk/product/gem-2-tier-electric-smoker/)
* [Alfresco Cooking Company](https://www.alfrescocookingcompany.co.uk/product-page/copy-of-electric-smoker-1100w)

## Why and how?
After purchasing a GEM two tier smoker from a food show I wanted to use it to make Texas style low-and-slow smoked BBQ.  Out of the box, these smokers are not suitable for this as left unchecked they will easily reach >250°C which is easily double what is needed for good BBQ.  First I tried a pulled pork and controlled the temperature by periodically turning the mains on and off.  This was tiresome for 6 hours and the temperature control was terrible.  However the meat came out tasty at the end.  I thought then about automating the process and smokerctrl was born.  

The first attempt was a bang-bang controller which worked significantly better than manual intervention but, due to the very slow response time of the system, there was lots of over-/under-shoot and the temperature was really only controlled within a 20°C window.  This first version just had a command line interface and logged to a .CSV file so you could analyse the smoke data after the event but not live.  

The next effort, smokerctrl2, was started to try to implement a PID (Proportional-Integral-Differential) controller.  Initially this was worse until I realised due to the slow response the P- and I-terms needed to be quite small but the D-term needed to be very large.  I tacked on a web interface in [flask](http://flask.pocoo.org/) and used [Highcharts](https://www.highcharts.com/) to plot the data as it ran.  This controlled the temperature very well; within +/-5°C most of the time.  It uses a 5s period slow PWM (pulse width modulation) signal to control the heating element and because I didn't want to mess with mains electricity it turns the element on and off using an 433MHz RF switch meaning the Raspberry Pi and low voltage electronics goes nowhere near 240VAC.  

I have cooked pulled-pork and brisket very successfully achieving a decent bark, visible smoke ring and an authentic smoky flavour.  A 3kg piece of brisket point smokes in about 6 hours.  

## Hardware
* [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
* [Remote Controlled Mains Switch](http://www.maplin.co.uk/p/remote-controlled-mains-sockets-set-3-pack-n79ka).  Set to group III switch 2.  
* [433MHz RF transmitter](http://www.instructables.com/id/Super-Simple-Raspberry-Pi-433MHz-Home-Automation/)

## External Dependencies
The following external libraries are required for smokerctrl2 to run:-
* flask
* rc-switch
* pi_switch
* WiringPi
* Adafruit_GPIO.SPI
* Adafruit_MCP3008

## Running
`sudo python ./smokerctrl2.py`
Needs to be run sudo in order for WiringPi to be able to set up the GPIO pins.  

## Terminating
`CTRL+Z`
`./killit`

## Web Interface
http://[address of Pi]:5000/

* Start - starts control system
* Stop - pauses control system, terminate as above after Stopping

## Temperature Sensors
* Smoker Temperature: [ETI 810-076 DOT / ChefAlarm oven probe and clip](https://thermometer.co.uk/probes-leads-fittings/1186-dot-oven-probe-and-clip.html?search_query=%09810-076&results=1)
* Meat Temperature: [ETO 810-071 DOT / ChefAlarm penetration probe](https://thermometer.co.uk/probes-leads-fittings/1100-dot-chefalarm-penetration-probe.html?search_query=%09810-071+%09+&results=3)

## Circuit
Schematic is in TinyCAD format and generated parts list is correct.  My first attempt I built on breadboard but then I made it more permanent on a [Adafruit Perma-Proto HAT for Pi Mini Kit](https://www.adafruit.com/product/2310)

## Disclaimer
I am not affiliated with any distributors or manufacturers of electric smokers.  
This project is not approved or authorised.  Use at your own risk.
