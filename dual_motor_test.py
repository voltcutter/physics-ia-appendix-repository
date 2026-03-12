import time
from dual_motor_control import DualMotorController

DMC = DualMotorController()
DMC.start()

DMC.motor1.setSpeed(-10)
DMC.motor2.setSpeed(-10)
time.sleep(1)
# DMC.motor1.setSpeed(-2)
# DMC.motor2.setSpeed(-2)
# time.sleep(1)
# DMC.motor1.setSpeed(-3)
# DMC.motor2.setSpeed(-3)
# time.sleep(1)
# DMC.motor1.setSpeed(-2)
# DMC.motor2.setSpeed(-2)
# time.sleep(1)
# DMC.motor1.setSpeed(-1)
# DMC.motor2.setSpeed(-1)
# time.sleep(1)
DMC.stop()