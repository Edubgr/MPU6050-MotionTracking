# Description
This program was designed to determine the position and rotation of a body using the **MPU6050** and a **Raspberry Pi**.

From the acceleration and quaternion values ​​obtained by the sensor, it is possible to determine the **rotation, position and velocity** of a body, using due processes. The program is still a robust version, which needs some improvements. Long movements with few pauses tend to have poor accuracy for position and velocity, due to the drift obtained by integrating acceleration data. However, rotation works in all cases, obtaining a rotation identical to the rotation performed by the body.
# Instructions 
To make it work, create the necessary circuit on a protoboard, run the program "Collect data" on your raspberry, press the button to start collecting the movement data and press it again to finish. Copy the files into the "Datas" folder and paste them into the "Processing data" program. Then run it on your computer or raspberry, following the appropriate procedures.
# Example
The program is able to return different types of graphs of different types of data. Examples of results and movements performed can be seen in:
    
https://www.youtube.com/watch?v=dDBdsNAT8Fs

https://www.youtube.com/watch?v=ekyY6dQ9t6o
## Square shaped movement    		
![](https://cdn.discordapp.com/attachments/857382160712466452/872321595635548160/posdveldacc_mov_square.png)
    ![](https://cdn.discordapp.com/attachments/857382160712466452/872315788437127188/xyz_mov_square_3d.png)
    ![](https://cdn.discordapp.com/attachments/857382160712466452/872315785152962560/xy_mov_square.png)
## Straight-line movement  
![](https://cdn.discordapp.com/attachments/857382160712466452/872299091428798564/acc_mov_linear.png)
    ![](https://cdn.discordapp.com/attachments/857382160712466452/872301214631620608/three_posd_veld_acc_mov_linear.png)
    ![](https://cdn.discordapp.com/attachments/857382160712466452/872313066891673600/xy_mov_linear_3d.png)
## Parable shaped movement
![](https://cdn.discordapp.com/attachments/857382160712466452/872322881894383716/posd_veld_acc_mov_parabola.png)
    ![](https://cdn.discordapp.com/attachments/857382160712466452/872323593126707260/xz_mov_parabola_3d.png)
## 360 degree rotation around the y axis 
![](https://cdn.discordapp.com/attachments/857382160712466452/872310307693920296/quat_quatc_eulerc_mov_linear.png)
## Contact
For any questions, please contact me <eduguibar@gmail.com> - Eduardo Guimarães 2021
