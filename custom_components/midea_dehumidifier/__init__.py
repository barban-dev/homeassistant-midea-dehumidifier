"""
Custom integation based on humidifer and sensor platforms for EVA II PRO WiFi Smart Dehumidifier appliance by Midea/Inventor.
For more details please refer to the documentation at
https://github.com/barban-dev/midea_inventor_dehumidifier
"""
VERSION = '1.0.0'

DOMAIN = "midea_dehumidifier"
MIDEA_API_CLIENT = "midea_api_client"
MIDEA_TARGET_DEVICE = "midea_target_device"


import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import load_platform
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

import asyncio
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

CONF_SHA256_PASSWORD = 'sha256password'
CONF_DEVICEID = 'deviceId'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_SHA256_PASSWORD): cv.string,
        vol.Optional(CONF_DEVICEID): cv.string
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Set up client for Midea API based on configuration entries."""
    _LOGGER.info("midea_dehumidifier: initializing platform...")
    _LOGGER.debug("midea_dehumidifier: starting async_setup")

    if DOMAIN not in config:
        _LOGGER.error("midea_dehumi: cannot find midea_dehumi platform on configuration.yaml")
        return False

    from midea_inventor_lib import MideaClient
    	
    username = config[DOMAIN].get(CONF_USERNAME)
    password = config[DOMAIN].get(CONF_PASSWORD)
    sha256password = config[DOMAIN].get(CONF_SHA256_PASSWORD)
    deviceId = config[DOMAIN].get(CONF_DEVICEID)
	
    #_LOGGER.debug("midea_dehumi: CONFIG PARAMS: username=%s, password=%s, sha256password=%s, deviceId=%s", username, password, sha256password, deviceId)

    if not password and not sha256password:
        _LOGGER.error("midea_dehumi: either plain-text password or password's sha256 hash should be specified in config entries.")
        return False

    #Create client
    client = MideaClient(username, password, sha256password)

    #Log-in to the Midea cloud Web Service and get the list of configured Midea/Inventor appliances for the user.
    _LOGGER.info("midea_dehumi: logging into Midea API Web Service...")

    #res = client.login()
    res = await hass.async_add_executor_job(client.login)
    if res == -1:
        _LOGGER.error("midea-dehumi: login error")
        return False
    else:
        sessionId = client.current["sessionId"]
        _LOGGER.info("midea-dehumi: login success, sessionId=%s", sessionId)

    appliances = {}

    #appliances = client.listAppliances()
    appliances = await hass.async_add_executor_job(client.listAppliances)
    
    appliancesStr = ""
    for a in appliances:
        appliancesStr = "[id="+a["id"]+" type="+a["type"]+" name="+a["name"]+"]"
    if a["onlineStatus"] == "1":
        appliancesStr += " is online,"
    else:
        appliancesStr += " is offline,"
    if a["activeStatus"] == "1":
        appliancesStr += " is active.\n"
    else:
        appliancesStr += " is not active.\n"
		
    _LOGGER.info("midea-dehumi: "+appliancesStr)
    
    #The first appliance having type="0xA1" is returned for default (TODO: otherwise, 'deviceId' configuration option can be used)
    targetDevice = None
    if not deviceId:
        if appliances is not None:
            for a in appliances:
                if a["type"] == "0xA1":
                    deviceId = str(a["id"])
                    targetDevice = a
    else:
        if appliances is not None:
            for a in appliances:
                if a["type"] == "0xA1" and deviceID == str(a["id"]):
                    targetDevice = a


    if targetDevice:
        _LOGGER.info("midea-dehumidifier: device type 0xA1 found.")

        hass.data[MIDEA_API_CLIENT] = client
        _LOGGER.info("midea-dehumidifier: loading humidifier entity sub-component...")
        load_platform(hass, 'humidifier', DOMAIN, {MIDEA_TARGET_DEVICE: targetDevice}, config)

        _LOGGER.info("midea-dehumidifier: loading sensor entity sub-component...")
        load_platform(hass, 'sensor', DOMAIN, {MIDEA_TARGET_DEVICE: targetDevice}, config)

        _LOGGER.info("midea_dehumidifier: platform successfuly initialized.")
        return True
    else:
        _LOGGER.error("midea-dehumidifier: device type 0xA1 not found.")
        return False
