"""
TO DO: fail check for 12C
error that keep encountering 
temp = self._get_regs(register, 1) ^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
File "/home/pi/Soil_monitoring_azure/env/lib/python3.11/site-packages/bme680/init.py", 
line 352, in _get_regs return self._i2c.read_byte_data(self.i2c_addr, register) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
File "/usr/lib/python3/dist-packages/smbus2/smbus2.py", line 433, in read_byte_data ioctl(self.fd, I2C_SMBUS, msg)
"""


import bme680
import threading
import time
import os

# set file directory to static 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_ENV_SENSOR_LOG = '/EnvironmentalState.txt'

# create SoilState file if not exist 
def check_env_sensor_log():
    if not os.path.exists(APP_STATIC + APP_ENV_SENSOR_LOG):
        sensorlog_f = open(APP_STATIC + APP_ENV_SENSOR_LOG, 'a')
        sensorlog_f.write('time, temperature (C), humidity (%), pressure (nPa) ' + "\n")
        sensorlog_f.close()
        print(APP_ENV_SENSOR_LOG + ' created')
    else:
        print(APP_ENV_SENSOR_LOG + ' exist')

# write on the soil log file
def env_sensor_log(data):
    timestr = time.strftime("%m-%d-%H%M%S", time.localtime())
    temp = data["temperature"]
    humidity = data["humidity"]
    pressure = data["pressure"]
    
    sensorlog_f = open(APP_STATIC + APP_ENV_SENSOR_LOG, 'a')
    # Write data to the log file
    sensorlog_f.write(f"{timestr}, {temp:.2f}, {humidity:.2f}, {pressure:.2f}\n")
    sensorlog_f.close()
    return

# Function to initialize the BME680 sensor with retries
def initialize_bme680(max_retries=2, delay=1):
    for attempt in range(max_retries):
        try:
            sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
            # Configure the sensor
            sensor.set_humidity_oversample(bme680.OS_2X)
            sensor.set_pressure_oversample(bme680.OS_4X)
            sensor.set_temperature_oversample(bme680.OS_8X)
            # sensor.set_filter(bme680.FILTER_SIZE_3)
            # sensor.set_gas_heater_temperature(320)  # degrees Celsius
            # sensor.set_gas_heater_duration(150)      # milliseconds
            print("BME680 sensor initialized successfully!")
            return sensor
        
        except (RuntimeError, IOError) as e:
            print(f"Attempt {attempt + 1} of {max_retries}: Could not initialize BME680 sensor! Error: {e}")
            time.sleep(delay)  # Wait before retrying
    print("Failed to initialize BME680 sensor after multiple attempts.")

    return 

def get_single_data():
    sensor = initialize_bme680()
    data = get_bme680_data(sensor)
    return data

def get_bme680_data(sensor):
    if sensor is None:
        # Handle the case where the sensor could not be initialized
        print("Exiting program due to sensor initialization failure.")
        data = {
            'temperature': "N/A",
            'humidity': "N/A",
            'pressure': "N/A",
            # 'gas_resistance': sensor.data.gas_resistance
        }
        return data

    # Read sensor data
    if sensor.get_sensor_data():
        data = {
            'temperature': sensor.data.temperature,
            'humidity': sensor.data.humidity,
            'pressure': sensor.data.pressure,
            # 'gas_resistance': sensor.data.gas_resistance
        }
        return data
    else:
        print ("Failed to read sensor data")
        return None
    
"""Read data from the BME680 sensor at a specified interval for a given duration."""
def timelapse_env_log(interval, duration):
    check_env_sensor_log()
    sensor = initialize_bme680()

    start_time = time.time()
    while (time.time() - start_time < duration):
        data = get_bme680_data(sensor)
        env_sensor_log(data)
        print("datalog" + str(time.time()))

        time.sleep(interval)

# Function to start the logging in a separate thread
def start_env_logging_thread(interval, duration):
    logging_thread = threading.Thread(target=timelapse_env_log, args=(interval, duration))
    logging_thread.start()
    return logging_thread

# Example usage
if __name__ == "__main__":
    try:
       print(bme680.__version__)  # Should print without errors
       start_env_logging_thread(10, 60)
    except KeyboardInterrupt:
        print("Exiting...")
