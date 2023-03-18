from machine import I2C
import machine
import time


ADS_I2C_ADDRESS = 0x48

# Pointer Register
ADS_POINTER_CONVERT = 0x00
ADS_POINTER_CONFIG = 0x01
ADS_POINTER_LOWTHRESH = 0x02
ADS_POINTER_HIGHTHRESH = 0x03

# Config Register
ADS_CONFIG_OS_BUSY = 0x0000      # Device is currently performing a conversion
ADS_CONFIG_OS_NOBUSY = 0x8000      # Device is not currently performing a conversion
ADS_CONFIG_OS_SINGLE_CONVERT = 0x8000      # Start a single conversion (when in power-down state)
ADS_CONFIG_OS_NO_EFFECT = 0x0000      # No effect
ADS_CONFIG_MUX_MUL_0_1 = 0x0000      # Input multiplexer,AINP = AIN0 and AINN = AIN1(default)
ADS_CONFIG_MUX_MUL_0_3 = 0x1000      # Input multiplexer,AINP = AIN0 and AINN = AIN3
ADS_CONFIG_MUX_MUL_1_3 = 0x2000      # Input multiplexer,AINP = AIN1 and AINN = AIN3
ADS_CONFIG_MUX_MUL_2_3 = 0x3000      # Input multiplexer,AINP = AIN2 and AINN = AIN3
ADS_CONFIG_MUX_SINGLE_0 = 0x4000      # SINGLE,AIN0
ADS_CONFIG_MUX_SINGLE_1 = 0x5000      # SINGLE,AIN1
ADS_CONFIG_MUX_SINGLE_2 = 0x6000      # SINGLE,AIN2
ADS_CONFIG_MUX_SINGLE_3 = 0x7000      # SINGLE,AIN3
ADS_CONFIG_PGA_6144 = 0x0000      # Gain= +/- 6.144V
ADS_CONFIG_PGA_4096 = 0x0200      # Gain= +/- 4.096V
ADS_CONFIG_PGA_2048 = 0x0400      # Gain= +/- 2.048V(default)
ADS_CONFIG_PGA_1024 = 0x0600      # Gain= +/- 1.024V
ADS_CONFIG_PGA_512 = 0x0800      # Gain= +/- 0.512V
ADS_CONFIG_PGA_256 = 0x0A00      # Gain= +/- 0.256V
ADS_CONFIG_MODE_CONTINUOUS = 0x0000      # Device operating mode:Continuous-conversion mode
ADS_CONFIG_MODE_NOCONTINUOUS = 0x0100      # Device operating mode：Single-shot mode or power-down state (default)
ADS_CONFIG_DR_RATE_128 = 0x0000      # Data rate=128SPS
ADS_CONFIG_DR_RATE_250 = 0x0020      # Data rate=250SPS
ADS_CONFIG_DR_RATE_490 = 0x0040      # Data rate=490SPS
ADS_CONFIG_DR_RATE_920 = 0x0060      # Data rate=920SPS
ADS_CONFIG_DR_RATE_1600 = 0x0080      # Data rate=1600SPS
ADS_CONFIG_DR_RATE_2400 = 0x00A0      # Data rate=2400SPS
ADS_CONFIG_DR_RATE_3300 = 0x00C0      # Data rate=3300SPS
ADS_CONFIG_COMP_MODE_WINDOW = 0x0010      # Comparator mode：Window comparator
ADS_CONFIG_COMP_MODE_TRADITIONAL = 0x0000      # Comparator mode：Traditional comparator (default)
ADS_CONFIG_COMP_POL_LOW = 0x0000      # Comparator polarity：Active low (default)
ADS_CONFIG_COMP_POL_HIGH = 0x0008      # Comparator polarity：Active high
ADS_CONFIG_COMP_LAT = 0x0004      # Latching comparator
ADS_CONFIG_COMP_NONLAT = 0x0000      # Nonlatching comparator (default)
ADS_CONFIG_COMP_QUE_ONE = 0x0000      # Assert after one conversion
ADS_CONFIG_COMP_QUE_TWO = 0x0001      # Assert after two conversions
ADS_CONFIG_COMP_QUE_FOUR = 0x0002      # Assert after four conversions
ADS_CONFIG_COMP_QUE_NON = 0x0003      # Disable comparator and set ALERT/RDY pin to high-impedance (default)


class ADS1015(object):
    """Encapsulation of the external AD converter ADS1015."""
    def __init__(self, i2c_bus=1, addr=ADS_I2C_ADDRESS):
        self.i2c = I2C(i2c_bus)
        self.addr = addr

    def set_channel(self, channel):
        """Configure the ADC to read a single value from the specified
        channel."""
        ads_config = (
            ADS_CONFIG_MODE_NOCONTINUOUS |      # Single-shot mode
            ADS_CONFIG_PGA_4096 |               # Gain= +/- 4.096V
            ADS_CONFIG_COMP_QUE_NON |           # Disable comparator
            ADS_CONFIG_COMP_NONLAT |            # Nonlatching comparator
            ADS_CONFIG_COMP_POL_LOW |           # Comparator polarity Active low
            ADS_CONFIG_COMP_MODE_TRADITIONAL |  # Traditional comparator
            ADS_CONFIG_DR_RATE_3300             # Data rate=3300 SPS
            )
        if channel == 0:
            ads_config |= ADS_CONFIG_MUX_SINGLE_0
        elif channel == 1:
            ads_config |= ADS_CONFIG_MUX_SINGLE_1
        elif channel == 2:
            ads_config |= ADS_CONFIG_MUX_SINGLE_2
        elif channel == 3:
            ads_config |= ADS_CONFIG_MUX_SINGLE_3
        ads_config |= ADS_CONFIG_OS_SINGLE_CONVERT
        self._write_word(ADS_POINTER_CONFIG, ads_config)

    def read_u16(self, channel):
        """Read a 16-bit ADC value from the previously set channel.

        The values read from the ADC are normalized to a full-range
        16-bit value.
        """
        self.set_channel(channel)
        time.sleep(0.003)
        value = self._read_word(ADS_POINTER_CONVERT) >> 4
        value = value*0x10000/1650.0
        return value

    def _read_word(self, cmd):
        data = self.i2c.readfrom_mem(self.addr, cmd, 2)
        return ((data[0] * 256) + data[1])

    def _write_word(self, cmd, val):
        temp = [0, 0]
        temp[1] = val & 0xFF
        temp[0] = (val & 0xFF00) >> 8
        self.i2c.writeto_mem(self.addr, cmd, bytes(temp))


