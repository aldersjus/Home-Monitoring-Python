# Home-Monitoring-Python
### Beginning development of a home monitoring system. 
___

You will need:
*Raspberry Pi
*RIR Sensor
*LED

#### Why Python?
Well, I originally was planning to make this with Android Things [see this repository](https://github.com/aldersjus/Home-Monitoring-Android-Things) as I have quite a bit experience with it. However, as I got into the project I started to encounter several issues, so I decided to try in Python and it was much simpler to implement!
___

The program senses movements through a PIR sensor. A movement object
is created with the count and datetime passed in, this is stored in
a list. The list is saved to a file periodically. The program will
also flash an LED to show it has detected movement.
