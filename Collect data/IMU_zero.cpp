#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include "I2Cdev.h"
#include <cstdio>
#include "MPU6050.h"

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 accelgyro;
//MPU6050 accelgyro(0x69); // <-- use for AD0 high


const char LBRACKET = '[';
const char RBRACKET = ']';
const char COMMA    = ',';
const char BLANK    = ' ';
const char PERIOD   = '.';

const int iAx = 0;
const int iAy = 1;
const int iAz = 2;
const int iGx = 3;
const int iGy = 4;
const int iGz = 5;

const int usDelay = 3150;   // empirical, to hold sampling to 200 Hz
const int NFast =  1000;    // the bigger, the better (but slower)
const int NSlow = 10000;    // ..
const int LinesBetweenHeaders = 5;


int LowValue[6];
int HighValue[6];
int Smoothed[6];
int LowOffset[6];
int HighOffset[6];
int Target[6];
int LinesOut;
int N;


void ForceHeader()
{ 
	LinesOut = 99; 
}
    
void GetSmoothed()
{ 
	int16_t RawValue[6];
	int i;
	long Sums[6];
	for (i = iAx; i <= iGz; i++)
	{ 
		Sums[i] = 0; 
	}
	//    unsigned long Start = micros();

	for (i = 1; i <= N; i++)
	{ 
		// get sums
		accelgyro.getMotion6(&RawValue[iAx], &RawValue[iAy], &RawValue[iAz], 
							&RawValue[iGx], &RawValue[iGy], &RawValue[iGz]);
		if ((i % 500) == 0)
		{
			printf("%c", PERIOD);
		}
		//delayMicroseconds(usDelay);
		for (int j = iAx; j <= iGz; j++)
		{
			Sums[j] = Sums[j] + RawValue[j];
		}
	} // get sums
	//    unsigned long usForN = micros() - Start;
	//    printf(" reading at %d Hz\n", 1000000/((usForN+N/2)/N));
	for (i = iAx; i <= iGz; i++)
	{ 
		Smoothed[i] = (Sums[i] + N/2) / N ; 
	}
} // GetSmoothed

void Initialize()
{
	// initialize device
	printf("Initializing I2C devices...\n");
	accelgyro.initialize();

	// verify connection
	printf("Testing device connections...\n");
	if(!accelgyro.testConnection()) 
	{
		printf("MPU6050 connection failed\n");
		return;
	}

	printf("MPU6050 connection successful\n"); 
	accelgyro.initialize();
	printf("Initialization done!\n");
} // Initialize

void SetAveraging(int NewN)
{ 
	N = NewN;
	printf("averaging %d  readings each time\n", N);
} // SetAveraging

void SetOffsets(int TheOffsets[6])
{ 
	accelgyro.setXAccelOffset(TheOffsets [iAx]);
	accelgyro.setYAccelOffset(TheOffsets [iAy]);
	accelgyro.setZAccelOffset(TheOffsets [iAz]);
	accelgyro.setXGyroOffset (TheOffsets [iGx]);
	accelgyro.setYGyroOffset (TheOffsets [iGy]);
	accelgyro.setZGyroOffset (TheOffsets [iGz]);
} // SetOffsets

void ShowProgress()
{ 
	if (LinesOut >= LinesBetweenHeaders)
	{ 
		// show header
		printf("\tXAccel\t\t\tYAccel\t\t\t\tZAccel\t\t\tXGyro\t\t\tYGyro\t\t\tZGyro\n");
		LinesOut = 0;
	} // show header
	printf("%c", BLANK);
	for (int i = iAx; i <= iGz; i++)
	{ 
		printf("%c%d%c%d] --> [%d%c%d", LBRACKET, LowOffset[i], COMMA, HighOffset[i],
						LowValue[i], COMMA, HighValue[i]);
		if (i == iGz)
		{ 
			printf("%c\n", RBRACKET); 
		}
		else
		{ 
			printf("]\t"); 
		}
	}
	LinesOut++;
} // ShowProgress

void PullBracketsIn()
{ 
	bool AllBracketsNarrow;
	bool StillWorking;
	int NewOffset[6];

	printf("\nclosing in:\n");
	AllBracketsNarrow = false;
	ForceHeader();
	StillWorking = true;
	while (StillWorking) 
	{ 
		StillWorking = false;
		if (AllBracketsNarrow && (N == NFast))
		{ 
			SetAveraging(NSlow); 
		}
		else
		{ 
			AllBracketsNarrow = true; 
		}// tentative
		for (int i = iAx; i <= iGz; i++)
		{ 
			if (HighOffset[i] <= (LowOffset[i]+1))
			{ 
			NewOffset[i] = LowOffset[i]; 
			}
			else
			{ 
			// binary search
				StillWorking = true;
				NewOffset[i] = (LowOffset[i] + HighOffset[i]) / 2;
				if (HighOffset[i] > (LowOffset[i] + 10))
				{ 
					AllBracketsNarrow = false; 
				}
			} // binary search
		}
		SetOffsets(NewOffset);
		GetSmoothed();
		for (int i = iAx; i <= iGz; i++)
		{ 
			// closing in
			if (Smoothed[i] > Target[i])
			{ 
				// use lower half
				HighOffset[i] = NewOffset[i];
				HighValue[i] = Smoothed[i];
			} // use lower half
			else
			{ 
				// use upper half
				LowOffset[i] = NewOffset[i];
				LowValue[i] = Smoothed[i];
			} // use upper half
		} // closing in
		ShowProgress();
	} // still working
} // PullBracketsIn

void PullBracketsOut()
{ 
	bool Done = false;
	int NextLowOffset[6];
	int NextHighOffset[6];

	printf("expanding:\n");
	ForceHeader();

	while (!Done)
	{
		Done = true;
		SetOffsets(LowOffset);
		GetSmoothed();
		for (int i = iAx; i <= iGz; i++)
		{
			// got low values
			LowValue[i] = Smoothed[i];
			if (LowValue[i] >= Target[i])
			{
				Done = false;
				NextLowOffset[i] = LowOffset[i] - 1000;
			}
			else
			{
				NextLowOffset[i] = LowOffset[i]; 
			}
		} // got low values

		SetOffsets(HighOffset);
		GetSmoothed();
		for (int i = iAx; i <= iGz; i++)
		{
			// got high values
			HighValue[i] = Smoothed[i];
			if (HighValue[i] <= Target[i])
			{
				Done = false;
				NextHighOffset[i] = HighOffset[i] + 1000;
			}
			else
			{ 
				NextHighOffset[i] = HighOffset[i]; 
			}
		} // got high values
		ShowProgress();
		for (int i = iAx; i <= iGz; i++)
		{ 
			LowOffset[i] = NextLowOffset[i];   // had to wait until ShowProgress done
			HighOffset[i] = NextHighOffset[i]; // ..
		}
	} // keep going
} // PullBracketsOut



int main(int argc, char **argv)
{ 
	Initialize();
	for (int i = iAx; i <= iGz; i++)
	{ // set targets and initial guesses
		Target[i] = 0; // must fix for ZAccel 
		HighOffset[i] = 0;
		LowOffset[i] = 0;
	} // set targets and initial guesses
	Target[iAz] = 16384;
	SetAveraging(NFast);
	PullBracketsOut();
	PullBracketsIn();

	printf("-------------- done --------------\n\n");
	return 0;
}


