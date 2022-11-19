"""
This code is ported from https://github.com/raspberrypi/pico-examples/blob/master/pio/ir_nec/nec_receive_library/nec_receive.pio

Decode IR frames in NEC format and push 32-bit words to the input FIFO.

The input pin should be connected to an IR detector with an 'active low' output.

This program expects there to be 10 state machine clock ticks per 'normal' 562.5us burst period
in order to permit timely detection of start of a burst. The initailisation function below sets
the correct divisor to achive this relative to the system clock.

Within the 'NEC' protocol frames consists of 32 bits sent least-siginificant bit first; so the
Input Shift Register should be configured to shift right and autopush after 32 bits, as in the
initialisation function below.

IR codes can be extracted from the sm RX fifo. Values might look like this: 0xa15eff00

The first byte 0xa1 is the inverse of the following code 0x5e and 0xff, the inverse of 0x00 is
a form of control code. The second byte, here 0x5e, represents the received key code.
"""
from machine import Pin
import rp2


BURST_LOOP_COUNTER = 30
BIT_SAMPLE_DELAY = 15


class IRreceiver:
    @rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT, autopush=True, push_thresh=32)
    def ir_receive(BURST_LOOP_COUNTER=BURST_LOOP_COUNTER, BIT_SAMPLE_DELAY=BIT_SAMPLE_DELAY):
        wrap_target()

        label("next_burst")
        set(x, BURST_LOOP_COUNTER)
        wait(0, pin, 0)                     #  wait for the next burst to start
        
        label("burst_loop")
        jmp(pin, "data_bit")                #  the burst ended before the counter expired
        jmp(x_dec, "burst_loop")            #  wait for the burst to end
        
                                            #  the counter expired - this is a sync burst
        mov(isr, null)                      #  reset the Input Shift Register
        wait(1, pin, 0)                     #  wait for the sync burst to finish
        jmp("next_burst")                   #  wait for the first data bit
        
        label("data_bit")
        nop() [ BIT_SAMPLE_DELAY - 1 ]      #  wait for 1.5 burst periods before sampling the bit value
        in_(pins, 1)                        #  if the next burst has started then detect a '0' (short gap)
                                            #  otherwise detect a '1' (long gap)
                                            #  after 32 bits the ISR will autop    

        wrap()

    def __init__(self):
        ir = Pin(5, Pin.IN)

        self.sm = rp2.StateMachine(0, IRreceiver.ir_receive, freq=int(10.0 / 562.5e-6), in_base=ir, jmp_pin=ir)
        self.sm.active(1)

    def key_available(self):
        return self.sm.rx_fifo() > 0

    def get_key(self):
        data = self.sm.get()
        return (data & 0x00ff0000) >> 16
