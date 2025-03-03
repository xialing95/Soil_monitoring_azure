import bme680
import time

# Create a BME680 object
sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY) #0x77 address as secondary

# Configure the sensor
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_heater_temperature(320)  # degrees Celsius
sensor.set_gas_heater_duration(150)      # milliseconds
sensor.select_gas_heater_profile(0)

# Main loop
try:
    while True:
        # Trigger measurement
        if sensor.get_sensor_data():
            # Print sensor data
            print("Temperature: {:.2f} °C".format(sensor.data.temperature))
            print("Pressure: {:.2f} hPa".format(sensor.data.pressure))
            print("Humidity: {:.2f} %".format(sensor.data.humidity))
            print("Gas Resistance: {} Ohms".format(sensor.data.gas_resistance))
            print("Air Quality: {}".format(sensor.data.air_quality))
            print("-----------------------------")
        
        # Wait before the next measurement
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped by User")