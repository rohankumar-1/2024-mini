#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

tones = { # also from https://www.coderdojotc.org/micropython/sound/04-play-scale/
"B0": 31,"C1": 33,"CS1": 35,"D1": 37,"DS1": 39,"E1": 41,"F1": 44,"FS1": 46,
"G1": 49,"GS1": 52,"A1": 55,"AS1": 58,"B1": 62,"C2": 65,
"CS2": 69,"D2": 73,"DS2": 78,"E2": 82,"F2": 87,"FS2": 93,"G2": 98,
"GS2": 104,"A2": 110,"AS2": 117,"B2": 123,"C3": 131,"CS3": 139,
"D3": 147,"DS3": 156,"E3": 165,"F3": 175,"FS3": 185,
"G3": 196,"GS3": 208,"A3": 220,"AS3": 233,"B3": 247,"C4": 262,"CS4": 277,"D4": 294,"DS4": 311,
"E4": 330,"F4": 349,"FS4": 370,"G4": 392,"GS4": 415,"A4": 440,"AS4": 466,"B4": 494,"C5": 523,"CS5": 554,"D5": 587,"DS5": 622,"E5": 659,"F5": 698,
"FS5": 740,"G5": 784,"GS5": 831,"A5": 880,"AS5": 932,"B5": 988,"C6": 1047,"CS6": 1109,"D6": 1175,"DS6": 1245,"E6": 1319,"F6": 1397,"FS6": 1480,"G6": 1568,"GS6": 1661,
"A6": 1760,"AS6": 1865,"B6": 1976,"C7": 2093,"CS7": 2217,"D7": 2349,"DS7": 2489,"E7": 2637,"F7": 2794,"FS7": 2960,"G7": 3136,"GS7": 3322,"A7": 3520,
"AS7": 3729,"B7": 3951,"C8": 4186,"CS8": 4435,"D8": 4699,"DS8": 4978
}

bpm = 148
secondsPerBeat: float = 60/bpm

duration: float = 0.008  # seconds

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))

def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(100)
    speaker.freq(frequency)
    utime.sleep(duration)

def playMeasure(note1, note2, note3):
    for i in range(int((secondsPerBeat/duration)/3)):
        playtone(tones[note1], duration)
        playtone(tones[note2], duration)
        playtone(tones[note3], duration)

def quiet():
    speaker.duty_u16(0)

# plays "Fein" by Travis Scott
while(1):
    for i in range(3):
        playMeasure("FS6", "DS6", "AS5")
    for i in range(5):
        playMeasure("F6", "DS6", "AS5")
    for i in range(3):
        playMeasure("FS6", "DS6", "AS5")
    for i in range(5):
        playMeasure("F6", "DS6", "AS5")
    for i in range(3):
        playMeasure("DS6", "B5", "GS5")
    for i in range(5):
        playMeasure("DS6", "AS5", "GS5")
    for i in range(3):
        playMeasure("DS6", "B5", "GS5")
    for i in range(5):
        playMeasure("DS6", "AS5", "GS5")
