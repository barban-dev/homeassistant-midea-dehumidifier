"""
Custom integation based on humidifer and sensor platforms for EVA II PRO WiFi Smart Dehumidifier appliance by Midea/Inventor.
For more details please refer to the documentation at
https://github.com/barban-dev/midea_inventor_dehumidifier
"""
VERSION = '1.0.4'

import logging
from typing import List, Optional
from custom_components.midea_dehumidifier import DOMAIN, MIDEA_API_CLIENT, MIDEA_TARGET_DEVICE
from homeassistant.const import ATTR_MODE

#patch for HA2024.1.0
#from homeassistant.components.humidifier import HumidifierEntity
from homeassistant.components.humidifier import HumidifierEntity, HumidifierDeviceClass, HumidifierEntityFeature	

from homeassistant.components.humidifier.const import (
    ATTR_AVAILABLE_MODES,
    ATTR_HUMIDITY,
    ATTR_MAX_HUMIDITY,
    ATTR_MIN_HUMIDITY,
    DEFAULT_MAX_HUMIDITY,
    DEFAULT_MIN_HUMIDITY,
    #patch for HA2024.1.0
    #DEVICE_CLASS_DEHUMIDIFIER,
    SERVICE_SET_HUMIDITY,
    SERVICE_SET_MODE
    #SUPPORT_MODES
)

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import service
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send
from homeassistant.core import callback


ATTR_ENTITY_ID = "entity_id"

SERVICE_SET_FAN_SPEED = "set_fan_speed"
ATTR_FAN_SPEED = "fan_speed"
SERVICE_SET_FAN_SPEED_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.entity_id,
    vol.Required(ATTR_FAN_SPEED): cv.string,
})

SERVICE_SET_ION_STATE = "set_ion_state"
ATTR_ION_STATE = "ion_state"
SERVICE_SET_ION_STATE_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.entity_id,
    vol.Required(ATTR_ION_STATE): cv.boolean,
})

SERVICE_SET_MODE = "set_mode"
ATTR_MODE = "mode"
SERVICE_SET_MODE_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.entity_id,
    vol.Required(ATTR_MODE): cv.string,
})


_LOGGER = logging.getLogger(__name__)

#patch for HA2024.1.0
#SUPPORT_FLAGS = SUPPORT_MODES
SUPPORT_FLAGS = HumidifierEntityFeature.MODES

#TODO: in midea_dehumi python lib the range 30-70 is hard coded (fix it)
MIN_HUMITIDY = 35
MAX_HUMITIDY = 70

DEHUMI_MODES_DICT = { 'TARGET_HUMIDITY' : 1, 'CONTINUOUS' : 2, 'SMART' : 3, 'DRYER' : 4}
DEHUMI_MODES_LIST = [ 'Target_humidity', 'Continuous', 'Smart', 'Dryer']

DEHUMI_FAN_SPEED_DICT = { 'SILENT' : 40, 'MEDIUM' : 60, 'HIGH' : 80 }
DEHUMI_FAN_SPEED_LIST = [ 'Silent', 'Medium', 'High' ]


