import json
import logging
import requests
from alerts.base import GenericAlertClass
from zeus import client



class CiscoZeusAlert(GenericAlertClass):
    """
    Sends alerts to a Cisco Zeus Log
    """

    def __init__(self, cfg):
        """
        Constructor method when the object is initialized

        :param cfg: Specifies the configuration file that will be used to process the data
        :return: nothing
        """
        self.cfg = cfg
        self.zeusToken = cfg.get("zeus", "token")
        self.logName = cfg.get("zeus", "log_name")
        self.logKey = cfg.get("zeus", "log_key")
        self.zeusServer = cfg.get("zeus", "url")
        self.client = client.ZeusClient(self.zeusToken, self.zeusServer)

        # Call the base class initializer
        super(CiscoZeusAlert, self).__init__()

    def post_message(self, text):
        """
        post_message - Internal function used to post the log to Cisco Zeus

        :param text - Message to be posted on the API
        :return message_dict - A Dictionary used to represent the result of the WebAPI Call
        """

        # Construct the Log Message
        payload = [{self.logKey: text}]

        if self.log:
            logging.warning("Sending Zeus Log to: " + self.zeusServer)
            logging.warning("   Log Name: "+ str(self.logName))
            logging.warning("   Payload: "+ str(payload))

        # Post the log to Zeus
        try:
            resp = self.client.sendLog(self.logName, payload)
        except:
            # if fails, try once more
            resp = self.client.sendLog(self.logName, payload)

        message_dict = {}
        message_dict['statuscode'] = str(resp[0])
        message_dict['data'] = resp[1]

        if self.log:
            logging.warning("requests Return Status Code: "+str(message_dict['statuscode']))
            logging.warning("requests Return Data: " + str(message_dict['data']))

        return message_dict

    def trigger(self, alertdata):
        """
        trigger - This method will be used to send the message

        :param alertdata: defines the message to be displayed
        :return: returns the dictionary from the resultant display
        """
        return self.post_message(alertdata)
