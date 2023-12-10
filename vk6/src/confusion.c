#include <zephyr/kernel.h>
#include <math.h>
#include "confusion.h"
#include "adc.h"
#include "keskipisteet.h"

/* 
  K-means algorithm should provide 6 center points with
  3 values x,y,z. Let's test measurement system with known
  center points. I.e. x,y,z are supposed to have only values
  1 = down and 2 = up
  
  CP matrix is thus the 6 center points got from K-means algoritm
  teaching process. This should actually come from include file like
  #include "KmeansCenterPoints.h"
  
  And measurements matrix is just fake matrix for testing purpose
  actual measurements are taken from ADC when accelerator is connected.
*/ 
float Suunta1_center[] = {1479.55357143, 1501.71428571, 1788.26785714}; 
float Suunta2_center[] = {1456.98214286, 1493.66071429, 1198.64285714};
float Suunta3_center[] = {1776.75123123, 1473.19642857, 1492.35714286};
float Suunta4_center[] = {1185.71428571, 1474.71428571, 1500.08928571};
float Suunta5_center[] = {1475.69642857, 1176.69642857, 1494.32142857};
float Suunta6_center[] = {1486.47272727, 1769.94545455, 1468.47272727};

int CP[6][3]={
	                     {1,0,0},
						 {2,0,0},
						 {0,1,0},
						 {0,2,0},
						 {0,0,1},
						 {0,0,2}
};

int measurements[6][3]={
	                     {1,0,0},
						 {2,0,0},
						 {0,1,0},
						 {0,2,0},
						 {0,0,1},
						 {0,0,2}
};

int CM[6][6]= {0};



void printConfusionMatrix(void)
{
	printk("Confusion matrix = \n");
	printk("   cp1 cp2 cp3 cp4 cp5 cp6\n");
	for(int i = 0;i<6;i++)
	{
		printk("cp%d %d   %d   %d   %d   %d   %d\n",i+1,CM[i][0],CM[i][1],CM[i][2],CM[i][3],CM[i][4],CM[i][5]);
	}
}

//debuggaamista varten feikkimittauksia
void makeHundredFakeClassifications(void)
{
   resetConfusionMatrix();

   for (int i = 0; i < 100; i++)
   {
      for (int actualClass = 1; actualClass <= 6; actualClass++)
      {
         int x = measurements[actualClass - 1][0];
         int y = measurements[actualClass - 1][1];
         int z = measurements[actualClass - 1][2];

         CM[actualClass - 1][actualClass - 1]++;
      }
   }
printConfusionMatrix();
}

//otetaan yks mittaus ja valitaan voittaja. sitte päivitetään cm
void makeOneClassificationAndUpdateConfusionMatrix(int direction)
{
    struct Measurement m = readADCValue();
    int result = calculateDistanceToAllCentrePointsAndSelectWinner(m.x, m.y, m.z);
    CM[direction][result-1]++;
    printk("Actual Direction: Suunta %d\n", direction+1);
    printk("Classified as: Suunta %d\n", result);
    printConfusionMatrix();
}

int calculateDistanceToAllCentrePointsAndSelectWinner(int x,int y,int z)
{
    float distances[6];
    
    // Lasketaan etäisyydet kaikkiin keskipisteisiin
    distances[0] = sqrt(pow(x - Suunta1_center[0], 2) + pow(y - Suunta1_center[1], 2) + pow(z - Suunta1_center[2], 2));
    distances[1] = sqrt(pow(x - Suunta2_center[0], 2) + pow(y - Suunta2_center[1], 2) + pow(z - Suunta2_center[2], 2));
    distances[2] = sqrt(pow(x - Suunta3_center[0], 2) + pow(y - Suunta3_center[1], 2) + pow(z - Suunta3_center[2], 2));
    distances[3] = sqrt(pow(x - Suunta4_center[0], 2) + pow(y - Suunta4_center[1], 2) + pow(z - Suunta4_center[2], 2));
    distances[4] = sqrt(pow(x - Suunta5_center[0], 2) + pow(y - Suunta5_center[1], 2) + pow(z - Suunta5_center[2], 2));
    distances[5] = sqrt(pow(x - Suunta6_center[0], 2) + pow(y - Suunta6_center[1], 2) + pow(z - Suunta6_center[2], 2));
   
   //Sitte valitaan lyhyin etäisyys ja sille kuuluva keskipiste
    int minIndex = 0;
    for (int i = 1; i < 6; i++)
    {
        if (distances[i] < distances[minIndex])
        {
            minIndex = i;
        }
    }
   //printataan keskipisteen suunta   
    int result = minIndex + 1; 
    		switch (result)
		{
		case 1:
			printk("Suunta 1 (Vaakataso)\n");
			break;
		case 2:
			printk("Suunta 2 (Vaakataso alaspäin)\n");
			break;
		case 3:
			printk("Suunta 3 (Sivuttain x-ylös)\n");
			break;
		case 4:
			printk("Suunta 4 (Sivuttain x-alas )\n");
			break;
		case 5:
			printk("Suunta 5 (Ylöspäin)\n");
			break;
		case 6:
			printk("Suunta 6 (Alaspäin)\n");
			break;
		}
      return result;
}


void resetConfusionMatrix(void)
{
	for(int i=0;i<6;i++)
	{ 
		for(int j = 0;j<6;j++)
		{
			CM[i][j]=0;
		}
	}
}

