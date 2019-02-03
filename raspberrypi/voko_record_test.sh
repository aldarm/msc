#!/bin/bash
export DISPLAY=':0.0'
at now + 1 minute -f voko_browser_refresh.sh
at now + 2 minute -f voko_app_start.sh
at now + 3 minute -f voko_start_record.sh
at now + 4 minute -f voko_stop_record.sh
at now + 5 minute -f voko_app_stop.sh
at now + 6 minute -f voko_copy_recording.sh
