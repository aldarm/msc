#!/bin/bash
export DISPLAY=':0.0'
at 1525 -f voko_browser_refresh.sh
at 1529 -f voko_app_start.sh
at 1530 -f voko_start_record.sh
at 1830 -f voko_stop_record.sh
at 1840 -f voko_app_stop.sh
at 1850 -f voko_copy_recording.sh
