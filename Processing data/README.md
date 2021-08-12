# Information
This code was created to process and display the data obtained by the MPU6050 sensor using the Raspberry Pi.

To run it, you need the libraries:
 - Matplotlib
 -  Pandas
 - SciPy
 - Math

# How to use
Run the "main" file on your computer or your Raspberry Pi to start the program.

The program will ask several questions to know which type of data, graph, and which file has the collected data.

The program can return the following data by responding to the terminal:

    acc = Body acceleration
    vel = Body speed integrating acceleration without correction
    pos = Body position integrating speed without correction
    veld = Body velocity integrating acceleration removing drift
    posd = Body position integrating velocity with correction
    quat = Quaternion obtained by the sensor
    quatc = Real body quaternion
    euler = Rotation in radians of the body without correction
    eulerc = Rotation in radians of the body with correction

Possible ways to display or save data are:

    |----Animated
        |----2d animated graphic
            |-Any data
        |----3d animated graphic
            |-Rotation
            |-Position
            |-Position and Rotation
    |----Static
        |----2d static graphic
            |-One data folder
                |One column
                |Three stacked graphics
            |-More than one folder
        |----3d static graphic
            |-Position
            |-Position and rotation
# Test
In the "Datas" folder there are some examples with data already collected. Use them to test the program:

    data_0 (file_number = 0): Parable shaped movement
    data_1 (file_number = 1): 360 degree rotation around the y axis
    data_2 (file_number = 2): Square shaped movement
    data_3 (file_number = 3): Straight line movement
    data_4 (file_number = 4): Rotation around the y axis

## Examples
Type the string "1 0 1 1 2" by pressing enter at each number. You will get an animated graphic indicating the position of a move in square shape. 
    The video for this movement can be seen at: https://www.youtube.com/watch?v=ekyY6dQ9t6o
![](https://cdn.discordapp.com/attachments/857382160712466452/875227725923774504/unknown.png)
![](https://cdn.discordapp.com/attachments/857382160712466452/875227879313653770/unknown.png)

Type the string "1 0 1 0 4" by pressing enter at each number. You will get an animated graphic indicating the rotation around the y axis. 
    The video for this movement can be seen at: https://www.youtube.com/watch?v=dDBdsNAT8Fs
![](https://cdn.discordapp.com/attachments/857382160712466452/875228051024253008/unknown.png)
![](https://cdn.discordapp.com/attachments/857382160712466452/875228338472501278/unknown.png)

Enter the string "1 1 0 0 1 3 acc veld posd". You'll get a static graph showing the acceleration, velocity, and position of a body that has made a straight-line trajectory. 
    The video for this movement can be seen at: https://www.youtube.com/watch?v=ekyY6dQ9t6o
![](https://cdn.discordapp.com/attachments/857382160712466452/875228632518377482/unknown.png)
![](https://cdn.discordapp.com/attachments/857382160712466452/875228764609585152/unknown.png)
## NOTE
Due to the difference in the calibration of the sensors, in which each one collects data with different errors, for some movements, the "stationary" function can have a bad performance, as it was calibrated for my sensor. To fix it, go to the "get_stationary" function in "functions.py" and modify the parameters for the filters so that the "stationary" function works fine, automatically correcting the velocity and position.
