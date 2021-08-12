# Information
This code is an update of Richard's code (https://github.com/richardghirst/PiBits/tree/master/MPU6050-Pi-Demo) which in turn is a modification of Jeff Rowberg's code so that the library works on the Raspberry Pi.

Copyright (c) 2012 Jeff Rowberg, and copied from
https://github.com/jrowberg/i2cdevlib

> I have simply hacked it to work with the RaspberryPi, using the
> in-kernel I2C drivers. It should be trivial to make use of any of the
> other sensors Jeff supports in this way. 
> - Richard Hirst <richardghirst@gmail.com>   06 Nov 2012
# Hardware
Create the circuit below on a breadboard or a phenolite board:
|GPIO|Component|
|--|--|
|8|SDA sensor|
|9|SLC sensor|
|0|Green Led|
|2|Red Led|
|3|Push Button|

## Example
My board:

![](https://cdn.discordapp.com/attachments/633486363139768330/872995568232837181/unknown.png)

My prototype:

![](https://cdn.discordapp.com/attachments/633486363139768330/875231769895510046/23daad41-3327-4f58-ab31-534a9cfbfb0a.png)

# Instruction

 - You need libgtkmm-3.0-dev installed in order to build. 
 - You need wiring-pi installed in order to build collect_data. http://wiringpi.com/download-and-install/


**NOTE:** If you have a revision 2 Raspberry Pi you need to edit I2Cdev.cpp and change all references to "/dev/i2c-0" to read "/dev/i2c-1".

Run "make" on your terminal. It will create two files: **"collect_data"** and **"IMU_zero"**.
## IMU_zero
  
Start the program and wait, after some time it will give you the maximum and minimum values ​​for the sensor calibration. Go to the code "collect_data" and modify the offsets to your values.
## Collect_data
Running "collect_data", the program will start counting 25 seconds and after that time it will allow you to press the button to start and finish the collection. If you press the button for more than 5 seconds Rapberry will turn off. 

For each data collected, a new file "data_" will be created in the "Data" folder. Successive collections can be made without restarting the program. 

The LEDs will indicate the status of the program:

 
|Green|Red|State|
|--|--|--|
| 0 | 1 |Wait|
| 1 | 1 |Ready |
| 1 | 0 |Collecting|

After collecting the data, copy the files from the "Datas" folder and paste them into the "Processing data" program.






