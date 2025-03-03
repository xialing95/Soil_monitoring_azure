import bme680
import time

class BME680Sensor:
    def __init__(self, address=bme680.I2C_ADDR_SECONDARY):
        """Initialize the BME680 sensor."""
        self.sensor = bme680.BME680(address)
        self.configure_sensor()

    def configure_sensor(self):
        """Configure the sensor settings."""
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        self.sensor.set_gas_heater_temperature(320)  # degrees Celsius
        self.sensor.set_gas_heater_duration(150)      # milliseconds
        self.sensor.select_gas_heater_profile(0)

    def read_sensor_data(self):
        """Read data from the sensor."""
        if self.sensor.get_sensor_data():
            data = {
                "temperature": self.sensor.data.temperature,
                "pressure": self.sensor.data.pressure,
                "humidity": self.sensor.data.humidity,
                "gas_resistance": self.sensor.data.gas_resistance,
                "air_quality": getattr(self.sensor.data, 'air_quality', 'N/A')  # Handle missing attribute
            }
            return data
        else:
            return None

    def print_sensor_data(self):
        """Print the sensor data."""
        data = self.read_sensor_data()
        if data:
            print("Temperature: {:.2f} °C".format(data["temperature"]))
            print("Pressure: {:.2f} hPa".format(data["pressure"]))
            print("Humidity: {:.2f} %".format(data["humidity"]))
            print("Gas Resistance: {} Ohms".format(data["gas_resistance"]))
            print("Air Quality: {}".format(data["air_quality"]))
            print("-----------------------------")
        else:
            print("Failed to read sensor data.")

    def run(self):
        """Run the sensor reading loop."""
        try:
            while True:
                self.print_sensor_data()
                time.sleep(1)  # Adjust the delay as needed
        except KeyboardInterrupt:
            print("Program stopped by User")

# Example usage
if __name__ == "__main__":
    bme680_sensor = BME680Sensor(address=bme680.I2C_ADDR_SECONDARY)  # Use 0x77 address
    bme680_sensor.run()