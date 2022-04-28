# XPATHs stored under this file for re-usability and clean code in WiFiScript.py

# iOS Locators

ios_wifi_xpath = "(//*[@id='Wi-Fi']//XCUIElementTypeStaticText)[2]"

# Android Locators

# Will work for S8 / S9 / S10 / S20 / Note 10 / Note 20 / Tab A - Android 8 and above
android_connections_xpath = "//android.widget.TextView[@text='Connections']"
android_wifi_xpath = "//android.widget.TextView[@text='Wi-Fi']/following-sibling::android.widget.TextView[@id='summary']"

