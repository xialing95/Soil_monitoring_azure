import bme680
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
        print(APP_ENV_SENSOR_LOG + 'created')
    else:
        print(APP_ENV_SENSOR_LOG + 'exist')

# write on the soil log file
def env_sensor_log(data):
    time = time.strftime("%m-%d-%H%M%S", time.localtime())
    temp = data["temperature"]
    humidity = data["humidity"]
    pressure = data["pressure"]
    
    sensorlog_f = open(APP_STATIC + APP_ENV_SENSOR_LOG, 'a')
    # Write data to the log file
    sensorlog_f.write(f"{time}, {temp:.2f}, {humidity:.2f}, {pressure:.2f}\n")
    sensorlog_f.close()
    return

def get_bme680_data():
    try:
        sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
    except (RuntimeError, IOError):
        print("Could not initialize BME680 sensor!")

    # Configure the sensor
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    # sensor.set_filter(bme680.FILTER_SIZE_3)
    # sensor.set_gas_heater_temperature(320)  # degrees Celsius
    # sensor.set_gas_heater_duration(150)      # milliseconds

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
    
def timelapse_bme680(interval, duration):
    check_env_sensor_log()

    """Read data from the BME680 sensor at a specified interval for a given duration."""
    start_time = time.time()

    while (time.time() - start_time < duration):
        data = get_bme680_data()
        env_sensor_log(data)
        print("datalog" + time.time())

        time.sleep(interval)

# Example usage
if __name__ == "__main__":
    try:
       timelapse_bme680(1, 60)
    except KeyboardInterrupt:
        print("Exiting...")
