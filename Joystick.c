/*
             LUFA Library
     Copyright (C) Dean Camera, 2014.

  dean [at] fourwalledcubicle [dot] com
           www.lufa-lib.org
*/

/*
  Copyright 2014  Dean Camera (dean [at] fourwalledcubicle [dot] com)

  Permission to use, copy, modify, distribute, and sell this
  software and its documentation for any purpose is hereby granted
  without fee, provided that the above copyright notice appear in
  all copies and that both that the copyright notice and this
  permission notice and warranty disclaimer appear in supporting
  documentation, and that the name of the author not be used in
  advertising or publicity pertaining to distribution of the
  software without specific, written prior permission.

  The author disclaims all warranties with regard to this
  software, including all implied warranties of merchantability
  and fitness.  In no event shall the author be liable for any
  special, indirect or consequential damages or any damages
  whatsoever resulting from loss of use, data or profits, whether
  in an action of contract, negligence or other tortious action,
  arising out of or in connection with the use or performance of
  this software.
*/

/** \file
 *
 *  Main source file for the Joystick demo. This file contains the main tasks of the demo and
 *  is responsible for the initial application hardware configuration.
 */

#include "Joystick.h"

/*** Button Mappings ****
The Pokken controller exposes 13 buttons, of which only 10 have physical
controls available. The Switch is fairly loose regarding the use of
descriptors, and can be expanded to a full 16 buttons (at least).

Of these 16 buttons, the Switch has 14 of them physically available: the four
face buttons, the four shoulder buttons, -/+, the stick clicks, Home, and
Capture (in that order). A curious thought to explore would be to see if we
can go beyond two bytes; along with the HAT, the Switch Pro Controller also
has an additional nibble of buttons available (which may correspond to Up,
Down, Left and Right as specific buttons instead of a 'directional unit').
**** Button Mappings ***/
#define PAD_Y       0x01
#define PAD_B       0x02
#define PAD_A       0x04
#define PAD_X       0x08
#define PAD_L       0x10
#define PAD_R       0x20
#define PAD_ZL      0x40
#define PAD_ZR      0x80
#define PAD_SELECT  0x100 
#define PAD_START   0x200
#define PAD_LS      0x400
#define PAD_RS      0x800
#define PAD_HOME    0x1000
#define PAD_CAPTURE 0x2000

// The following buttons map to buttons within Pokken, as most of this code was originally used for my Pokken fightstick.
#define POKKEN_PKMNMOVE PAD_A
#define POKKEN_JUMP     PAD_B
#define POKKEN_HOMING   PAD_X
#define POKKEN_LONGDIST PAD_Y
#define POKKEN_SUPPORT  PAD_L
#define POKKEN_GUARD    PAD_R

#define POKKEN_COUNTER (PAD_X | PAD_A)
#define POKKEN_GRAB    (PAD_Y | PAD_B)
#define POKKEN_BURST   (PAD_L | PAD_R)

/*
The following ButtonMap variable defines all possible buttons within the
original 13 bits of space, along with attempting to investigate the remaining
3 bits that are 'unused'. This is what led to finding that the 'Capture'
button was operational on the stick.
*/
uint16_t ButtonMap[16] = {
	0x01,
	0x02,
	0x04,
	0x08,
	0x10,
	0x20,
	0x40,
	0x80,
	0x100,
	0x200,
	0x400,
	0x800,
	0x1000,
	0x2000,
	0x4000,
	0x8000,
};

/*** Debounce ****
The following is some -really bad- debounce code. I have a more robust library
that I've used in other personal projects that would be a much better use
here, especially considering that this is a stick indented for use with arcade
fighters.

This code exists solely to actually test on. This will eventually be replaced.
**** Debounce ***/
// Quick debounce hackery!
// We're going to capture each port separately and store the contents into a 32-bit value.
uint32_t pb_debounce = 0;
uint32_t pd_debounce = 0;

// We also need a port state capture. We'll use a 16-bit value for this.
uint16_t bd_state = 0;

