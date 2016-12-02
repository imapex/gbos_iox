from sensors.base import GenericSensorClass
import serial
import logging
import json

class MotionArduino(GenericSensorClass):

    def __init__(self, serial_dev):

        self.data = 0
        self.active = False
        self.triggered = False

        super(MotionArduino, self).__init__()

        # Set Serial Parameters
        # serial_dev = "/dev/cu.usbmodem1421"
        # if serial_dev is None:
        #     serial_dev = "/dev/cu.usbserial"

        self.sdev = serial.Serial(port=serial_dev, baudrate=9600)
        self.sdev.bytesize = serial.EIGHTBITS  # number of bits per bytes
        self.sdev.parity = serial.PARITY_NONE  # set parity check: no parity
        self.sdev.stopbits = serial.STOPBITS_ONE  # number of stop bits
        self.sdev.timeout = 5

    def read(self):
        """
        read - This method will read data from the sensor
        :return: nothing
        """
        # Execute any method in the base class prior to this method
        super(MotionArduino,self).read()

        if self.sdev.inWaiting() > 0:
            if self._log:
                logging.warning("Incoming Data Found")

            inc = self.sdev.readline()[:-2]
            # print(inc)
            value = json.loads(inc)

            current_active = value["Value"]

            self.data = value

            if current_active == self.active:
                self.triggered = False
            else:
                self.triggered = True
                self.active = current_active
        else:
            self.triggered = False

        if self._log:
            logging.warning("Sensor read #"+ str(self._totalcount) + ", Data returned: "+str(self.data))
        # sdev.close()
        return

    def compare(self, value):
        """
        This method will compare the retrieved sensor data with the value.
        If the value is less that data then this data returns true otherwise
        will be false.

        :param value: int value to compare against
        :return: bool result of comparison
        """

        if self._log:
            logging.warning("Comparing {} with {}".format(self.data, value))

        if self.data == value:
            self._sensorcount += 1
            return True
        else:
            return False