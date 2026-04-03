"""
Pump switch platform for EVA II PRO WiFi Smart Dehumidifier appliance by Midea/Inventor.
For more details please refer to the documentation at
https://github.com/barban-dev/midea_inventor_dehumidifier
"""
VERSION = '1.07'

import logging
from custom_components.midea_dehumidifier import DOMAIN, MIDEA_API_CLIENT, MIDEA_TARGET_DEVICE
from homeassistant.components.switch import SwitchEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up pump switch platform for MideaDehumidifier."""
    _LOGGER.info("switch.midea_dehumidifier: initializing pump switch platform")

    client = hass.data[MIDEA_API_CLIENT]
    targetDevice = discovery_info[MIDEA_TARGET_DEVICE]

    if targetDevice is not None:
        async_add_entities([MideaPumpSwitch(hass, client, targetDevice)])
        _LOGGER.info("switch.midea_dehumidifier: pump switch entity initialized.")
    else:
        _LOGGER.error("switch.midea_dehumidifier: error initializing pump switch entity.")


class MideaPumpSwitch(SwitchEntity):
    """Representation of the pump switch on a Midea/Inventor dehumidifier."""

    def __init__(self, hass, client, targetDevice):
        self._hass = hass
        self._client = client
        self._device = targetDevice
        self._name = 'midea_dehumidifier_' + targetDevice['id'] + '_pump'
        self._unique_id = 'midea_dehumidifier_' + targetDevice['id'] + '_pump'
        self._is_on = False

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return 'mdi:water-pump'

    @property
    def is_on(self):
        return self._is_on

    @property
    def should_poll(self):
        return True

    async def async_update(self):
        """Update pump state from device status."""
        if self._client.deviceStatus is not None:
            self._is_on = self._client.deviceStatus.pumpSwitch == 1
            _LOGGER.debug("switch.midea_dehumidifier: pump state updated: %s", self._is_on)

    async def async_turn_on(self, **kwargs):
        """Turn the pump on."""
        _LOGGER.info("switch.midea_dehumidifier: async_turn_on (pump) called.")
        if self._client.deviceStatus and self._client.deviceStatus.powerMode == 1:
            res = await self._hass.async_add_executor_job(
                self._client.send_pump_on_command, self._device['id']
            )
            if res:
                self._is_on = True
                _LOGGER.debug("switch.midea_dehumidifier: send_pump_on_command succeeded.")
            else:
                _LOGGER.error("switch.midea_dehumidifier: send_pump_on_command ERROR.")
        else:
            _LOGGER.warning("switch.midea_dehumidifier: pump cannot be turned on while device is off.")

    async def async_turn_off(self, **kwargs):
        """Turn the pump off."""
        _LOGGER.info("switch.midea_dehumidifier: async_turn_off (pump) called.")
        if self._client.deviceStatus and self._client.deviceStatus.powerMode == 1:
            res = await self._hass.async_add_executor_job(
                self._client.send_pump_off_command, self._device['id']
            )
            if res:
                self._is_on = False
                _LOGGER.debug("switch.midea_dehumidifier: send_pump_off_command succeeded.")
            else:
                _LOGGER.error("switch.midea_dehumidifier: send_pump_off_command ERROR.")
        else:
            _LOGGER.warning("switch.midea_dehumidifier: pump cannot be turned off while device is off.")
