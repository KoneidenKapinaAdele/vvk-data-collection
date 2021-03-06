
# nimi, device_id, place_id, type, zwave_path
devices = [
	('vessa1_lampo', 1003, 1, 'temperature', (3, 0, 49, 1, 'val')),
	('vessa1_valo', 1004, 1, 'ambient_light', (3, 0, 49, 3, 'val')),
	('vessa1_ovi', 1001, 1, 'closed', (3, 0, 48, 10, 'level')),
	('vessa1_liike', 1002, 1, 'movement', (2, 0, 48, 1, 'level'))
]

zway_user = 'vvk'

zway_poll_url = "http://localhost:8083/ZWaveAPI/Data/"
zway_poll_pattern = "devices.%d.instances.%d.commandClasses.%d.data.%d"

zway_url = "http://localhost:8083/JS/Run/"
zway_pattern = "zway.devices[%d].instances[%d].commandClasses[%d].data[%d].%s.value"

vvk_url = 'https://secret-oasis-98680.herokuapp.com/v1/event'

