#
# aprs Weather Station for aprs using Raspberry Pi Zero and PiicoDev_BME280
#
# Phil Kern - VK5ZEY
# email: phil.kern@staff.kernwifi.com.au
# 07/11/22

import configparser
import logging
import os
import sys
import time
from datetime import datetime
from PiicoDev_BME280 import PiicoDev_BME280
import smbus2
import aprslib
from aprslib.util import latitude_to_ddm, longitude_to_ddm

bme280 = PiicoDev_BME280()
tempC, presPa, humRH = bme280.values() # read all data from the sensor
pres_hPa = presPa / 100 # convert air pressure Pascals -> hPa (or mbar, if you prefer)
tempCF = round((tempC*9/5) +32, 2)
humiRH = humRH

tempC_str = "{:.1f}".format(tempC)
presPa_str = "{:.1f}".format(presPa/100)
humRH_str = "{:.1f}".format(humRH)
    
CONFIG_FILE = 'aprs_wx.conf'

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def make_aprs_wx(wind_dir=None, wind_speed=None, wind_gust=None, temperature=None,
                 rain_last_hr=None, rain_last_24_hrs=None, rain_since_midnight=None,
                 humidity=None, pressure=None, position=False):
    wx_fmt = lambda n, l=3: '.' * l if n is None else "{:0{l}d}".format(int(n), l=l)
    if position == True:
        template = '{}/{}g{}t{}r{}p{}P{}h{}b{}'.format
    else:
        template = 'c{}s{}g{}t{}r{}p{}P{}h{}b{}'.format

    return template(wx_fmt(wind_dir),
                    wx_fmt(wind_speed),
                    wx_fmt(wind_gust),
                    wx_fmt(temperature),
                    wx_fmt(rain_last_hr),
                    wx_fmt(rain_last_24_hrs),
                    wx_fmt(rain_since_midnight),
                    wx_fmt(humidity, 2),
                    wx_fmt(pressure, 5))


def connect(call, password):
    ais = aprslib.IS(call, passwd=password, port=14580)
    for retry in range(5):
        try:
            ais.connect()
        except ConnectionError as err:
            logging.warning(err)
            time.sleep(5 * retry)
        else:
            return ais
        raise IOError('Connection Failed')

def main():
    logging.info('Read config file %s', CONFIG_FILE)
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        call = config.get('APRS', 'call')
        passcode = config.get('APRS', 'passcode')
        lat = config.getfloat('APRS', 'latitude', fallback=0.0)
        lon = config.getfloat('APRS', 'longitude', fallback=0.0)
        sleep_time = config.getint('APRS', 'sleep', fallback=900)
        position = config.getboolean('APRS', 'position', fallback=False)
    except configparser.Error as err:
        logging.error(err)
        sys.exit(os.EX_CONFIG)

    logging.info('Send weather data %s position', 'with' if position else 'without')
   
    BME280 = PiicoDev_BME280()
    
    while True:
        try:
            print("")
            print("PiicoDev_BME280 Sensor Readings:")
            print(str(tempC)+" °C  " + str(pres_hPa)+" hPa  " + str(humRH)+" % RH")
            print("")
            
            bme280_data = PiicoDev_BME280()
           
            logging.info('After bme280 call %s', bme280_data)
            if (bme280_data) is None:
                logging.debug("No reading from sensor")
                break;
            
            logging.info('Ambient temperature %f',tempCF)
            logging.info('Pressure %s', presPa)
            logging.info('Humidity %s', humRH)
            ais = connect(call, passcode)
            
            weather = make_aprs_wx(temperature=tempCF, pressure=presPa, humidity=humRH, position=position)
            if position:
                ais.sendall("{}>APRS,TCPIP*:={}/{}_{}X".format(call, latitude_to_ddm(lat), longitude_to_ddm(lon),weather))
            else:
                _date = datetime.utcnow().strftime('%m%d%H%M')
                ais.sendall("{}>APRS,TCPIP*:_{}{}".format(call, _date, weather))
            ais.close()
        except IOError as err:
            logging.error(err)
            sys.exit(os.EX_IOERR)
        except Exception as err:
            logging.error(err)

        time.sleep(sleep_time)

