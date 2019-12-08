/** \file
 *
 *  Header file for Commands.c.
 */

#ifndef _COMMAND_MCU_H_
#define _COMMAND_MCU_H_

#include "Joystick.h"

typedef enum {
	UP,
	DOWN,
	LEFT,
	RIGHT,
	X,
	Y,
	A,
	B,
	L,
	R,
	THROW,
	NOP,
	TRIGGERS,
    HOME,
} Buttons_t;

typedef struct {
	Buttons_t button;
	uint16_t duration;
} Command; 

// The commands that run independently from a PC
// Store arrays in Flash memory to save a SRAM data capacity

// Infinity Watt
Command inf_watt_commands[];
int inf_watt_size;



#endif