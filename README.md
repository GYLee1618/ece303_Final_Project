# ece303
This repository contains teaching material for ECE303.
_This API is subject to change and expansion!_

`channelsimulation.py` contains a simple API for a mock connection over an unreliable channel. `sender.py` and `receiver.py` are mock sender and receivers that use this unreliable channel. These are examples that do not properly handle the bit errors in the channel.

The channel simulator will simulate random bit errors, packet loss, and packet duplication.

## Assignment
The goal of this project is to develop a transport layer protocol that can successfully and quickly transmit bits over this unreliable channel. The protocol will be implemented in your versions `sender.py` and `receiver.py`. Your implementations should inherit from the Bogo{Receiver,Sender} classes in from this repository and override the receive() and send() methods.

## Grading
The grading policy for this project is as follows:
* Protocol design specifications (20%): a written report providing an overview of your specific protocol and design choices. A discussion of your protocol's features, tradeoffs and assumptions.
* Implementation documentation (10%): implementation specific documentation including libraries used and code annotations.
* Minimum functionality (60%): protocol must be able to transmit and acknowledge receipt of data packets through the unreliable channel.
* Competitive performance (10%): protocol performance will be determined relative to a reference implementation and to the class.

## Due Date
This project will be due Wednesday, May 2nd before midnight. This is the day before the final exam.
