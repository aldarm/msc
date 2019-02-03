#!/bin/bash
export DISPLAY=':0.0'
wmctrl -a vokoscreen
xte "keydown Control_L" "keydown Shift_L" "key F10" "keyup Control_L" "keyup Shift_L"
