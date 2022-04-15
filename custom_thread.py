from threading import Thread
import time
import appium_script

# Not using this class. Purely experimental for understanding Multi Threading better.
class CustomThread:

    def __init__(self, device_udid):
        Thread.__init__(self)
        self.device_udid = device_udid

    def run(self):
        print('Starting Appium Script on device: ', self.device_udid)
        appium_methods = appium_script.CheckDeviceWiFiState()
        try:
            appium_methods.setUp(self.device_udid)
            appium_methods.test_wifi_connection_dummy()
            appium_methods.tearDown()
        except Exception as e:
            appium_methods.tearDown()
            raise Exception(e)
        print('Finished Appium Script on device: ', self.device_udid)

