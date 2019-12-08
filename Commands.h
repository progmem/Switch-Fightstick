/** \file
 *
 *  Header file for Commands.c.
 */

#pragma once

#include "Joystick.h"

typedef struct {
	Buttons_t button;
	uint16_t duration;
} Command; 

// The commands that run independently from a PC
// Store arrays in Flash memory to save a SRAM data capacity

// Infinity Watt
extern const Command inf_watt_commands[];
extern const int inf_watt_size;

// Inf ID lottery & Watt
extern const Command inf_id_watt_commands[];
extern const int inf_id_watt_size;
