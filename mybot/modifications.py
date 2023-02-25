from machine import Pin, PWM


class Buzzer:
    def __init__(self):
        self.buzzer = PWM(Pin(4))

    def play_tone(self, frequency):
        self.buzzer.duty_u16(1000)
        self.buzzer.freq(frequency)

    def be_quiet(self):
        self.buzzer.duty_u16(0)
