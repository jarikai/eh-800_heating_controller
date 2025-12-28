"""Constants for eh-800_heating_controller."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "eh_800_heating_controller"
ATTRIBUTION = "Data provided by eh-800 heating controller"
DEVICE_NAME = "Ouman EH800"
CONF_IP = "ip"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 1  # minutes
DEFAULT_IP = "192.168.1.55"

# A mapping from the key we ask the device for to an entity description.
# Add all the 30 keys you need here.
# Each entry can have: key, name, icon, device_class, unit, state_class
SENSOR_DESCRIPTIONS = {
    "S_300_85": {
        "name": "Autumn Drying Effect",
        "icon": "mdi:solar-power",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_227_85": {
        "name": "Outside Temperature",
        "icon": "mdi:home-thermometer-outline",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_321_85": {
        "name": "Fine Tunning Effect",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_90_85": {
        "name": "Big Temperature Drop L1",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_177_85": {
        "name": "Big Temperature Drop L2",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_1000_0": {
        "name": "Control Mode",
        "icon": "mdi:cog",
        "device_class": "enum",
        "state_class": "measurement",
    },
    "S_1001_0": {
        "name": "Control Mode L2",
        "icon": "mdi:cog",
        "device_class": "enum",
        "state_class": "measurement",
    },
    "S_292_85": {
        "name": "Floor Heating Effect",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_65_85": {
        "name": "Heating Curve High L1",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_152_85": {
        "name": "Heating Curve High L2",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_61_85": {
        "name": "Heating Curve Low L1",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_148_85": {
        "name": "Heating Curve Low L2",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_63_85": {
        "name": "Heating Curve Mid L1",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_150_85": {
        "name": "Heating Curve Mid L2",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_135_85": {
        "name": "Home Away Status",
        "icon": "mdi:home",
        "device_class": "enum",
        "state_class": "measurement",
    },
    "S_55_85": {
        "name": "Max Water Temp L1",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_142_85": {
        "name": "Max Water Temp L2",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_54_85": {
        "name": "Min Water Temp L1",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_141_85": {
        "name": "Min Water Temp L2",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_275_85": {
        "name": "Requested Temp L1",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_310_85": {
        "name": "Requested Temp L2",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_134_85": {
        "name": "Room Fine Tune L1",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_259_85": {
        "name": "Supply Water Temp L1",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_293_85": {
        "name": "Supply Water Temp L2",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_89_85": {
        "name": "Temp Drop L1",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_176_85": {
        "name": "Temp Drop L2",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "S_26_85": {
        "name": "Trent Sampling Interval",
        "icon": "mdi:timer-sync-outline",
        "device_class": "duration",
        "unit_of_measurement": "s",
        "state_class": "measurement",
    },
    "S_272_85": {
        "name": "Valve Position L1",
        "icon": "mdi:percent",
        "device_class": "position",
        "unit_of_measurement": "%",
        "state_class": "measurement",
    },
    "S_306_85": {
        "name": "Valve Position L2",
        "icon": "mdi:percent",
        "device_class": "position",
        "unit_of_measurement": "%",
        "state_class": "measurement",
    },
    "S_294_85": {
        "name": "Water Temp By Curve L2",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
}
