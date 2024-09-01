[<img src = "https://github.com/barban-dev/homeassistant-midea-dehumidifier/blob/master/images/ha-logo.png?raw=true" height = "100">](https://www.home-assistant.io/) 
# Home Assistant Custom Integration for Midea dehumidifiers (Inventor EVA II PRO WiFi / Comfee MDDP-50DEN7 appliances).

[![ViewCount](https://views.whatilearened.today/views/github/barban-dev/midea_inventor_dehumidifier.svg)](http://github.com/barban-dev/homeassistant-midea-dehumidifier)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5E7ULVFGCGKU2&source=url)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

Author: Andrea Barbaresi =2020-2024=

Licence: GPLv3

This repo contains a Home Assistant custom integration for EVA II PRO WiFi Smart Dehumidifier appliance by Midea/Inventor.
It has been reported that the custom integration can work also with **Comfee MDDP-50DEN7** appliance.

This custom component is based on python library [***midea_inventor_lib***.](https://github.com/barban-dev/midea_inventor_dehumidifier): see library's readme and prerequisites to be able to control your device on Home Assistant.

You can buy Midea/Inventor/Comfee smart dehumidifier appliances (WiFi version) on Amazon sites (the links below contain my referral code):
### Amazon USA
* [Midea Cube 20 pint](https://amzn.to/3MA8R9b)
* [Midea Cube 35 pint](https://amzn.to/4cOeFXp)
* [Midea Cube 50 pint](https://amzn.to/3MuxWCE)
* [Midea Cube 50 pint w pump](https://amzn.to/3MA8ZWd)
* [Midea EasyDry 22 pint](https://amzn.to/3TdxAUy)
* [Midea EasyDry 35 pint](https://amzn.to/4cLXJkl)
* [Midea EasyDry 50 pint](https://amzn.to/4cNR6On)
* [Midea EasyDry 50 pint w pump](https://amzn.to/3MugDSb)
* [Midea EasyDry 50 pint w pump wifi upd](https://amzn.to/478YAuc)

### Amazon UK
* [Inventor Fresh](https://amzn.to/3AVFkEm)
* [Comfee 10L](https://amzn.to/3XbAiLG)
* [Comfee 10L w HEPA filter](https://amzn.to/3X1Blh6)
* [Comfee 12L](https://amzn.to/3X8fx3p)
* [Comfee 12L w HEPA filter](https://amzn.to/3Z1RHZM)
* [Comfee 16L](https://amzn.to/3X7tte6)
* [Comfee 20L](https://amzn.to/477QwK8)
  
### Amazon IT
* [Midea FRESH DRY 10L](https://amzn.to/3AFEviX)
* [Midea FRESH DRY 12L](https://amzn.to/3TbaY7c)
* [Midea FRESH DRY 20L (DE plug)](https://amzn.to/478z0pk)
* [Midea FRESH DRY 20L](https://amzn.to/3MqOHhY)
* [Inventor Eva II PRO WiFi on Amazon.it](https://amzn.to/2RsIQMx)
* [Comfee MDDP-50DEN7 on Amazon.it](https://amzn.to/3iuBX9D)
  
### Amazon DE
* [Midea DF-20DEN7-WF](https://amzn.to/3MAep3v)
* [Midea DF-20DEN7-WF](https://amzn.to/3TaMn2t)
* [Midea Cube 20L](https://amzn.to/4e7ER0o)
* [Midea Quiet 12L](https://amzn.to/478iEgo)
* [Midea Quiet 20L](https://amzn.to/3ANpfkb)
* [Midea Fesh Dry 10L](https://amzn.to/4cNUFUL)
* [Midea Fesh Dry 12L](https://amzn.to/478HlJE)
* [Comfeee MDDN-10DEN7 10L](https://amzn.to/3z2IHJ8)
* [Comfeee MDDN-10DEN7 12L](https://amzn.to/3Xq234h)
* [Comfeee MDDN-10DEN7 16L](https://amzn.to/3XsPPYA)
* [Comfeee MDDN-10DEN7 20L](https://amzn.to/3Xufhft)
* [Comfeee MDDN-10DEN7 30L](https://amzn.to/478ilSM)
* [Comfeee MDDN-10DEN7 50L](https://amzn.to/3XosSWG)
* [Comfeee Easy Dry 16L](https://amzn.to/4dL3DU2)
* [Comfeee Easy Dry 20L](https://amzn.to/3z5gbXt)
    
### Amazon ES
* [Midea Cube 20L](https://amzn.to/3zdecQN)
* [Midea MDDF-20DEN7 20L](https://amzn.to/3T8qIrO)
* [Midea MDDF-20DEN7 50L](https://amzn.to/4e8TQqD)
* [Midea 12L](https://amzn.to/3ANqIHd)
* [Midea 20L](https://amzn.to/4761JuZ)
* [Midea 1500 pies](https://amzn.to/3Teer4T)
* [Comfee 10L](https://amzn.to/4g7skM2)
* [Comfee 12L](https://amzn.to/4e4pzcL)
* [Comfee 20L](https://amzn.to/4gbXBxF)
* [Comfee 20L new 2024 version](https://amzn.to/4dLaWeG)
* [Comfee Easy Dry 16L new 2024 version](https://amzn.to/3z32ubu)
* [Comfee Easy Dry 50L new 2024 version](https://amzn.to/3TbTjMT)
  
### Amazon FR
* [Midea Cube 12L](https://amzn.to/478xHqa)
* [Midea Cube 20L 80m2](https://amzn.to/3X86lfh)
* [Midea Cube 20L 40m2](https://amzn.to/4g51YKL)
* [Midea 12L](https://amzn.to/4gaVDgI)
* [Midea 20L](https://amzn.to/3AVHwM6)
* [Midea 50L](https://amzn.to/3AMkK9D)
* [Midea ‎MAD22C1AWS](https://amzn.to/3XapltH)
* [Midea Fresh Dry 10L w HEPA filter](https://amzn.to/4cM4jY5)
* [Comfee 12L](https://amzn.to/3z1Urf0)
* [Comfee 20L](https://amzn.to/3AJaPBM)
* [Comfee 50L](https://amzn.to/47bQpNQ)
* [Comfee MDDN-10DEN7 10L](https://amzn.to/4dHVKig)
* [Comfee Easy Dry 12L](https://amzn.to/3Z2ten7)
* [Comfee MDDF-20DEN7 20L](https://amzn.to/3Tdyxwp)
* [Comfee MDDPE-30DEN7 30L](https://amzn.to/4dKjceV)
  
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
      - Continuous
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

