import logging
import threading
import appium_script
import helpers


def start_appium_script(name, device_udid):
    logging.info("Thread %s: starting", name)
    # Instantiating the Appium Script Class
    appium_methods = appium_script.CheckDeviceWiFiState()

    try:
        # Setting up Appium Session using Device ID
        appium_methods.setUp(device_udid)
        # Running the Appium Script itself
        appium_methods.test_wifi_connection_dummy()
        # Tearing down the Appium Session once done
        appium_methods.tearDown()
    except Exception as e:
        # If Script fails for some reason, making sure Appium Session still ends and doesn't leave sessions hanging
        appium_methods.tearDown()
        raise Exception(e)

    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # Gets list of all Devices in the SeeTest Cloud
    devices_list = helpers.get_device_list()

    threads = list()
    for index in range(len(devices_list)):
        # Splits the device properties: 0 is Device ID, 1 is Device OS, 2 is Status, 3 is Device Name, 4 is Device UDID
        device_property = devices_list[index].split('|')
        # Checks if device is in Available state first
        if 'Available' in devices_list[index]:
            # If device OS is iOS, only then run (As script is only developed for iOS now)
            if 'iOS' in device_property[1]:
                logging.info("Main    : create and start thread %d.", index)
                x = threading.Thread(target=start_appium_script, args=(index, device_property[4].strip()))
                threads.append(x)
                x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
