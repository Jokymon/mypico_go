"""This module contains implementations for robot modifications. Before using
any of them, make sure to check the "Modifications" chapter for what kind of
changes need to be made on the robot.
"""
from machine import Pin, PWM


class Buzzer:
    """A buzzer class to implement sound output using a passive buzzer."""
    def __init__(self):
        self.buzzer = PWM(Pin(4))

    def play_tone(self, frequency):
        """Play a tone of the given frequency in Hz."""
        self.buzzer.duty_u16(1000)
        self.buzzer.freq(frequency)

    def be_quiet(self):
        self.buzzer.duty_u16(0)
