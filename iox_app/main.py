#!/usr/bin python

import os
import time
from alerts.spark import SparkRoomAlert
from alerts.local import PrintAlertClass
from sensors.motionarduino import MotionArduino
from ConfigParser import SafeConfigParser

def load_config():
    # Get hold of the configuration file (package_config.ini)
    moduledir = os.path.abspath(os.path.dirname(__file__))
    BASEDIR = os.getenv("CAF_APP_PATH", moduledir)

    # If we are not running with CAF, use the BASEDIR to get cfg file
    tcfg = os.path.join(BASEDIR, "package_config.ini")

    CONFIG_FILE = os.getenv("CAF_APP_CONFIG_FILE", tcfg)

    cfg.read(CONFIG_FILE)

def set_alerts(sensor):
    cancontinue = False
    # This code will instantiate the Print Alert Class - Check to see if it is enabled
    if (cfg.get("print", "enabled") == "True"):
        print "Print Alert Enabled for output..."
        screen = PrintAlertClass()

        if (cfg.get("print", "logging") == "True"):
            screen.log = True

        sensor.add_alert(screen)
        cancontinue = True

    # This code will instantiate the Tropo Alert Class - Check to see if it is enabled
    if (cfg.get("spark", "enabled") == "True"):
        print "Spark Alert Enabled for output..."
        spark = SparkRoomAlert(cfg)

        if (cfg.get("spark", "logging") == "True"):
            spark.log = True

        sensor.add_alert(spark)
        cancontinue = True

    return cancontinue

def setup_sensor():
    if (cfg.get("motionsensor", "enabled") == "True"):
        # Instantiate Motion Sensor 1
        print "Motion Sensor 1 Enabled..."
        # Prefer the Serial Dev from CAF, otherwise Config File
        serial_dev = os.getenv("HOST_DEV1", cfg.get("motionsensor", "serial_dev"))

        # Setup new Sensor Object
        sensor = MotionArduino(serial_dev)
        if (cfg.get("motionsensor", "logging") == "True"):
            sensor.log = True
        sensor.comparedata = cfg.get("motionsensor", "compare_data")

        # Setup Alerts
        if not set_alerts(sensor):
            print "ERROR: No alerts are enabled.   Please enable at least one alert."
            exit(-1)
        return sensor
    else:
        print "ERROR: At least one sensor must be defined. Please enable at least one sensor."
        exit(-1)


if __name__ == "__main__":
    print "running"


    cfg = SafeConfigParser()
    load_config()

    location_info = {"name": cfg.get("info", "location_name"),
                     "id": cfg.get("info", "location_id"),
                     "contact email": cfg.get("info", "location_contact_email")
                     }

    sensor = setup_sensor()

    while True:
        # Let's get data from the sensor
        sensor.read()

        currentdate = time.strftime("%b %d %Y, %H:%M:%S ", time.gmtime())

        # # Check if triggered
        if sensor.triggered:
            alert_data = "# Activity Detected at %s \n" \
                         "* **Time**: %s \n" \
                         "* **Sensor:** %s \n" \
                         "* **Data:** %s \n" \
                         % (location_info["name"], currentdate, sensor.data["Sensor"], sensor.data["Desc"])

            sensor.send_alerts(alert_data)

        # Sleep for an appropriate time
        time.sleep(2)


