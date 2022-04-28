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

# Pre-defining the Android Capabilities as this Class is designed for iOS only
capabilities = DesiredCapabilities.IPHONE


class CheckDeviceWiFiStateiOS(unittest.TestCase):

    def setUp(self, udid):
        # Capabilities for the session
        capabilities['testName'] = 'Check Device WiFi State'
        capabilities['accessKey'] = '%s' % helpers.get_access_key()
        capabilities['udid'] = '%s' % udid
        capabilities['platformName'] = 'iOS'
        capabilities['autoDismissAlerts'] = True  # This helps to handle unexpected native pop-ups
        capabilities['generateReport'] = False  # Disable report creation, will help to reduce execution time
        capabilities['bundleId'] = 'com.apple.Preferences'

        self.driver = webdriver.Remote(desired_capabilities=capabilities,
                                       command_executor=helpers.get_cloud_url() + helpers.get_wd_hub())

    def test_wifi_connection(self):
        # Storing device Serial Number to variable
        device_udid = self.driver.capabilities['udid']

        # Getting Device ID from SeeTestCloud with an API call
        device_id = helpers.get_device_property(device_udid, 'id')

        # Wait for element to be present before interacting
        helpers.wait_for_element_to_be_present(self.driver, Locators.ios_wifi_xpath)

        # Storing Wi-Fi Connection in text format
        wifi_label = helpers.get_text_from_element(self.driver, Locators.ios_wifi_xpath)
        logger(wifi_label)

        # Check if the desired Wi-Fi name is present in the connected Wi-Fi
        if config.get('wifi', 'wifi_name') in wifi_label:
            logger('Python Script (logger) - Connected to correct Wi-Fi: %s' % wifi_label)
            # remove all device tags with an API call
            helpers.remove_all_device_tags(device_id)
            # add custom device tag with an API call
            helpers.add_device_tag(device_id, config.get('tags', 'good_tag_value'))
        else:
            logger('Python Script (logger) - Not Connected to correct Wi-Fi: %s' % wifi_label)
            # remove all device tags with an API call
            helpers.remove_all_device_tags(device_id)
            # add custom device tag with an API call
            helpers.add_device_tag(device_id, config.get('tags', 'bad_tag_value'))

    def tearDown(self):
        # Ending the device reservation session
        self.driver.quit()


# Helps run the test using unittest framework
runner = unittest.TextTestRunner()
suite = unittest.TestLoader().loadTestsFromTestCase(CheckDeviceWiFiStateiOS)