class LineSensor(object):
    def __init__(self):
        self.num_sensors = 5
        self.last_value = 0
        self.adc1 = machine.ADC(27)
        self.adc5 = machine.ADC(28)
        self.adc = ADS1015()

        self.reset_calibration()

    def analog_read(self):
        """Read the sensor values from all five line tracking sensors and
        return them in an array.

        The read values are normalized to the range 0 - 1024.
        """
        value = [0]*self.num_sensors

        value[0] = int(self.adc1.read_u16()*1024/0x10000)

        value[1] = int(self.adc.read_u16(0)*1024/0x10000)
        value[2] = int(self.adc.read_u16(1)*1024/0x10000)
        value[3] = int(self.adc.read_u16(2)*1024/0x10000)

        value[4] = int(self.adc5.read_u16()*1024/0x10000)

        return value

    def reset_calibration(self):
        self.calibrated_min = [1023] * self.num_sensors
        self.calibrated_max = [0] * self.num_sensors

    def calibration_cycle(self):
        """Read all line sensor values once and adjust the calibration range
        for the individual sensor channels. Once sufficient cycles have been
        run, :py:meth:`tracking.LineSensor.read_calibrated` will return a
        normalized measurement based on the minima and maxima measurements.

        For the calibration it is recommended to run multiple calibration
        cycles while the robot is moved over the bright and dark undergrounds.
        """
        sensor_values = self.analog_read()
        for i in range(self.num_sensors):
            value = sensor_values[i]

            if value < 200:
                # ignore values below the threshold
                continue

            if value < self.calibrated_min[i]:
                self.calibrated_min[i] = value
            if value > self.calibrated_max[i]:
                self.calibrated_max[i] = value

    def read_calibrated(self):
        """Return values calibrated to a value between 0 and 1000, where
        0 corresponds to the minimum value calculated by
        :py:meth:`tracking.LineSensor.calibration_cycle()`
        and 1000 corresponding to the maximum value."""
        sensor_values = self.analog_read()

        def scale_and_clamp(value, bottom, top):
            if value < 200:
                return -1
            else:
                total_range = top - bottom
                scaled = (value - bottom) * 1000.0 / total_range

                scaled = max(0, scaled)
                scaled = min(1000, scaled)

                return int(scaled)

        return list(map(scale_and_clamp,
                        sensor_values,
                        self.calibrated_min,
                        self.calibrated_max))

    def read_line(self, white_line=False):
        """
        Operates the same as read calibrated, but also returns an
        estimated position of the robot with respect to a line. The
        estimate is made using a weighted average of the sensor indices
        multiplied by 1000, so that a return value of 0 indicates that
        the line is directly below sensor 0, a return value of 1000
        indicates that the line is directly below sensor 1, 2000
        indicates that it's below sensor 2000, etc.  Intermediate
        values indicate that the line is between two sensors.  The
        formula is:

        .. math::
            \\frac{0 \\cdot value0 + 1000 \\cdot value1 + 2000 \\cdot
                value2 + \\dotso}
            {value0  +  value1  +  value2 + \\dotso}

        By default, this function assumes a dark line (high values)
        surrounded by white (low values).  If your line is light on
        black, set the optional second argument white_line to true.  In
        this case, each sensor value will be replaced by (1000-value)
        before the averaging.
        """
        sensor_values = self.read_calibrated()
        if not white_line:
            sensor_values = list(map(lambda x: 1000-x, sensor_values))

        avg = 0
        on_line = False
        for index, value in enumerate(sensor_values):
            # does at least one sensor still detect a line?
            # The value can be bigger than 1000 if the sensor
            # didn't detect any black/white at all and returned -1
            if value > 500 and value <= 1000:
                on_line = True

            # sum up the weighted measurement values
            avg += value * (index * 1000)

        if not on_line:
            # If we are no longer on the line, check the last
            # position value we calculated. If that value was
            # smaller that middle position, just return a 0 for left
            if (self.last_value < (self.num_sensors - 1)*1000/2):
                self.last_value = 0
            # otherwise return the maximum possible value for right
            else:
                self.last_value = (self.num_sensors - 1)*1000
        else:
            self.last_value = avg / sum(sensor_values)

        return int(self.last_value), sensor_values


def calib(line_sensor):
    """Run multiple calibration cycles on the given
    :py:class:`tracking.LineSensor` instance. The cycles are run with a 500ms
    pause between them. They are run in an infinite loop and need to be
    stopped with Ctrl-C."""
    while True:
        line_sensor.calibration_cycle()
        print(f"{line_sensor.calibrated_min} {line_sensor.calibrated_max}")
        time.sleep(0.5)
