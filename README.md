# Soil_monitoring_azure
Soil holographic microbes monitoring 

How connect to the soil sensor (July 9 2022)

If you want to test without putting the electronics in the housing. 
	•	Plug in the HDMI and the keyboard first before the green power cable. Do not plug in the power usb and the battery power at the same time!!!! 
	•	Wait for the raspi to boot up.
	•	Currently we have the system on auto run the app script on reboot, but for some reason the script does not work. So instead, we are going to close the script and run it normally
	⁃	If you see “Soilstate.txt started” and the IP address, and flask server is running on the monitor it means that the script is running and we want to exit out of it. 
	⁃	To exit the script press control + C. 
	⁃	You should see pi@soilsensor2 $ on the command line. 
	⁃	If you don’t see “soilstate.txt” + etc and just a bunch of error message and pi@soilsensor2 $. It means something went wrong with the script at start up and exit out of itself. Either way we are going to restart it. 
	•	navigate to the app location using cd /Documents/Soil_monitoring_azure
	•	To run the app type sh launcher.sh or python3 app.py
	•	and hopefully you should see “soilstate.txt started” the IP address on the tiny display and the monitoring. Go on to the website with the IP address + :5000. Everything should be good to go. 

If you want to test with the electronics in the housing
	•	You won’t be able to use the monitor/keyboard. The power should be connect to the battery. 
	•	Once the battery is connect, wait for the system to boot. 
	•	The tiny display should come up with the IP address (if it was able to connect on MIT wifi. If not the IP address would be blank. Try restarting it)
	•	With the IP address, you can now ssh into the pi using the terminal on your laptop. Must be on the same wifi network. 
	•	open terminal, type in ssh pi@IPaddress 
	•	It should ask you for the password: raspberry 
	•	When you are logged on, on your laptop’s terminal it should print a the same message either “soilstate.txt”, server on or error and pi@soilsensor2 $
	⁃	If you see “Soilstate.txt started” and the IP address, and flask server is running on the monitor it means that the script is running and we want to exit out of it. 
	⁃	To exit the script press control + C. 
	⁃	You should see pi@soilsensor2 $ on the command line. 
	⁃	If you don’t see “soilstate.txt” + etc and just a bunch of error message and pi@soilsensor2 $. It means something went wrong with the script at start up and exit out of itself. Either way we are going to restart it. 
	⁃	Navigate to the app location using cd /Documents/Soil_monitoring_azure
	⁃	To run the app type sh launcher.sh or python3 app.py
	⁃	and hopefully you should see “soilstate.txt started” the IP address on the tiny display and the monitoring. Go on to the website with the IP address + :5000. Everything should be good to go. 

Hopefully that works. Try restarting if something goes wrong, by either typing shutdown now on the command line or unplug and plug the power cable. 

The best way to get the image is to use ssh with either fetch or FileZilla and download the image. 

Todo:
* Update camera setting for consistant camera
* Add error catching for naming conversion (need to have .jpg)
* Create containers and save images
* Add flash and 555 timer for pulsing laser (https://www.instructables.com/555-Timer/#step3, https://picamera.readthedocs.io/en/release-1.13/recipes2.html#using-a-flash-with-the-camera)

Microfluidic channel
* Thinner viewport or filter (too dense) 
* registration mark on the channel 
