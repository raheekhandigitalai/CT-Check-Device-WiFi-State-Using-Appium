import requests
import json
import configparser

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = configparser.ConfigParser()
config.read('config.properties')


def get_device_list():

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % get_access_key()
    }

    response = requests.request('GET',
                                get_cloud_url() + get_devices_end_point(),
                                headers=headers,
                                verify=False,
                                timeout=120)

    device_id = get_json_values_from_response_content('id', response.content)
    device_os = get_json_values_from_response_content('deviceOs', response.content)
    device_status = get_json_values_from_response_content('displayStatus', response.content)
    device_name = get_json_values_from_response_content('deviceName', response.content)
    device_udid = get_json_values_from_response_content('udid', response.content)

    combined_list = []

    for i in range(len(device_status)):
        combined_list.append(str(device_id[i]) + ' | ' + device_os[i] + ' | ' + device_status[i] + ' | ' + device_name[i] + ' | ' + device_udid[i])

    return combined_list


def get_device_property(serial_number, property_value):
    end_url = get_cloud_url() + get_devices_end_point() + "?query=@serialnumber='%s'" % serial_number

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % get_access_key()
    }

    response = requests.request('GET',
                                end_url,
                                headers=headers,
                                verify=False)

    value = get_json_value_from_response_content(property_value, response.content)
    return value


def remove_all_device_tags(device_id):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % get_access_key()
    }

    response = requests.request('DELETE',
                                get_cloud_url() + get_devices_end_point() + '/%s/tags' % device_id,
                                headers=headers,
                                verify=False)

    if response.status_code == 200:
        logger(
            'Python Script (function: remove_all_device_tags) - Successfully removed all device tags from device, '
            'response output: %s' % response.text)
    else:
        logger(
            'Python Script (function: remove_all_device_tags) - Unable to remove device tags from device, '
            'response output: %s' % response.text)

    return response


def add_device_tag(device_id, tag_value):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % get_access_key()
    }

    response = requests.request('PUT',
                                get_cloud_url() + get_devices_end_point() + '/' + device_id + '/tags/' + tag_value,
                                headers=headers,
                                verify=False)

    if response.status_code == 200:
        logger(
            'Python Script (function: add_device_tag) - Successfully added device tag to device, response output: %s' % response.text)
        logger('Python Script (function: add_device_tag) - Device Tag Added: %s' % tag_value)
    else:
        logger(
            'Python Script (function: add_device_tag) - Unable to add device tag to device, response output: %s' % response.text)

    return response


def get_device_tags(device_id):
    # GET /api/v1/devices/{id}/tags
    return 0


def get_json_values_from_response_content(value, response_content):
    response_list = []
    try:
        data = json.loads(response_content)
        for i in range(len(data['data'])):
            response_list.append(data['data'][i]['%s' % value])
    except Exception as e:
        print(e)
    return response_list


def get_json_value_from_response_content(value, response_content):
    data = json.loads(response_content)
    return_value = data['data'][0]['%s' % value]
    return return_value


def write_to_file(file_name, items):
    with open(file_name, 'w') as f:
        for item in items:
            f.write("%s\n" % item)


def logger(message):
    print(message)


# Re-usable method for waiting on element to be present
def wait_for_element_to_be_present(driver, xpath):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, xpath)))


# Re-usable method for waiting on element to be present and then click
def wait_for_element_to_be_present_and_click(driver, xpath):
    driver.wait_for_element_to_be_present(driver, xpath)
    driver.find_element(By.XPATH, xpath).click()


# Re-usable method to get text from element
def get_text_from_element(driver, xpath):
    value = driver.find_element(By.XPATH, xpath).text
    return value


# Re-usable method for getting elements in a list format
def find_elements(driver, xpath):
    items = driver.find_elements(By.XPATH, xpath)
    return items


# Re-usable method to click on element if found, else swipe and click
def click_element_else_swipe_and_click(driver, xpath, start_offset):
    try:
        if driver.find_element(By.XPATH, xpath).is_displayed():
            driver.find_element(By.XPATH, xpath).click()
    except:
        driver.execute_script("seetest:client.swipeWhileNotFound(\"DOWN\"," + str(start_offset) +
                              ", 1000, \"NATIVE\", \"xpath=" + xpath + "\", 0, 1500, 2, true)")


def get_access_key():
    return config.get('seetest_authorization', 'access_key')


def get_cloud_url():
    return config.get('seetest_urls', 'cloud_url')


def get_wd_hub():
    return config.get('seetest_urls', 'wd_hub')


def get_devices_end_point():
    return config.get('seetest_urls', 'end_point')

