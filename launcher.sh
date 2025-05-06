kill -9 $(lsof -t -i:5000)
cd /home/pi/Soil_monitoring_azure
source env/bin/activate
PYTHONPATH=/home/pi/env/bin/python
python3 /home/pi/Soil_monitoring_azure/hotspot.py --ssid HoloScopePurple --password fishystuff