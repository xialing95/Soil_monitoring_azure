kill -9 $(lsof -t -i:5000)
cd /home/pi/Documents/Soil_monitoring_azure
source env/bin/activate
PYTHONPATH=/home/pi/env/bin/python
python3 /home/pi/Documents/soil_azure/hotspot.py
