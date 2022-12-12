from machine import Pin


class IRobstacle:
    def __init__(self):
        self.dsr = Pin(2, Pin.IN)
        self.dsl = Pin(3, Pin.IN)

    def obstacle_left(self):
        return self.dsl.value() == 0

    def obstacle_right(self):
        return self.dsr.value() == 0

    def obstacle_front(self):
        return self.dsl.value() == 0 and self.dsr.value() == 0