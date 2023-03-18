from machine import Pin
import utime


class IRobstacle:
    """Obstacle detector using the IR sensors."""
    def __init__(self):
        self.dsr = Pin(2, Pin.IN)
        self.dsl = Pin(3, Pin.IN)

    def obstacle_left(self):
        """Returns true if an obstacle is detected at the front left of the
        robot using the IR sensors."""
        return self.dsl.value() == 0

    def obstacle_right(self):
        """Returns true if an obstacle is detected at the front right of the
        robot using the IR sensors."""
        return self.dsr.value() == 0

    def obstacle_front(self):
        """Returns true if an obstacle is detected right in front of the
        robot using the IR sensors."""
        return self.dsl.value() == 0 and self.dsr.value() == 0


class Ultrasonic:
    """Obstacle detection and distance measurements using the ultrasonic
    ranging sensor."""
    def __init__(self):
        self.echo = Pin(15, Pin.IN)
        self.trig = Pin(14, Pin.OUT)
        self.echo.value(0)
        self.trig.value(0)

    def distance_cm(self):
        """Measure the distance to the nearest obstacle right in front of
        robot. The individual measurements should be around 60ms appart from
        each other so as not to overlap the triggers.

        The measurement is returned in cm.
        """
        self.trig.value(1)
        utime.sleep_us(10)
        self.trig.value(0)

        while self.echo.value() == 0:
            pass

        t_start = utime.ticks_us()
        while self.echo.value() == 1:
            pass
        t_end = utime.ticks_us()

        distance = ((t_end - t_start)*0.034) / 2
        return distance
