#!/bin/bash

if [[ "$1" == "on" ]];then
	cmd="set_powerstat 1"
elif [[ "$1" == "off" ]];then
	cmd="set_powerstat 0"
elif [[ "$1" == "f" ]];then
        cmd="f"
else
	cmd="get_powerstat"
fi

# was model 135

rigctl-local --model=1035 --rig-file=/dev/serial/by-id/usb-Silicon_Labs_CP2105_Dual_USB_to_UART_Bridge_Controller_00C99175-if00-port0 $cmd 
