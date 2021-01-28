[<img src = "https://github.com/barban-dev/homeassistant-midea-dehumidifier/blob/master/images/ha-logo.png?raw=true" height = "100">](https://www.home-assistant.io/) 
# Home Assistant Custom Integration for Midea dehumidifiers (Inventor EVA II PRO WiFi / Comfee MDDP-50DEN7 appliances).

[![ViewCount](https://views.whatilearened.today/views/github/barban-dev/midea_inventor_dehumidifier.svg)](http://github.com/barban-dev/homeassistant-midea-dehumidifier)
[![HitCount](http://hits.dwyl.io/barban-dev/homeassistant-midea-dehumidifier.svg)](http://github.com/barban-dev/homeassistant-midea-dehumidifier)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5E7ULVFGCGKU2&source=url)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

Author: Andrea Barbaresi =2020=

Licence: GPLv3

This repo contains a Home Assistant custom integration for EVA II PRO WiFi Smart Dehumidifier appliance by Midea/Inventor.
It has been reported that the custom integration can work also with **Comfee MDDP-50DEN7** appliance.

This custom component is based on python library [***midea_inventor_lib***.](https://github.com/barban-dev/midea_inventor_dehumidifier): see library's readme and prerequisites to be able to control your device on Home Assistant.

Info about the dehumidifier appliance can be found [here.](https://www.inventorappliances.com/dehumidifiers/eva-ii-pro-wi-fi-20l)

You can buy Inventor/Comfee smart dehumidifier appliances (WiFi version) on Amazon (the links below contain my referral code):
* [Inventor Eva II PRO WiFi on Amazon.it](https://amzn.to/2RsIQMx)
* [Comfee MDDP-50DEN7 on Amazon.it](https://amzn.to/3iuBX9D)

* [Inventor Eva II PRO WiFi on Amazon.de](https://amzn.to/3iXpU5F)
* [Comfee MDDP-50DEN7 on Amazon.de](https://amzn.to/3iZ5WYm)

* [Inventor Eva II PRO WiFi on Amazon.es](https://amzn.to/39pYMJb)
* [Comfee MDDP-50DEN7 on Amazon.es](https://amzn.to/2M3MqOn)

* [Inventor Eva II PRO WiFi on Amazon.fr](https://amzn.to/3klHdgh)
* [Comfee MDDP-50DEN7 on Amazon.fr](https://amzn.to/2FlQoi1)

* [Inventor Eva II PRO WiFi on Amazon.co.uk](https://amzn.to/3hDEVaF)
* [Comfee MDDP-50DEN7 on Amazon.co.uk](https://amzn.to/3kdN1ID)

## Installation instruction

### HACS [![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
1. Update HomeAssistant to version 0.96.0 or newer
2. In HACS Store, search for [***barban-dev/midea_dehumidifier***]
3. Install the custom integration
4. Activate midea_dehumidifier custom integration on your HA's configuration yaml file (see instructions below)

### Manual
1. Update HomeAssistant to version 0.96.0 or newer
2. Clone this repo
3. Copy the `custom_components/midea_dehumidifier` folder into your HA's `custom_components` folder
4. Activate midea_dehumidifier custom integration on your HA's configuration yaml file (see instructions below)


## Activate midea_dehumidifier custom integrations

Add the following section in your ``configuration.yaml`` & restart HA (use the same username and password of your INVmate II App):
```
midea_dehumidifier:
  username: user@example.com
  password: passwordExample
```
As usual, you can hide your secret password by means of ``!secret`` notation by specifing it in ``secrets.yaml``

Alternatively, if you prefer, ``sha256password`` parameter can be used instead of the ``password`` one to specify password's sha-256 hash
```
midea_dehumi:
  username: user@example.com
  sha256password: cf76d55503cdee3....
```

If everything is ok, you will find the following two new entities in your HA dashboard:

* **humidifier.midea_dehumidifier_*[Device_ID]***
* **sensor.midea_dehumidifier_*[Device_ID]*_humidity**

By means of the humidifier entity, you can control your appliance whereas the sensor reports the detected current humidity on your environment.

## Lovelace card for midea_dehumidifier entity

Add the following part of code to have a lovelace card representing your device and able to control all its features (change "12345678901234" with your device's ID):

configuration.yaml
```
input_select:
  dehumidifier_fan_mode:
    name: "Fan Mode"
    options:
      - Silent
      - Medium
      - High
    icon: "mdi:animation-outline"
  dehumidifier_modes:
    name: "Modes"
    options:
      - Target_humidity
      - Continuos
      - Smart
      - Dryer
    icon: "mdi:animation-outline"

sensor:
  - platform: template
    sensors:
      midea_current_humidity:
        friendly_name: "midea_current_humidity"
        value_template: "{{ state_attr('humidifier.midea_dehumidifier_12345678901234', 'current_humidity') }}"
        unit_of_measurement: "%"
      midea_target_humidity:
        friendly_name: "midea_target_humidity"
        value_template: "{{ state_attr('humidifier.midea_dehumidifier_12345678901234', 'humidity') }}"
        unit_of_measurement: "%"
```

automations.yaml
```
- alias: input_select.dehumidifier_fan_mode change
  trigger:
    entity_id: input_select.dehumidifier_fan_mode
    platform: state
  action:
    service: midea_dehumidifier.set_fan_speed
    data_template:
      entity_id: humidifier.midea_dehumidifier_12345678901234
      fan_speed: '{{ states.input_select.dehumidifier_fan_mode.state }}'
###
- alias: MideaDehumidifier fan speed change
  trigger:
    entity_id: humidifier.midea_dehumidifier_12345678901234
    platform: state
  action:
    service: input_select.select_option
    data_template:
      entity_id: input_select.dehumidifier_fan_mode
      option: '{{ states.humidifier.midea_dehumidifier_12345678901234.attributes.fan_speed_mode }}'
###
- alias: Set input_select.dehumidifier_fan_mode options to 'High' when state of device change to Dryer
  trigger:
    platform: template
    value_template: "{% if is_state('input_select.dehumidifier_modes', 'Dryer') %}true{% endif %}"
  action:
    service: input_select.set_options
    data_template:
      entity_id: input_select.dehumidifier_fan_mode
      options: 
        - 'High'
- alias: Revert back input_select.dehumidifier_fan_mode options when state of device change to not Dryer
  trigger:
    platform: template
    value_template: "{% if not is_state('input_select.dehumidifier_modes', 'Dryer') %}true{% endif %}"
  action:
    service: input_select.set_options
    data_template:
      entity_id: input_select.dehumidifier_fan_mode
      options:
        - 'Silent'
        - 'medium'
        - 'High'
######
- alias: input_select.dehumidifier_modes change
  trigger:
    entity_id: input_select.dehumidifier_modes
    platform: state
  action:
    service: midea_dehumidifier.set_mode
    data_template:
      entity_id: humidifier.midea_dehumidifier_12345678901234
      mode: '{{ states.input_select.dehumidifier_modes.state }}'
###
- alias: MideaDehumidifier mode change
  trigger:
    entity_id: humidifier.midea_dehumidifier_12345678901234
    platform: state
  action:
    service: input_select.select_option
    data_template:
      entity_id: input_select.dehumidifier_modes
      option: '{{ states.humidifier.midea_dehumidifier_12345678901234.attributes.mode }}'
```



## Installation Troubleshooting

After installation, final result should look similar to this:
```
\\<ha_ip_address>
    └── config
        ├── custom_components
        │   └── midea_dehumidifier
        │       ├── __init__.py
        │       ├── humidifier.py
        │       ├── manifest.json
        │       ├── sensor.py
        │       └── services.yaml
        └── deps
            └── lib
                └── python3.6
                    └── site-packages
                        └── midea_inventor_lib
                            └── libfiles...
```

If you cannot find the midea_dehumidifier entity on HA, check the logs generated by HA to track the issue.
In order to set DEBUG level for midea_dehumidifier, add the following in your HA's configuration yaml:
```
logger:
  default: info
  logs:
    custom_components.midea_dehumidifier: debug
    custom_components.humidifier.midea_dehumidifier: debug
    custom_components.sensor.midea_dehumidifier: debug
```

Copy ``/midea_inventor_lib`` folder on ``\deps\lib\python3.6\site-packages\`` of your HA's configuration shared folder.




Donations
---------
If this project helps you to reduce time to develop your code, you can make me a donation.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5E7ULVFGCGKU2&source=url)
[![coffe](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/barban)

