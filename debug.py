import appium_script_android

# Debug Script for testing Android Logic
if __name__ == "__main__":
    appium_methods = appium_script_android.CheckDeviceWiFiStateAndroid()
    try:
        appium_methods.setUp('04157df46ab5ba31')
        appium_methods.test_wifi_connection()
        appium_methods.tearDown()
    except Exception as e:
        appium_methods.tearDown()
        print(e)

# TESTED ON Android 10 / 11 / 12: Note 10 / Note 20 / S9 / S10 / S20
# Android 9 and below has a different settings name: com.android.settings/.Settings instead of com.android.settings/.homepage.SettingsHomepageActivity
