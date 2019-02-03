#!/bin/bash
kill $(ps aux | grep '[v]okoscreen' | awk '{print $2}')
