import sys
import unittest
import configparser

import helpers
import Locators
from helpers import logger

from appium import webdriver
from selenium.webdriver import DesiredCapabilities

# config.properties reader
config = configparser.ConfigParser()
config.read('config.properties')

# Pre-defining the Android Capabilities as this Class is designed for Android only
capabilities = DesiredCapabilities.ANDROID


class CheckDeviceWiFiStateAndroid(unittest.TestCase):

    def setUp(self, udid):
        # Capabilities for the session
        capabilities['testName'] = 'Check Device WiFi State'
        capabilities['accessKey'] = '%s' % helpers.get_access_key()
        capabilities['udid'] = '%s' % udid
        capabilities['platformName'] = 'Android'
        capabilities['generateReport'] = False  # Disable report creation, will help to reduce execution time

        self.driver = webdriver.Remote(desired_capabilities=capabilities,
                                       command_executor=helpers.get_cloud_url() + helpers.get_wd_hub())

    def test_wifi_connection(self):
        # Storing device Serial Number to variable
        device_udid = self.driver.capabilities['udid']

        # Retrieving Device ID from SeeTest Cloud with an API call
        device_id = helpers.get_device_property(device_udid, 'id')

        # Retrieving manufacturer information from SeeTest Cloud using an API call
        device_manufacturer = helpers.get_device_property(device_udid, 'manufacturer')

        # Retrieving category information from SeeTest Cloud using an API call
        device_category = helpers.get_device_property(device_udid, 'deviceCategory')

        # Retrieving OS Version information from SeeTest Cloud using an API call
        device_os_version = helpers.get_device_property(device_udid, 'osVersion')

        # logger('device udid : %s' % device_udid)
        # logger('device id : %s' % device_id)
        # logger('device manufacturer : %s' % device_manufacturer)
        # logger('device category : %s' % device_category)
        # logger('device os version : %s' % device_os_version)

        # If device is not a Samsung device, end script. Only supporting Samsung to begin with
        if 'samsung' not in device_manufacturer:
            logger('Device manufacturer is : %s . Currently only supporting Samsung. Exiting Script.' % device_manufacturer)
            self.tearDown()
            sys.exit()

        # If Device OS is 5, the UI logic is different, exit test (Not yet implemented)
        if '5' in device_os_version:
            logger('Device OS Version is Android 5. Only supporting Android 8 and above. Exiting Script.')
            self.tearDown()
            sys.exit()
        # If Device OS is 6, the UI logic is different, exit test (Not yet implemented)
        elif '6' in device_os_version:
            logger('Device OS Version is Android 6. Only supporting Android 8 and above. Exiting Script.')
            self.tearDown()
            sys.exit()
        # If Device OS is 7, the UI logic is different, exit test (Not yet implemented)
        elif '7' in device_os_version:
            logger('Device OS Version is Android 7. Only supporting Android 8 and above. Exiting Script.')
            self.tearDown()
            sys.exit()
        # Script will work on Android 8, but Settings App has different Activity Name. Launch accordingly
        elif '8' in device_os_version:
            self.driver.execute_script("seetest:client.launch(\"com.android.settings/.Settings\", \"false\", \"true\")")
        # Script will work on Android 9, but Settings App has different Activity Name. Launch accordingly
        elif '9' in device_os_version:
            self.driver.execute_script("seetest:client.launch(\"com.android.settings/.Settings\", \"false\", \"true\")")
        # Script will work on Android 10 and above, but Settings App has different Activity Name. Launch accordingly
        else:
            self.driver.execute_script("seetest:client.launch(\"com.android.settings/.homepage.SettingsHomepageActivity\", \"false\", \"true\")")

        if 'TABLET' in device_category:
            logger('device is TABLET category. Not properly tested yet. Will try to run test.')

        # Wait for element to be present before interacting
        helpers.wait_for_element_to_be_present(self.driver, Locators.android_connections_xpath)
        helpers.click_on_element(self.driver, Locators.android_connections_xpath)

        # Storing Wi-Fi Connection in text format
        helpers.wait_for_element_to_be_present(self.driver, Locators.android_wifi_xpath)
        wifi_label = helpers.get_text_from_element(self.driver, Locators.android_wifi_xpath)
        logger(wifi_label)

        # Check if the desired Wi-Fi name is present in the connected Wi-Fi
        if config.get('wifi', 'wifi_name') in wifi_label:
            logger('Python Script (logger) - Connected to correct Wi-Fi: %s' % wifi_label)
            # remove all device tags with an API call
            helpers.remove_all_device_tags(device_id)
            # add custom device tag with an API call
            helpers.add_device_tag(device_id, config.get('tags', 'good_tag_value'))
        else:
            logger('Python Script (logger) - Not Connected to correct Wi-Fi. Current Wi-Fi: %s' % wifi_label)
            # remove all device tags with an API call
            helpers.remove_all_device_tags(device_id)
            # add custom device tag with an API call
            helpers.add_device_tag(device_id, config.get('tags', 'bad_tag_value'))

    def tearDown(self):
        # Ending the device reservation session
        self.driver.quit()


# Helps run the test using unittest framework
runner = unittest.TextTestRunner()
suite = unittest.TestLoader().loadTestsFromTestCase(CheckDeviceWiFiStateAndroid)
