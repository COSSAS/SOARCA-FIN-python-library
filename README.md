# SOARCA Fin Library
A Python implementation for the SOARCA FIN, compatible with: SOARCA the TNO orchestrator for Open-C2, CACAO and STIX

## building / starting / stopping  
### Requirements
 - Python3

### Setup
Install requirements
```bash
pip3 install -r requirements.txt
```
Create .env file with the following entries:
```
MQTT_USERNAME = "soarca"
MQTT_PASSWD = "soarca1234"
```


## Quick Run
```bash
python3 main.py
```


## Documentation
For documentation about the fin protocol we refer the reader to de documention page of [SOARCA](https://cossas.github.io/SOARCA/docs/soarca-extensions/fin-protocol/)

For class diagrams and example sequence diagrams of the Fin implementation [plantUML](https://plantuml.com/) is used.