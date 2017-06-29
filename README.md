# smokerctrl2
Raspberry Pi PID temperature controller for electric BBQ smokers written in Python

For smokers of the style sold by:
* [GEM Smokers](https://www.gemsmokers.co.uk/product/gem-2-tier-electric-smoker/)
* [Alfresco Cooking Company](https://www.alfrescocookingcompany.co.uk/product-page/copy-of-electric-smoker-1100w)

# Hardware
* [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
* [Remote Controlled Mains Switch](http://www.maplin.co.uk/p/remote-controlled-mains-sockets-set-3-pack-n79ka).  Set to group III switch 2.  
* [433MHz RF transmitter](http://www.instructables.com/id/Super-Simple-Raspberry-Pi-433MHz-Home-Automation/)

# External Dependencies
The following external libraries are required for smokerctrl2 to run:
* flask
* rc-switch
* pi_switch
* WiringPi
* Adafruit_GPIO.SPI
* Adafruit_MCP3008

# Running
`sudo python ./smokerctrl2.py`
Needs to be run sudo in order for WiringPi to be able to set up the GPIO pins.  

# Terminating
`CTRL+Z`
`./killit`

# Web Interface
http://[address of Pi]:5000/

* Start - starts control system
* Stop - pauses control system, terminate as above after Stopping

# Temperature Sensors
* Smoker Temperature: [ETI 810-076 DOT / ChefAlarm oven probe and clip](https://thermometer.co.uk/probes-leads-fittings/1186-dot-oven-probe-and-clip.html?search_query=%09810-076&results=1)
* Meat Temperature: [ETO 810-071 DOT / ChefAlarm penetration probe](https://thermometer.co.uk/probes-leads-fittings/1100-dot-chefalarm-penetration-probe.html?search_query=%09810-071+%09+&results=3)

# Circuit
Schematic is in TinyCAD format and generated parts list is correct.  My first attempt I built on breadboard but then I made it more permanent on a [Adafruit Perma-Proto HAT for Pi Mini Kit](https://www.adafruit.com/product/2310)

# Disclaimer
I am not affiliated with any distributors or manufacturers of electric smokers.  
This project is not approved or authorised.  Use at your own risk.
