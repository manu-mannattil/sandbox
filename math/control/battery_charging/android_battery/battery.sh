#!/bin/sh

stdbuf -oL adb shell '
    while true
    do
        for f in /sys/class/power_supply/battery/*
        do
            [ -f "$f" ] || continue
            [ -r "$f" ] || continue
            echo "-*-"
            date +%s
            echo "-*-"
            echo "$f"
            echo "-*-"
            cat "$f" 2>/dev/null
        done
        sleep 5
    done
' >"battery-$(date +%s).dat"
