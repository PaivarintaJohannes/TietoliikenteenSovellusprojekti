/*
 * Copyright (c) 2020 Libre Solar Technologies GmbH
 *
 * SPDX-License-Identifier: Apache-2.0
 */
#include <zephyr/logging/log.h>
#include <dk_buttons_and_leds.h>
#include <inttypes.h>
#include <stddef.h>
#include <stdint.h>
#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/util.h>
#include "adc.h"
#include <zephyr/device.h>
#include <zephyr/devicetree.h>

#include "confusion.h"



#define USER_LED1         	 	DK_LED1
#define USER_LED2          		DK_LED2
#define USER_LED3               DK_LED3
#define USER_LED4               DK_LED4

#define USER_BUTTON_1           DK_BTN1_MSK
#define USER_BUTTON_2           DK_BTN2_MSK
#define USER_BUTTON_3           DK_BTN3_MSK
#define USER_BUTTON_4           DK_BTN4_MSK

#define DEBUG 0 

static int direction = -1; //alkuun -1 jotta suunta pitää ite alustaa

                				 

LOG_MODULE_REGISTER(MAIN, LOG_LEVEL_INF);

static void button_changed(uint32_t button_state, uint32_t has_changed)
{

	if ((has_changed & USER_BUTTON_1) && (button_state & USER_BUTTON_1)) 
	{
		printk("Button 1 down\n");
		struct Measurement m = readADCValue();
		calculateDistanceToAllCentrePointsAndSelectWinner(m.x, m.y, m.z);
	}

	if ((has_changed & USER_BUTTON_2) && (button_state & USER_BUTTON_2)) 
	{
		printk("Button 2 down, resetting confusion matrix\n");
		resetConfusionMatrix();
		printConfusionMatrix();
	}		
	
	if ((has_changed & USER_BUTTON_3) && (button_state & USER_BUTTON_3)) 
	{	
		#if DEBUG
		direction = 0;
		makeHundredFakeClassifications();
		printConfusionMatrix();
		#else
        direction = (direction +1)%6;
		switch (direction)
		{
		case 0:
			printk("Suunta on nyt vaakataso +z (1)\n");
			break;
		case 1:
			printk("Suunta on nyt vaakataso -z (2)\n");
			break;
		case 2:
			printk("Suunta on nyt sivuttain +x (3)\n");
			break;
		case 3:
			printk("Suunta on nyt sivuttain -x (4)\n");
			break;
		case 4:
			printk("Suunta on nyt ylös -y (5)\n");
			break;
		case 5:
			printk("Suunta on nyt alas +y (6)\n");
			break;
		
		default:
		    printk("Wrong direction set!!!\n");
			break;
		}		
		#endif
	}		

	if ((has_changed & USER_BUTTON_4) && (button_state & USER_BUTTON_4))
	{
		if(direction < 0){
			printk("Määritä suunta ensin painamlla button3!\n"); //jottei zephyr kaatuis
		}else{
			makeOneClassificationAndUpdateConfusionMatrix(direction);
		}
		
	}
}


void main(void)	//init ledit ja adc 
{	
	int err;
	err = dk_leds_init();
	if (err) {
		LOG_ERR("LEDs init failed (err %d)\n", err);
		return;
	}

	err = dk_buttons_init(button_changed);
	if (err) {
		printk("Cannot init buttons (err: %d)\n", err);
		return;
	}
	
	
	if(initializeADC() != 0)
	{
	printk("ADC initialization failed!");
	return;
	}

	while (1) 
	{
		// ota seuraavat kommentit pois jos haluat että laite mittaa jatkuvasti ja luokittelee suunnan

		// struct Measurement m = readADCValue();
		// printk("x = %d,  y = %d,  z = %d\n",m.x,m.y,m.z);
		// calculateDistanceToAllCentrePointsAndSelectWinner(m.x, m.y, m.z);
		
		
		// vaiha sleep-aikoja jos haluat nopeampaa mittausta tms.

		k_sleep(K_MSEC(1000));
		
		dk_set_led_on(USER_LED1);
		dk_set_led_on(USER_LED2);
		dk_set_led_on(USER_LED3);
		dk_set_led_on(USER_LED4);
		 
		k_sleep(K_MSEC(1000));
		
		dk_set_led_off(USER_LED1);
		dk_set_led_off(USER_LED2);
		dk_set_led_off(USER_LED3);
		dk_set_led_off(USER_LED4);


	}
}


