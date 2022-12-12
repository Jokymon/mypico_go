PicoGo Hardware
===============

+-----------------------------+----------+-----+-----+----------+-----------------+
| function                    | pin name | pin | pin | pin name | function        |
+=============================+==========+=====+=====+==========+=================+
| Bluetooth RX                | GPIO0    | 1   | 40  | VBUS     |                 |
+-----------------------------+----------+-----+-----+----------+-----------------+
| Bluetooth TX                | GPIO1    | 2   | 39  | VSYS     |                 |
+-----------------------------+----------+-----+-----+----------+-----------------+
|                             | GND      | 3   | 38  | GND      |                 |
+-----------------------------+----------+-----+-----+----------+-----------------+
| IR obstacle right           | GPIO2    | 4   | 37  | 3V3_EN   |                 |
+-----------------------------+----------+-----+-----+----------+-----------------+
| IR obstacle left            | GPIO3    | 5   | 36  | 3V3(OUT) |                 |
+-----------------------------+----------+-----+-----+----------+-----------------+
| Buzzer                      | GPIO4    | 6   | 35  | ADC_VREF |                 |
+-----------------------------+----------+-----+-----+----------+-----------------+
| IR receiver                 | GPIO5    | 7   | 34  | ADC2     | Tracking sensor |
+-----------------------------+----------+-----+-----+----------+-----------------+
|                             | GND      | 8   | 33  | GND      |                 |
+-----------------------------+----------+-----+-----+----------+-----------------+
| I2C SDA                     | GPIO6    | 9   | 32  | ADC1     | Tracking sensor |
+-----------------------------+----------+-----+-----+----------+-----------------+
| I2C SCL                     | GPIO7    | 10  | 31  | ADC0     | Battery voltage |
+-----------------------------+----------+-----+-----+----------+-----------------+
| LCD SPI RX                  | GPIO8    | 11  | 30  | RUN      |                 |
+-----------------------------+----------+-----+-----+----------+-----------------+
| LCD SPI CS                  | GPIO9    | 12  | 29  | GPIO22   | Neopixel        |
+-----------------------------+----------+-----+-----+----------+-----------------+
|                             | GND      | 13  | 28  | GND      |                 |
+-----------------------------+----------+-----+-----+----------+-----------------+
| LCD SPI SCK                 | GPIO10   | 14  | 27  | GPIO21   | Motor PWM right |
+-----------------------------+----------+-----+-----+----------+-----------------+
| LCD SPI TX                  | GPIO11   | 15  | 26  | GPIO20   | Motor IN2 right |
+-----------------------------+----------+-----+-----+----------+-----------------+
| LCD Reset                   | GPIO12   | 16  | 25  | GPIO19   | Motor IN1 right |
+-----------------------------+----------+-----+-----+----------+-----------------+
| LCD Backlight               | GPIO13   | 17  | 24  | GPIO18   | Motor IN1 left  |
+-----------------------------+----------+-----+-----+----------+-----------------+
|                             | GND      | 18  | 23  | GND      |                 |
+-----------------------------+----------+-----+-----+----------+-----------------+
| Ultrasonic distance trigger | GPIO14   | 19  | 22  | GPIO17   | Motor IN2 left  |
+-----------------------------+----------+-----+-----+----------+-----------------+
| Ultrasonic distance echo    | GPIO15   | 20  | 21  | GPIO16   | Motor PWM left  |
+-----------------------------+----------+-----+-----+----------+-----------------+

Infrared receiver
-----------------

The PicoGo robot features an IR receiver for remote controlling your robot.

.. image:: images/ir_recv_schema.png
    :alt: IR receiver schema
    :width: 49%
.. image:: images/ir_recv_location.png
    :alt: IR receiver location on the robot
    :width: 49%

From the schema and the actual hardware it is unclear what kind of component it is.
Based on search results, it could however be something like an Everlight IRM-H6XXT
or an Everlight EAIRMIA1. The top shows an engraving showing "AX14".

Display
-------

The display has a resolution of 240 x 135 pixel. Every pixel is represented by a 16-bit 5-6-5 RGB value