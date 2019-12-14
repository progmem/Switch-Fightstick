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

bool GetNextReportFromCommands(const Command* const commands, int step_size, USB_JoystickReport_Input_t* const ReportData);

// The commands that run independently from a PC
// Store arrays in Flash memory to save a SRAM data capacity

// controller sync (use for ease of debugging)
extern const Command sync[];
extern const int sync_size;

// controller unsync
extern const Command unsync[];
extern const int unsync_size;

// Mash A Button
extern const Command mash_a_commands[];
extern const int mash_a_size;

// Infinity Watt
extern const Command inf_watt_commands[];
extern const int inf_watt_size;

// Inf ID lottery & Watt
extern const Command inf_id_watt_commands[];
extern const int inf_id_watt_size;
