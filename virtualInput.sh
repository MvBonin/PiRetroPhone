#!/bin/bash

#Github toadjaune/pulseaudio-config

# This script sets up pulseaudio virtual devices
# The following variables must be set to the names of your own microphone and speakers devices
# You can find their names with the following commands :
# pacmd list-sources
# pacmd list-source-outputs
# Use pavucontrol to make tests for your setup and to make the runtime configuration
# Route your audio source to virtual1
# Record your sound (videoconference) from virtual2.monitor

MICROPHONE="alsa_input.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.mono-fallback"
SPEAKERS="alsa_output.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-stereo"


# Create the null sinks
# virtual1 gets your audio sources (mplayer ...) that you want to hear and share
# virtual2 gets all the audio you want to share (virtual1 + micro)
pactl load-module module-null-sink sink_name=virtual1 sink_properties=device.description="virtual1"
pactl load-module module-null-sink sink_name=virtual2 sink_properties=device.description="virtual2"

# Now create the loopback devices, all arguments are optional and can be configured with pavucontrol
pactl load-module module-loopback source=virtual1.monitor sink=$SPEAKERS latency_msec=1
pactl load-module module-loopback source=virtual1.monitor sink=virtual2 latency_msec=1
pactl load-module module-loopback source=$MICROPHONE sink=virtual2 latency_msec=1

# If you struggle to find the correct values of your physical devices, you can
# also simply leave these undefined, and configure everything manually via pavucontrol
#pactl load-module module-loopback source=virtual1.monitor
#pactl load-module module-loopback source=virtual1.monitor sink=virtual2
#pactl load-module module-loopback sink=virtual2

pacmd "set-default-source virtual2.monitor"
