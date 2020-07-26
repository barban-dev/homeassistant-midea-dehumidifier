"""
Custom integation based on humidifer and sensor platforms for EVA II PRO WiFi Smart Dehumidifier appliance by Midea/Inventor.
For more details please refer to the documentation at
https://github.com/barban-dev/midea_inventor_dehumidifier
"""
VERSION = '1.0.0'

import logging
from custom_components.midea_dehumidifier import DOMAIN, MIDEA_TARGET_DEVICE
from homeassistant.helpers.entity import Entity
from homeassistant.const import (DEVICE_CLASS_HUMIDITY)

from custom_components.midea_dehumidifier.humidifier import ATTR_CURRRENT_HUMIDITY

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up available sensors for MideaDehumidifier Humidifier Entity."""
    _LOGGER.info("sensor.midea_dehumidifier: initializing sensor entity sub-component")
    _LOGGER.debug("sensor.midea_dehumidifier: starting async_setup_platform")

    #ref: https://developers.home-assistant.io/docs/en/creating_component_generic_discovery.html
    targetDevice = discovery_info[MIDEA_TARGET_DEVICE]
    _LOGGER.debug("sensor.midea_dehumidifier: targetDevice = %s", targetDevice)
    
    if targetDevice:
        #Create sensor entity
        sensor = MideaDehumidifierSensor(targetDevice, hass)

        #Add sensor entity
        async_add_entities([sensor])
        _LOGGER.info("midea_dehumidifier: sensor entity initialized.")
    else:
        _LOGGER.error("midea_dehumidifier: error initializing sensor entity.")

	
class MideaDehumidifierSensor(Entity):
    """Humidity sensors embedded on Midea Dehumidifier device."""

    def __init__(self, targetDevice, hass):
        """Initialize the sensor."""

        self._device = targetDevice
        self._hass = hass
        self._name = 'midea_dehumidifier_' + targetDevice['id'] + '_humidity'
        self._unique_id = 'midea_dehumidifier_' + targetDevice['id'] + '_humidity'
        #self._type = type
        self._device_class = DEVICE_CLASS_HUMIDITY
        self._unit_of_measurement = '%'
        self._icon = 'mdi:water-percent'
        #self._battery = battery

        self._humidifier_entity_id = 'humidifier.midea_dehumidifier_' + targetDevice['id']

        self._state = None
        self.__updateStateFromHumidifierEntity()


    def __updateStateFromHumidifierEntity(self):
        """Update state from current_humidity attribute of humidifier entity"""
        #hass.states.get is async friendly (ref. https://dev-docs.home-assistant.io/en/master/api/core.html#homeassistant.core.StateMachine)
        state = self._hass.states.get(self._humidifier_entity_id)
        if state:
            _LOGGER.debug("state.attributes = %s", state.attributes)
        #ATTR_CURRRENT_HUMIDITY attribute may not exist when device is initializing...
        if state and (ATTR_CURRRENT_HUMIDITY in state.attributes):
            #Update state
            self._state = state.attributes[ATTR_CURRRENT_HUMIDITY]
            _LOGGER.debug("sensor.midea_dehumidifier: current humidity = %s", self._state)
        else:
            _LOGGER.debug("sensor.midea_dehumidifier: cannot retrieve the state of midea_dehumidifier device")

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor device. The Name is derived from the device id"""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Update the state from the template."""
        self.__updateStateFromHumidifierEntity()

    @property
    def should_poll(self):
        return True
