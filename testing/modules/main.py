from sensors.temp_and_humid.sensTempHum import TermoHumid



th = TermoHumid()

th.start()
print th.temp
th.stop()