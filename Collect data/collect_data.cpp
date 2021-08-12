#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include <dirent.h>
#include <iostream>
#include <filesystem>
#include <sys/stat.h>
#include <sys/timeb.h>
#include <sys/time.h>
#include <wiringPi.h>

MPU6050 mpu;

#define OUTPUT_READABLE_ACCEL
#define OUTPUT_READABLE_GYRO
#define OUTPUT_READABLE_QUATERNION
//#define OUTPUT_READABLE_EULER
//#define OUTPUT_READABLE_YAWPITCHROLL
#define OUTPUT_READABLE_REALACCEL
//#define OUTPUT_READABLE_WORLDACCEL

// MPU control/status vars
bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 acc;        // [x, y, z]            accel sensor measurements
VectorInt16 gyr;        // [x, y, z]            gyroscopy sensor measurements
VectorInt16 accReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 accWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector

int lred=2,lgreen=0,button=3;
bool state=0;
// packet structure for InvenSense teapot demo
uint8_t teapotPacket[14] = { '$', 0x02, 0,0, 0,0, 0,0, 0,0, 0x00, 0x00, '\r', '\n' };

FILE    *arq_Accel,
        *arq_Gyro,
        *arq_Quaternions,
        *arq_Euler,
        *arq_YawPitchRoll,
        *arq_LinearAcc,
        *arq_WorldAcc;

std::string namepaste="";

struct timeval start, end, startc, endc,startb, endb;
long mtime, seconds, useconds,timestart,secondsb, usecondsb,timestartb;

// ================================================================
// ===                      INITIAL SETUP                       ===
// ================================================================

void setup() {
    // initialize device
    printf("Initializing I2C devices...\n");
    mpu.initialize();
    
    //wiringPi initialize
    wiringPiSetup();
    pinMode(lred,OUTPUT);
    pinMode(lgreen,OUTPUT);
    pinMode(button,INPUT);
    
    digitalWrite(lred,HIGH);
    digitalWrite(lgreen,LOW);
    
    // verify connection
    printf("Testing device connections...\n");
    printf(mpu.testConnection() ? "MPU6050 connection successful\n" : "MPU6050 connection failed\n");

    // load and configure the DMP
    printf("Initializing DMP...\n");
    devStatus = mpu.dmpInitialize();
    
    mpu.setXAccelOffset(-2757);
    mpu.setYAccelOffset(417);
    mpu.setZAccelOffset(1191);
    
    mpu.setXGyroOffset(-609);
    mpu.setYGyroOffset(-474);
    mpu.setZGyroOffset(415);
    // My offsets
    //            XAccel			     YAccel				   ZAccel			               XGyro			          YGyro			              ZGyro
    //[-2679,-2678] --> [-15,1]	[398,398] --> [-1,2]	[1205,1206] --> [16381,16391]	[-116,-115] --> [-4,2]	[69,70] --> [0,3]	[-93,-92] --> [0,3]
    

    // make sure it worked (returns 0 if so)
    if (devStatus == 0) {
        
        // turn on the DMP, now that it's ready
        printf("Enabling DMP...\n");
        mpu.setDMPEnabled(true);

        // enable Arduino interrupt detection
        //Serial.println(F("Enabling interrupt detection (Arduino external interrupt 0)..."));
        //attachInterrupt(0, dmpDataReady, RISING);
        mpuIntStatus = mpu.getIntStatus();

        // set our DMP Ready flag so the main loop() function knows it's okay to use it
        printf("DMP ready!\n");
        dmpReady = true;

        // get expected DMP packet size for later comparison
        packetSize = mpu.dmpGetFIFOPacketSize();
    } else {
        // ERROR!
        // 1 = initial memory load failed
        // 2 = DMP configuration updates failed
        // (if it's going to break, usually the code will be 1)
        printf("DMP Initialization failed (code %d)\n", devStatus);
    }
        
    gettimeofday(&start, NULL);
    gettimeofday(&startc, NULL);
}

// ================================================================
// ===                    MAIN PROGRAM LOOP                     ===
// ================================================================

