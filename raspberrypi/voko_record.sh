#!/bin/bash
export DISPLAY=':0.0'
at 0558 -f voko_browser_refresh.sh
at 0559 -f voko_app_start.sh
at 0600 -f voko_start_record.sh
at 0915 -f voko_stop_record.sh
at 0920 -f voko_app_stop.sh
at 0925 -f voko_copy_recording.sh
