# Optimal charging protocols for an Android phone

Basically finds out how to charge an Android phone's battery using
optimal control.

The `battery.sh` shell script continuously reads the various files under
`/sys/class/power_supply/battery/` and stores the result in a file.
(You need to set up ADB over WiFi for this to work.)
The resulting file is then read by `optimal.py`, which finds the
optimal current based on the resistance vs SOC curve.  See the notes on
lead-acid battery charging for more details.
