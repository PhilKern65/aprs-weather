APRS (Automatic Packet Reporting System) is an amateur radio-based system for real time digital communication of information of immediate value in a local area. It is used for communicating GPS coordinates, weather station telemetry, text messages, announcements, queries and other telemetry.

Data is ingested into an APRS -IS (APRS - Internet System), via an Internet connected receiver (iGate) and transmitted to all other stations using packet repeaters or digipeaters, using store and forward technology to retransmit packets.

With a Raspberry Pi Zero connected to a PiicoDev_BME280 sensor (see my weather station GitHub repository to learn about setup), you can generate local weather readings (temperature, pressure, humidity) and transmit local weather readings via APRS.

Steps
1.	pip install aprslib (install the aprs python library) onto your Raspberry Pi Zero.
2.	pip install piicodev (install the drivers for the PiicoDev ecosystem of sensors and modules) onto your Pi Zero. 
3.	Find the passcode associated with your Amateur Radio callsign using the below link
          https://apps.magicbug.co.uk/passcode/index.php/passcode
4.	Find your latitude, longitude using Google Maps. (use decimal format)
5.	Download and Edit the APRS config file (aprs_wx.conf) with callsign latitude, longitude (decimal format) and passcode. If you want to send your latitude, longitude along with the weather packet (good idea to do so), then set position as True.
6.	Download the python program to collect weather data from BME280, form the ARPS packet and transmit it. (vk5rkw_weather_station.py).
7.	Connect the BME280 sensor to the Raspberry Pi zero (refer to README in my weather_station repo for details).
8.	Run vk5rkw_weather_station.py (python3 vk5rkw_weather_station.py
Example output:

INFO: Login successful

PiicoDev_BME280 Sensor Readings:

24.38 °C  968.0354296875 hPa  26.6796875 % RH

INFO: After bme280 call <PiicoDev_BME280.PiicoDev_BME280 object at 0xb6509a30>

INFO: Ambient temperature 75.880000

INFO: Pressure 96803.54296875

INFO: Humidity 26.6796875

INFO: Attempting connection to rotate.aprs.net:14580

INFO: Connected to ('205.233.35.46', 14580)

INFO: Sending login information

9.	Log into aprs.fi. Click on Weather data. Search with your "callsign" to confirm that weather packet has been transmitted.
