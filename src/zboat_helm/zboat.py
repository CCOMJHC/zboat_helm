#!/usr/bin/env python

import sys
import time
import serial

class ZBoat:
    #'/dev/tty.usbserial'
    #'\\.\COMxx'
    #'/dev/ttyUSB0'
    #38400
    def __init__(self, serial_port='/dev/ttyUSB0', baudrate=115200):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.port_open = False
        self.ser = None

    def open_port(self, timeout=10):
        try:
            self.ser = serial.Serial(self.serial_port, self.baudrate, timeout=timeout)
            if self.ser.isOpen():
                self.port_open = True
            return self.port_open
        except serial.SerialException:
            return False

    def close_port(self):
        # The port will also close when it is deconstructed
        self.ser.close()

    def set_autonomy_mode(self):
        print('Setting Autonomous Control Mode\n')
        self.ser.write('!SetAutonomousControl\r\n')

    def set_manual_mode(self):
        print('Setting Manual Control Mode\n')
        self.ser.write('!SetManualControl\r\n')

    def write_pwm_values(self, left_thrust, right_thrust, rudder):
        # Make sure they are inside the possible ranges
        clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
        left_thrust = clamp(left_thrust, 1.0, 2.0)
        right_thrust = clamp(right_thrust, 1.0, 2.0)
        rudder = clamp(rudder, 1.0, 2.0)

        print('Writing PWM values l_thrust={:.3f}, r_thrust={:.3f}, rudder={:.3f}'.format( \
            left_thrust, right_thrust, rudder))
        self.ser.write('!pwm, *, {:.3f}, {:.3f}, {:.3f}, *, *\r\n'.format( \
            right_thrust, left_thrust, rudder))

if __name__ == '__main__':
  if len(sys.argv) > 1:
    zb = ZBoat(sys.argv[1])
  else:
    zb = ZBoat()
  zb.open_port()
  zb.set_autonomy_mode()
  for i in range(5):
    zb.write_pwm_values(2.0, 2.0, 2.0)
    time.sleep(1)
  zb.write_pwm_values(1.5, 1.5, 1.5)
