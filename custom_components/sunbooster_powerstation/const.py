"""Constants for Sunbooster Powerstation integration."""
DOMAIN = "sunbooster_powerstation"

CONF_PROXY_URL = "proxy_url"
CONF_CUSTOMER_KEY = "customer_key"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_PROXY_URL = "https://api.sunbooster.com"
DEFAULT_SCAN_INTERVAL = 30

# Property codes (mirrors Acceleronix TSL codes)
PROP_BATTERY = "battery_percentage"
PROP_REMAIN_TIME = "remain_time"
PROP_REMAIN_CHARGE_TIME = "remain_charging_time"
PROP_TOTAL_INPUT = "total_input_power"
PROP_TOTAL_OUTPUT = "total_output_power"
PROP_DEVICE_STATUS = "device_status"
PROP_CHARGE_POWER = "charge_mode_power_hm"
PROP_AC_OUTPUT = "ac_output_Power"
PROP_DC_OUTPUT = "dc_output_Power"
PROP_USB_OUTPUT = "usb_output_power_hm"
PROP_CHARGE_MODE = "charge_mode_data_hm"
PROP_MIG_CONNECTION = "MIG_connection_data_hm"
PROP_AC_SWITCH = "ac_switch_hm"
PROP_DC_SWITCH = "dc_switch_hm"
PROP_USB_SWITCH = "usb_switch"

CHARGE_MODE_LABELS = {"0": "off", "1": "normal", "2": "fast", "3": "silent"}

# Watt -> Acceleronix MIG enum (charge from grid)
MIG_WATT_TO_ENUM = {
    0: "0", 100: "1", 150: "2", 200: "3", 250: "4", 300: "5",
    350: "6", 400: "7", 450: "8", 500: "9", 550: "10",
    600: "11", 650: "12", 700: "13", 750: "14", 800: "15",
}
MIG_ENUM_TO_WATT = {v: k for k, v in MIG_WATT_TO_ENUM.items()}