void loop() {    
    gettimeofday(&end, NULL);
    seconds = end.tv_sec - start.tv_sec;
    useconds = end.tv_usec - start.tv_usec;
    timestart = ((seconds) * 1000 + useconds/1000.0) + 0.5;
    
    if(timestart>25000)
        digitalWrite(lgreen,HIGH);
        
    if (digitalRead(button)==true && timestart>25000){
        gettimeofday(&startb, NULL);
        
        while(digitalRead(button)){
            gettimeofday(&endb, NULL);
            secondsb = endb.tv_sec - startb.tv_sec;
            usecondsb = endb.tv_usec - startb.tv_usec;
            timestartb = ((secondsb) * 1000 + usecondsb/1000.0) + 0.5;
            
            if(timestartb>5000&&state!=1){
                execl("/usr/bin/sudo","sudo","shutdown","-h","now",NULL);
                return;
            }
        }
        
        if(state){
            fclose(arq_Accel);
            fclose(arq_Gyro);
            fclose(arq_Quaternions);
            //fclose(arq_Euler);
            //fclose(arq_YawPitchRoll);
            fclose(arq_LinearAcc);
            //fclose(arq_WorldAcc);
            digitalWrite(lred,HIGH);
        }else{
            digitalWrite(lred,LOW);
            DIR *d;
            struct dirent *dir;
            d = opendir ("/home/pi/MPU6050-Pi-Demo/Datas");
            int dir_len=0;
            if (d != NULL){
                while ((dir = readdir(d)) != NULL)
                    dir_len++;
                (void) closedir (d);
            } else{
                perror ("Couldn't open the directory");
            }  

            printf("%d",dir_len);
            namepaste="/home/pi/MPU6050-Pi-Demo/Datas/data_"+std::to_string(dir_len-2);
            printf(namepaste.c_str());

            std::string new_dir = namepaste;
            std::string existing_dir = ".";
            struct stat atributes;
            stat(existing_dir.c_str(), &atributes);
            mkdir(new_dir.c_str(), atributes.st_mode);
            
            std::string Data_Accel= namepaste + "/Data_Accel.txt",
            Data_Gyro= namepaste + "/Data_Gyro.txt",
            Data_Quaternions= namepaste + "/Data_Quaternions.txt",
            //Data_Euler= namepaste + "/Data_Euler.txt",
            //Data_YawPitchRoll= namepaste + "/Data_YawPitchRoll.txt",
            Data_LinearAcc= namepaste + "/Data_LinearAcc.txt";
            //Data_WorldAcc = namepaste + "/Data_WorldAcc.txt";
            
            arq_Accel = fopen(Data_Accel.c_str(),"wt");
            fprintf(arq_Accel,"time,accx,accy,accz\n");
            
            arq_Gyro = fopen(Data_Gyro.c_str(),"wt");
            fprintf(arq_Gyro,"time,gyrx,gyry,gyrz\n");
            
            arq_Quaternions = fopen(Data_Quaternions.c_str(),"wt");
            fprintf(arq_Quaternions,"time,qw,qx,qy,qz\n");
            
            //arq_Euler = fopen(Data_Euler.c_str(),"wt");
            //fprintf(arq_Euler,"time,alfa,beta,gama\n");
            
            //arq_YawPitchRoll = fopen(Data_YawPitchRoll.c_str(),"wt");
            //fprintf(arq_YawPitchRoll,"time,yaw,pitch,roll\n");
            
            arq_LinearAcc = fopen(Data_LinearAcc.c_str(),"wt");
            fprintf(arq_LinearAcc,"time,accx,accy,accz\n");
            
            //arq_WorldAcc = fopen(Data_WorldAcc.c_str(),"wt");
            //fprintf(arq_WorldAcc,"time,accx,accy,accz\n");
            
            gettimeofday(&startc, NULL);
        }
        state=!state;
        printf("Change state ");
        printf("%d\n",state);
    }
    // if programming failed, don't try to do anything
    if (!dmpReady) return;
    // get current FIFO count
    fifoCount = mpu.getFIFOCount();

    if (fifoCount == 1024) {
        // reset so we can continue cleanly
        mpu.resetFIFO();
        printf("FIFO overflow!\n");

    // otherwise, check for DMP data ready interrupt (this should happen frequently)
    } else if (fifoCount >= 42) {
        if(state)digitalWrite(lgreen,LOW);
        // read a packet from FIFO
        mpu.getFIFOBytes(fifoBuffer, packetSize);
        // get the time to create the millis function 
        gettimeofday(&endc, NULL);
        seconds = endc.tv_sec - startc.tv_sec;
        useconds = endc.tv_usec - startc.tv_usec;
        mtime = ((seconds) * 1000 + useconds/1000.0) + 0.5;
        // display time in milliseconds
        printf("\ntime %ld ms    ",mtime);
        
        #ifdef OUTPUT_READABLE_ACCEL
            // display accel values in easy matrix form: x y z
            mpu.dmpGetAccel(&acc, fifoBuffer);
            printf("accel  %6d %6d %6d    ",acc.x,acc.y,acc.z);
        #endif
        
        #ifdef OUTPUT_READABLE_GYRO
            // display accel values in easy matrix form: x y z
            mpu.dmpGetGyro(&gyr, fifoBuffer);
            printf("gryro  %6d %6d %6d    ",gyr.x,gyr.y,gyr.z);
        #endif
        
        #ifdef OUTPUT_READABLE_QUATERNION
            // display quaternion values in easy matrix form: w x y z
            mpu.dmpGetQuaternion(&q, fifoBuffer);
            //printf("quat %7.5f %7.5f %7.5f %7.5f    ", q.w,q.x,q.y,q.z);
            // save quaternion values 
            //fprintf(arq_Quaternions,"%ld,%7.2f,%7.2f,%7.2f,%7.2f\n",mtime,q.w,q.x,q.y,q.z);
        #endif

        #ifdef OUTPUT_READABLE_EULER
            // display Euler angles in degrees
            mpu.dmpGetQuaternion(&q, fifoBuffer);
            mpu.dmpGetEuler(euler, &q);
            printf("euler %7.2f %7.2f %7.2f    ", euler[0] * 180/M_PI, euler[1] * 180/M_PI, euler[2] * 180/M_PI);
            // save Euler angles 
            //fprintf(arq_Euler,"%ld,%7.2f,%7.2f,%7.2f\n", mtime, euler[0] * 180/M_PI, euler[1] * 180/M_PI, euler[2] * 180/M_PI);
        #endif

        #ifdef OUTPUT_READABLE_YAWPITCHROLL
            // display Euler angles in degrees
            mpu.dmpGetQuaternion(&q, fifoBuffer);
            mpu.dmpGetGravity(&gravity, &q);
            mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
            printf("ypr  %7.2f %7.2f %7.2f    ", ypr[0] * 180/M_PI, ypr[1] * 180/M_PI, ypr[2] * 180/M_PI);
        #endif

        #ifdef OUTPUT_READABLE_REALACCEL
            // display real acceleration, adjusted to remove gravity
            mpu.dmpGetQuaternion(&q, fifoBuffer);
            mpu.dmpGetAccel(&acc, fifoBuffer);
            mpu.dmpGetGravity(&gravity, &q);
            mpu.dmpGetLinearAccel(&accReal, &acc, &gravity);
            //printf("areal %6d %6d %6d    ", accReal.x, accReal.y, accReal.z);
            // save real acceleration 
            //fprintf(arq_LinearAcc,"%ld,%6d,%6d,%6d\n", mtime, aaReal.x, aaReal.y, aaReal.z);
        #endif

        #ifdef OUTPUT_READABLE_WORLDACCEL
            // display initial world-frame acceleration, adjusted to remove gravity
            // and rotated based on known orientation from quaternion
            mpu.dmpGetQuaternion(&q, fifoBuffer);
            mpu.dmpGetAccel(&acc, fifoBuffer);
            mpu.dmpGetGravity(&gravity, &q);
            mpu.dmpGetLinearAccelInWorld(&accWorld, &accReal, &q);
            printf("world  %6d %6d %6d     ",accWorld.x,accWorld.y,accWorld.z);
            // save initial word-frame acceleration
            //fprintf(arq_WorldAcc,"%ld,%7.2f,%7.2f,%7.2f\n", mtime, (double) aaWorld.x/4096, (double) aaWorld.y/4096, (double) (aaWorld.z-4096)/4096);
        #endif
    
        #ifdef OUTPUT_TEAPOT
            // display quaternion values in InvenSense Teapot demo format:
            teapotPacket[2] = fifoBuffer[0];
            teapotPacket[3] = fifoBuffer[1];
            teapotPacket[4] = fifoBuffer[4];
            teapotPacket[5] = fifoBuffer[5];
            teapotPacket[6] = fifoBuffer[8];
            teapotPacket[7] = fifoBuffer[9];
            teapotPacket[8] = fifoBuffer[12];
            teapotPacket[9] = fifoBuffer[13];
            Serial.write(teapotPacket, 14);
            teapotPacket[11]++; // packetCount, loops at 0xFF on purpose
        #endif
        printf("\n");
        if(state){
            fprintf(arq_Accel,"%ld,%6d,%6d,%6d\n",mtime,acc.x,acc.y,acc.z);
            fprintf(arq_Gyro,"%ld,%6d,%6d,%6d\n",mtime,gyr.x,gyr.y,gyr.z);
            fprintf(arq_Quaternions,"%ld,%7.5f,%7.5f,%7.5f,%7.5f\n",mtime,q.w,q.x,q.y,q.z);
            //fprintf(arq_Euler,"%ld,%7.5f,%7.5f,%7.5f\n", mtime, euler[0] * 180/M_PI, euler[1] * 180/M_PI, euler[2] * 180/M_PI);
            //fprintf(arq_YawPitchRoll,"%ld,%7.2f,%7.2f,%7.2f\n",mtime, ypr[0] * 180/M_PI, ypr[1] * 180/M_PI, ypr[2] * 180/M_PI);
            fprintf(arq_LinearAcc,"%ld,%6d,%6d,%6d\n", mtime,accReal.x,accReal.y,accReal.z);
            //fprintf(arq_WorldAcc,"%ld,%6d,%6d,%6d\n", mtime,accWorld.x,accWorld.y,accWorld.z);
        }
    }
}

int main() {
    setup();
    //usleep(100000);
    while(1){
        loop();
    }
    
    return 0;
}