#States Attributes
ATTR_ION_SET_SWITCH = "ion"
ATTR_FAN_SPEED_MODE = "fan_speed_mode"
ATTR_CURRRENT_HUMIDITY = "current_humidity"
ATTR_TANK = "tank_show"
PROP_TO_ATTR = {
    "ionSetSwitch": ATTR_ION_SET_SWITCH,
	"mode": ATTR_MODE,
    "windSpeedMode": ATTR_FAN_SPEED_MODE,
    "windSpeed": ATTR_FAN_SPEED,
	"current_humidity": ATTR_CURRRENT_HUMIDITY,
        "tank_show": ATTR_TANK,	
}


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up Midea/Inventor dehumidifier platform based on config_entry."""
    _LOGGER.info("midea_dehumidifier: initializing humidifier platform")
    _LOGGER.debug("midea_dehumidifier: starting async_setup_platform")
    _LOGGER.debug("midea_dehumidifier: MIDEA_API_CLIENT="+MIDEA_API_CLIENT)
    _LOGGER.debug("midea_dehumidifier: MIDEA_TARGET_DEVICE="+MIDEA_TARGET_DEVICE)

    #ref: https://developers.home-assistant.io/docs/en/creating_component_generic_discovery.html
    client = hass.data[MIDEA_API_CLIENT]
    targetDevice = discovery_info[MIDEA_TARGET_DEVICE]
    _LOGGER.debug("midea_dehumidifier: targetDevice = %s", targetDevice)

    if targetDevice is not None:
        #Add entity
        async_add_entities([MideaDehumidifierDevice(hass, client, targetDevice)])

        _LOGGER.info("midea_dehumidifier: humidifier entity initialized.")
    else:
        _LOGGER.error("midea_dehumidifier: error initializing humidifier entity.")


    #Register services
    #https://community.home-assistant.io/t/registering-a-service/40327/11

    async def async_service_set_fan_speed(call):
        entity_id = call.data[ATTR_ENTITY_ID]
        speed_mode = call.data[ATTR_FAN_SPEED]
        async_dispatcher_send(hass, SERVICE_SET_FAN_SPEED.format(entity_id), speed_mode)

    async def async_service_set_ion_state(call):
        entity_id = call.data[ATTR_ENTITY_ID]
        ion_state = call.data[ATTR_ION_STATE]
        async_dispatcher_send(hass, SERVICE_SET_ION_STATE.format(entity_id), ion_state)
		
    async def async_service_set_mode(call):
        entity_id = call.data[ATTR_ENTITY_ID]
        mode_name = call.data[ATTR_MODE]
        async_dispatcher_send(hass, SERVICE_SET_MODE.format(entity_id), mode_name)

    hass.services.async_register(DOMAIN, SERVICE_SET_FAN_SPEED, async_service_set_fan_speed, SERVICE_SET_FAN_SPEED_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_SET_ION_STATE, async_service_set_ion_state, SERVICE_SET_ION_STATE_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_SET_MODE, async_service_set_mode, SERVICE_SET_MODE_SCHEMA)

    return True



async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Dehumidifier device config entry."""
    await async_setup_platform(hass, {}, async_add_entities)


