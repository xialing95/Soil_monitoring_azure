import bme680
import time

def get_bme680_data():
    # Create a BME680 sensor object
    sensor = bme680.BME680(i2c_addr=bme680.I2C_ADDR_SECONDARY)

    # Configure the sensor
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_heater_temperature(320)  # degrees Celsius
    sensor.set_gas_heater_duration(150)      # milliseconds

    # Read sensor data
    if sensor.get_sensor_data():
        data = {
            'temperature': sensor.data.temperature,
            'humidity': sensor.data.humidity,
            'pressure': sensor.data.pressure,
            'gas_resistance': sensor.data.gas_resistance
        }
        print(f"Temperature: {data['temperature']:.2f} °C")
        print(f"Humidity: {data['humidity']:.2f} %")
        print(f"Pressure: {data['pressure']:.2f} hPa")
        print(f"Gas Resistance: {data['gas_resistance']} Ohms")
        print('---')
        return data
    else:
        print(f"Temperature: {data['temperature']:.2f} °C")
        print(f"Humidity: {data['humidity']:.2f} %")
        print(f"Pressure: {data['pressure']:.2f} hPa")
        print(f"Gas Resistance: {data['gas_resistance']} Ohms")
        print('---')
        print ("Failed to read sensor data")
        return None

# # Example usage
# if __name__ == "__main__":
#     try:
#         while True:
#             sensor_data = get_bme680_data()
#             if sensor_data:
#                 print(f"Temperature: {sensor_data['temperature']:.2f} °C")
#                 print(f"Humidity: {sensor_data['humidity']:.2f} %")
#                 print(f"Pressure: {sensor_data['pressure']:.2f} hPa")
#                 print(f"Gas Resistance: {sensor_data['gas_resistance']} Ohms")
#                 print('---')
#             else:
#                 print("Failed to read sensor data.")
#             time.sleep(1)  # Read every second
#     except KeyboardInterrupt:
#         print("Exiting...")