// We'll also give us some useful macros here.
#define PINB_DEBOUNCED ((bd_state >> 0) & 0xFF)
#define PIND_DEBOUNCED ((bd_state >> 8) & 0xFF) 

// So let's do some debounce! Lazily, and really poorly.
void debounce_ports(void) {
	// We'll shift the current value of the debounce down one set of 8 bits. We'll also read in the state of the pins.
	pb_debounce = (pb_debounce << 8) + PINB;
	pd_debounce = (pd_debounce << 8) + PIND;

	// We'll then iterate through a simple for loop.
	for (int i = 0; i < 8; i++) {
		if ((pb_debounce & (0x1010101 << i)) == (0x1010101 << i)) // wat
			bd_state |= (1 << i);
		else if ((pb_debounce & (0x1010101 << i)) == (0))
			bd_state &= ~(uint16_t)(1 << i);

		if ((pd_debounce & (0x1010101 << i)) == (0x1010101 << i))
			bd_state |= (1 << (8 + i));
		else if ((pd_debounce & (0x1010101 << i)) == (0))
			bd_state &= ~(uint16_t)(1 << (8 + i));
	}
}

/** Main program entry point. This routine configures the hardware required by the application, then
 *  enters a loop to run the application tasks in sequence.
 */
int main(void)
{
	SetupHardware();
	GlobalInterruptEnable();

	for (;;)
	{
		HID_Task();
		USB_USBTask();
		debounce_ports();
	}
}

/** Configures the board hardware and chip peripherals for the demo's functionality. */
void SetupHardware(void)
{
	/* Disable watchdog if enabled by bootloader/fuses */
	MCUSR &= ~(1 << WDRF);
	wdt_disable();

	DDRD  &= ~0xFF;
	PORTD |=  0xFF;

	DDRB  &= ~0xFF;
	PORTB |=  0xFF;

	/* Disable clock division */
	clock_prescale_set(clock_div_1);
	/* Hardware Initialization */
	USB_Init();
}

/** Event handler for the USB_Connect event. This indicates that the device is enumerating via the status LEDs and
 *  starts the library USB task to begin the enumeration and USB management process.
 */
void EVENT_USB_Device_Connect(void)
{
	/* Indicate USB enumerating */
}

/** Event handler for the USB_Disconnect event. This indicates that the device is no longer connected to a host via
 *  the status LEDs and stops the USB management and joystick reporting tasks.
 */
void EVENT_USB_Device_Disconnect(void)
{
	/* Indicate USB not ready */
}

/** Event handler for the USB_ConfigurationChanged event. This is fired when the host set the current configuration
 *  of the USB device after enumeration - the device endpoints are configured and the joystick reporting task started.
 */
void EVENT_USB_Device_ConfigurationChanged(void)
{
	bool ConfigSuccess = true;

	/* Setup HID Report Endpoint */
	ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_OUT_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);
	ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_IN_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);

	/* Indicate endpoint configuration success or failure */
}

/** Event handler for the USB_ControlRequest event. This is used to catch and process control requests sent to
 *  the device from the USB host before passing along unhandled control requests to the library for processing
 *  internally.
 */
void EVENT_USB_Device_ControlRequest(void)
{
	/* Handle HID Class specific requests */
	switch (USB_ControlRequest.bRequest)
	{
		case HID_REQ_GetReport:
			if (USB_ControlRequest.bmRequestType == (REQDIR_DEVICETOHOST | REQTYPE_CLASS | REQREC_INTERFACE))
			{
				USB_JoystickReport_Input_t JoystickReportData;

				/* Create the next HID report to send to the host */
				GetNextReport(&JoystickReportData);

				Endpoint_ClearSETUP();

				/* Write the report data to the control endpoint */
				Endpoint_Write_Control_Stream_LE(&JoystickReportData, sizeof(JoystickReportData));
				Endpoint_ClearOUT();
			}

			break;
		case HID_REQ_SetReport:
			if (USB_ControlRequest.bmRequestType == (REQDIR_HOSTTODEVICE | REQTYPE_CLASS | REQREC_INTERFACE))
			{
				USB_JoystickReport_Output_t TempData;

				Endpoint_ClearSETUP();

				/* Read the report data from the control endpoint */
				Endpoint_Read_Control_Stream_LE(&TempData, sizeof(TempData));
				Endpoint_ClearIN();
			}

			break;
	}
}

