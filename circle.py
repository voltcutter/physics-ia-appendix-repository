import time
import math
from dual_motor_control import DualMotorController

DMC = DualMotorController()
DMC.start()

gearCircumference = 17 * 1 * math.pi # teeth * module (mm) * pi
circleRadius = 2
circumference = 2 * math.pi * circleRadius
revolutions = circumference / gearCircumference

t = 0
while t < 2:
    angularVelocityX = revolutions * 4 * math.pi * math.cos(math.pi * t)
    angularVelocityY = -revolutions * 4 * math.pi * math.sin(math.pi * t)

    DMC.motor2.setSpeed(-angularVelocityX)
    DMC.motor1.setSpeed(angularVelocityY)

    t += 1/60
    time.sleep(1 / 60)

DMC.stop()