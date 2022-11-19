from machine import ADC, Pin


class System:
    def __init__(self):
        self.bat_adc = ADC(Pin(26))
        self.temp_adc = ADC(4)

    def temperature(self):
        """Returns the current Pico-Core temperature in degree celsius"""
        reading = self.temp_adc.read_u16() * 3.3 / 65535
        t = 27 - (reading - 0.706) / 0.001721
        return t

    def battery_voltage(self):
        """Returns the current battery voltage in V"""
        voltage = self.bat_adc.read_u16() * 3.3 / 65535 * 2
        return voltage

    def battery_percentage(self):
        """Returns the current battery charge in percent"""
        v = self.battery_voltage()
        percentage = (v - 3) * 100 / 1.2
        if percentage < 0: percentage = 0
        if percentage > 100: percentage = 100
        return percentage