/** Fills the given HID report data structure with the next HID report to send to the host.
 *
 *  \param[out] ReportData  Pointer to a HID report data structure to be filled
 *
 *  \return Boolean \c true if the new report differs from the last report, \c false otherwise
 */
void GetNextReport(USB_JoystickReport_Input_t* const ReportData)
{
	// All of this code here is handled -really poorly-, and should be replaced with something a bit more production-worthy.
	uint16_t buf_button   = 0x00;
	uint8_t  buf_joystick = 0x00;

	/* Clear the report contents */
	memset(ReportData, 0, sizeof(USB_JoystickReport_Input_t));

	buf_button   = (~PIND_DEBOUNCED & 0xFF) << (~PINB_DEBOUNCED & 0x08 ? 8 : 0);
	buf_joystick = (~PINB_DEBOUNCED & 0xFF);

	for (int i = 0; i < 16; i++) {
		if (buf_button & (1 << i))
			ReportData->Button |= ButtonMap[i];
	}

	if (buf_joystick & 0x10)
		ReportData->X = 0;
	else if (buf_joystick & 0x20)
		ReportData->X = 255;
	else
		ReportData->X = 128;

	if (buf_joystick & 0x80)
		ReportData->Y = 0;
	else if (buf_joystick & 0x40)
		ReportData->Y = 255;
	else
		ReportData->Y = 128;

	switch(buf_joystick & 0xF0) {
		case 0x80: // Top
			ReportData->HAT = 0x00;
			break;
		case 0xA0: // Top-Right
			ReportData->HAT = 0x01;
			break;
		case 0x20: // Right
			ReportData->HAT = 0x02;
			break;
		case 0x60: // Bottom-Right
			ReportData->HAT = 0x03;
			break;
		case 0x40: // Bottom
			ReportData->HAT = 0x04;
			break;
		case 0x50: // Bottom-Left
			ReportData->HAT = 0x05;
			break;
		case 0x10: // Left
			ReportData->HAT = 0x06;
			break;
		case 0x90: // Top-Left
			ReportData->HAT = 0x07;
			break;
		default:
			ReportData->HAT = 0xff;
	}
}

/** Function to manage HID report generation and transmission to the host. */
void HID_Task(void)
{
	/* Device must be connected and configured for the task to run */
	if (USB_DeviceState != DEVICE_STATE_Configured)
	  return;

	/* Select the Joystick Report Endpoint */
	Endpoint_SelectEndpoint(JOYSTICK_OUT_EPADDR);

	/* Check to see if the host is ready for another packet */
	if (Endpoint_IsOUTReceived())
	{
		/* Check to see if the packet contains data */
		if (Endpoint_IsReadWriteAllowed())
		{
			USB_JoystickReport_Output_t TempData;
			/* Read Generic Report Data */
			// We're not actually doing anything with this data, simply reading it in and continuing on our way.
			Endpoint_Read_Stream_LE(&TempData, sizeof(TempData), NULL);
		}
		Endpoint_ClearOUT();
	}

	/* Select the Joystick Report Endpoint */
	Endpoint_SelectEndpoint(JOYSTICK_IN_EPADDR);

	/* Check to see if the host is ready for another packet */
	if (Endpoint_IsINReady())
	{
		USB_JoystickReport_Input_t JoystickReportData;

		/* Create the next HID report to send to the host */
		GetNextReport(&JoystickReportData);

		/* Write Joystick Report Data */
		Endpoint_Write_Stream_LE(&JoystickReportData, sizeof(JoystickReportData), NULL);

		/* Finalize the stream transfer to send the last packet */
		Endpoint_ClearIN();

		/* Clear the report data afterwards */
		memset(&JoystickReportData, 0, sizeof(JoystickReportData));
	}
}