class MideaDehumidifierDevice(HumidifierEntity):
    """Representation of a Midea/Inventor dehumidifier device."""

    def __init__(self, hass, client, targetDevice):
        _LOGGER.debug("midea_dehumidifier: initializing MideaDehumidifierDevice...")

        self._hass = hass
        self._supported_features = SUPPORT_FLAGS

        #Fan modes
        self._fan_dict = DEHUMI_FAN_SPEED_DICT
        self._fan_list = DEHUMI_FAN_SPEED_LIST

        #Device modes
        self._modes_dict = DEHUMI_MODES_DICT
        self._available_modes = DEHUMI_MODES_LIST

        self._client = client
        self._device = targetDevice
        self._name = "midea_dehumidifier_"+targetDevice['id']
        self._unique_id = 'midea_dehumidifier_' + targetDevice['id']

        #Default values for device state
        self._powerMode = None			# 0:off, 1:on
        self._mode = None			# device's current mode ['Target_humidity', 'Continuous', 'Smart', 'Dryer']
        self._ionSetSwitch = None		# 0:off, 1:on
        self._humidity = None			# current humidity
        self._humidity_set = None		# target hunidity
        self._humidity_dot = None		# current humidity (decimal)
        self._humidity_dot_set = None		# target humidity (decimal)
        self._windSpeed = None			# fan speed [1..99]
        self._windSpeedMode = None		# fan speed mode (Silent:40, Medium:60, High:80)
        self._isDisplay = None
        self._filterShow = False
        self._tankShow = False
        self._dryClothesSetSwitch = None
        self._upanddownSwing = None
        self._tankShow = False

	#patch for HA2024.1.0
        #self._device_class = DEVICE_CLASS_DEHUMIDIFIER
	self._device_class = HumidifierDeviceClass.DEHUMIDIFIER

        ##Get appliance's status to set initial values for the device
        #_LOGGER.debug("midea-client: querying appliance status via Web API...")
        #res = self._client.get_device_status(self._device['id'])
        #if res == 1:
        #    _LOGGER.debug("midea_dehumidifier: get_device_status suceeded: "+self._client.deviceStatus.toString())
        #    #Set initial values for device's status
        #    self.__refresh_device_status()
        #else:
        #    _LOGGER.error("midea_dehumidifier: get_device_status error")

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the humidity device."""
        return self._name

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._supported_features

    @property
    def should_poll(self):
        """Return the polling state."""
        #get device's status by polling it: Midea Web API lacks of notification capability
        return True

    @property
    def target_humidity(self):
        """Return the humidity we try to reach."""
        return self._humidity_set

    @property
    def mode(self):
        """Return current mode."""
        return self._mode

    @property
    def available_modes(self):
        """Return available modes."""
        return self._available_modes

    @property
    def is_on(self):
        """Return true if the device is on."""
        return self._powerMode

    @property
    def device_class(self):
        """Return the device class of the humidifier."""
        return self._device_class

    @property
    def ionSetSwitch(self):
        return self._ionSetSwitch

    @property
    def windSpeed(self):
        return self._windSpeed

    @property
    def windSpeedMode(self):
        return self._windSpeedMode

    @property
    def current_humidity(self):
        """Return the current humidity."""
        return self._humidity

    @property
    def min_humidity(self):
        """Return the min humidity set."""
        return 40

    @property
    def max_humidity(self):
        """Return the max humidity set."""
        return 85

    @property
    def tank_show(self):
        """Return the tank status """
        return self._tankShow

    #patch for HA2024.1.0
    #def extra_state_attributes(self):	
    @property
    def device_state_attributes(self):
        """Return entity specific state attributes."""
        data = {}

        for prop, attr in PROP_TO_ATTR.items():
            value = getattr(self, prop)
            if value is not None:
                data[attr] = value

        return data


    #####################################################
    #asycn methods 
    #####################################################

    async def async_added_to_hass(self):
        """Run when about to be added to hass."""
        async_dispatcher_connect(self.hass, SERVICE_SET_FAN_SPEED.format(self.entity_id), self.service_set_fan_speed)
        async_dispatcher_connect(self.hass, SERVICE_SET_ION_STATE.format(self.entity_id), self.service_set_ion_state)
        async_dispatcher_connect(self.hass, SERVICE_SET_MODE.format(self.entity_id), self.service_set_mode)

#
#    def __hass_update_state_attribute(self, _state, _attr, _value):
#        """Update attribute on state obtained via hass.states.get() and return dict containing all the state attributes."""
#        data = {}
#        for attr, value in _state.attributes.items():
#            #_LOGGER.info("(attr, value) = (%s,%s)", attr, value)
#            if attr == _attr:
#                data[attr] = _value
#            else:
#                data[attr] = value
#
#        return data
#

    @callback
    async def service_set_fan_speed(self, speed_mode):
        """service_set_fan_speed"""
        _LOGGER.info("service_set_fan_speed called, speed_mode = %s", speed_mode)
        speed = self._fan_dict.get(speed_mode.upper(), 0)
        _LOGGER.info("speed = %s", speed)
        if self.is_on and self._windSpeed != speed and self._client.deviceStatus.setMode != 4:
            _LOGGER.debug("midea-dehumidifier: sending send_fan_speed_command via Web API...")
            res = await self.hass.async_add_executor_job(self._client.send_fan_speed_command, self._device["id"], speed)
            if res is not None:
                _LOGGER.debug("midea-dehumidifier: send_fan_speed_command suceeded: "+self._client.deviceStatus.toString())
                self._windSpeed = speed
                self._windSpeedMode = speed_mode
                
                #Update state attribute
                state = self._hass.states.get('humidifier.'+self._unique_id)
                if state:
                    #attrs = self.__hass_update_state_attribute(state, ATTR_FAN_SPEED_MODE, speed)
                    attrs = state.attributes.copy()
                    attrs[ATTR_FAN_SPEED_MODE] = speed_mode
                    attrs[ATTR_FAN_SPEED] = speed
                    
                    self._hass.states.async_set('humidifier.'+self._unique_id, state.state, attrs, force_update = True)

            else:
                _LOGGER.error("midea-dehumidifier: send_fan_speed_command ERROR.")

    @callback
    async def service_set_ion_state(self, ion_state):
        """service_set_ion_state"""
        _LOGGER.info("service_set_ion_state called, ion_state = %s", ion_state)
        if self.is_on and self._ionSetSwitch != ion_state:
            if ion_state:
                _LOGGER.debug("midea-dehumidifier: sending send_ion_on_command via Web API...")
                res = await self.hass.async_add_executor_job(self._client.send_ion_on_command, self._device["id"])
            else:
                _LOGGER.debug("midea-dehumidifier: sending send_ion_off_command via Web API...")
                res = await self.hass.async_add_executor_job(self._client.send_ion_off_command, self._device["id"])
            if res is not None:
                _LOGGER.debug("midea-dehumidifier: send_ion_(on/off)_command suceeded: "+self._client.deviceStatus.toString())
                self._ionSetSwitch = ion_state
                #Update state attribute
                state = self._hass.states.get('humidifier.'+self._unique_id)
                if state:
                    #attrs = self.__hass_update_state_attribute(state, ATTR_ION_SET_SWITCH, ion_state)
                    attrs = state.attributes.copy()
                    attrs[ATTR_ION_SET_SWITCH] = ion_state					
                    self._hass.states.async_set('humidifier.'+self._unique_id, state.state, attrs, force_update = True)

            else:
                _LOGGER.error("midea-dehumidifier: send_fan_speed_command ERROR.")

    @callback
    async def service_set_mode(self, mode_name):
        """service_set_mode"""
        _LOGGER.info("service_set_mode called, mode_name = %s", mode_name)
        mode = self._modes_dict.get(mode_name.upper(), 0)
        _LOGGER.info("mode = %s", mode)
        if self.is_on and self._mode != mode:
            _LOGGER.debug("midea-dehumidifier: sending send_mode_command via Web API...")
            res = await self.hass.async_add_executor_job(self._client.send_mode_command, self._device["id"], mode)
            if res is not None:
                _LOGGER.debug("midea-dehumidifier: send_mode_command suceeded: "+self._client.deviceStatus.toString())
                self._mode = mode_name
                #Dryer mode set speed_mode to High too
                if mode == 4:    
                    self._windSpeedMode = 'High'
                    self._windSpeed = self._fan_dict.get('HIGH', 0)
				
                #Update state attribute
                state = self._hass.states.get('humidifier.'+self._unique_id)
                if state:
                    attrs = state.attributes.copy()
                    attrs[ATTR_MODE] = mode_name
                    #Dryer mode set speed_mode to High too
                    if mode == 4:
                        attrs[ATTR_FAN_SPEED_MODE] = 'High'
                        attrs[ATTR_FAN_SPEED] = self._fan_dict.get('HIGH', 0)
					
                    #attrs = self.__hass_update_state_attribute(state, ATTR_MODE, mode)
                    self._hass.states.async_set('humidifier.'+self._unique_id, state.state, attrs, force_update = True)

            else:
                _LOGGER.error("midea-dehumidifier: send_mode_command ERROR.")


    async def async_update(self):
        """Retrieve latest state from the appliance and keep UI updated with respect to the updated status."""
        _LOGGER.info("midea-dehumidifier: async_update called.")
        
        if self._client.security.access_token:
            _LOGGER.debug("midea-dehumidifier: sending get_device_status via Web API...")
            #res = self._client.get_device_status(self._device['id'])
            res = await self.hass.async_add_executor_job(self._client.get_device_status, self._device['id'])
            if res == 1:
                _LOGGER.info(self._client.deviceStatus.toString())
                #Refresh device status
                self.__refresh_device_status()
            else:
                _LOGGER.error("midea-dehumidifier: get_device_status ERROR.")


    def __refresh_device_status(self):
        """Called by async_update(self): keep UI updated with respect to the updated status."""
        if self._client.deviceStatus is not None:
            self._powerMode = self._client.deviceStatus.powerMode
            self._ionSetSwitch = self._client.deviceStatus.ionSetSwitch

            #Current mode
            #self._mode = self._client.deviceStatus.setMode
            self._mode = self._available_modes[self._client.deviceStatus.setMode - 1]

            self._windSpeed = self._client.deviceStatus.windSpeed
            if self._windSpeed == 40:
                self._windSpeedMode = self._fan_list[0]
            elif self._windSpeed == 60:
                self._windSpeedMode = self._fan_list[1]
            elif self._windSpeed == 80:
                self._windSpeedMode = self._fan_list[2]
            else:
                self._windSpeedMode = "unknown"

            self._humidity = self._client.deviceStatus.humidity
            self._humidity_set = self._client.deviceStatus.humidity_set
            self._humidity_dot = self._client.deviceStatus.humidity_dot
            self._humidity_dot_set = self._client.deviceStatus.humidity_dot_set
            self._isDisplay = self._client.deviceStatus.isDisplay
            self._filterShow = self._client.deviceStatus.filterShow
            self._tankShow = self._client.deviceStatus.tankShow
            self._dryClothesSetSwitch = self._client.deviceStatus.dryClothesSetSwitch
            self._upAndDownSwing = self._client.deviceStatus.upAndDownSwing
            self._tankShow = self._client.deviceStatus.tankShow 

            #Useful or useless ?
            #self.async_update_ha_state()
            #self.async_schedule_update_ha_state()

            #PROVE
            #async_update_entity(self._hass, self._name)
            #async_update_entity(self._hass, 'humidifier.midea_dehumidifier_17592186063322')
			#ALTERNATIVA DA PROVARE: self.async_update_entity(self._hass, self._unique_id)

#            state = hass.states.get(entity_id)
#            if state:
#                attrs = state.attributes
#            self._hass.states.set(self._unique_id, state, state.attributes, force_update=True)


    async def async_turn_on(self, **kwargs):
        """Turn the device on."""
        _LOGGER.info("midea-dehumidifier:async_turn_on called.")
        if not self.is_on:
            _LOGGER.debug("midea-dehumi: sending power-on command via Web API...")
            #res = self._client.send_poweron_command(self._device["id"])
            res = await self.hass.async_add_executor_job(self._client.send_poweron_command, self._device["id"])
            if res is not None:
                _LOGGER.debug("midea-dehumidifier: send_poweron_command suceeded: "+self._client.deviceStatus.toString())
                #Refresh device status
                self.__refresh_device_status()
            else:
                _LOGGER.error("midea-dehumidifier: send_poweron_command ERROR.")


    async def async_turn_off(self, **kwargs):
        """Turn the device off."""
        _LOGGER.info("midea-dehumidifier: async_turn_off called.")
        if self.is_on:
            _LOGGER.debug("midea-dehumi: sending power-off command via Web API...")
            #res = self._client.send_poweroff_command(self._device["id"])
            res = await self.hass.async_add_executor_job(self._client.send_poweroff_command, self._device["id"])
            if res is not None:
                _LOGGER.debug("midea-dehumidifier: send_poweroff_command suceeded: "+self._client.deviceStatus.toString())
                #Refresh device status
                self.__refresh_device_status()
            else:
                _LOGGER.error("climate.midea-dehumi: send_poweroff_command ERROR.")


    async def async_set_humidity(self, humidity):
        """Set new humidity level."""
        _LOGGER.info("midea-dehumidifier: async_set_humidity called.")
        if self.is_on:
            if self._humidity_set != humidity:
                _LOGGER.debug("midea-dehumidifier: setting new target hunidity value via Web API...")
                #res = self._client.send_target_humidity_command(self._device["id"], humidity)
                res = await self.hass.async_add_executor_job(self._client.send_target_humidity_command, self._device["id"], humidity)
                if res is not None:
                    _LOGGER.info("midea-dehumidifier: send_target_humidity_command succeeded: "+self._client.deviceStatus.toString())
                    #Refresh device status
                    self.__refresh_device_status()
                else:
                    _LOGGER.error("midea-dehumidifier: send_target_humidity_command ERROR")


    async def async_set_mode(self, mode):
        """Update mode."""
        _LOGGER.info("midea-dehumidifier: async_set_mode called; current_mode=%s, new mode=%s", self._mode, mode)
        if self.is_on:
            mode_num = self._modes_dict.get(mode.upper(), 0)			
            _LOGGER.debug("midea-dehumi: sending update status command via Web API...")
            #res = self._client.send_mode_command(self._device["id"], mode_num)
            res = await self.hass.async_add_executor_job(self._client.send_mode_command, self._device["id"], mode_num)
            if res is not None:
                _LOGGER.debug("midea-dehumidifier: send_mode_command suceeded: "+self._client.deviceStatus.toString())
                self._client.deviceStatus._setMode = mode_num
                #Refresh device status
                self.__refresh_device_status()
            else:
                _LOGGER.error("climate.midea-dehumi: send_mode_command ERROR.")
