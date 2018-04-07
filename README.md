# ece303
This repository contains teaching material for ECE303.
_This API is subject to change and expansion!_

`channelsimulation.py` contains a simple API for a mock connection over an unreliable channel. `sender.py` and `receiver.py` are mock sender and receivers that use this unreliable channel. These are examples that do not properly handle the bit errors in the channel.

The channel simulator will simulate random bit errors, packet loss, and packet duplication.
