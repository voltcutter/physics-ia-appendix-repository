import time
import math
from dual_motor_control import DualMotorController

import pygame
import RPi.GPIO as GPIO
# from gpiozero import Servo

# servo = Servo(17, min_pulse_width=0.0005, max_pulse_width=0.0025)

DMC = DualMotorController()
DMC.start()

currentPosition = (0, 0)
targetPosition = (2, 2)
maxPosition = (8, 8)

radius = 0.5
circumference = 2 * math.pi * radius

windowSize = (400, 400)
screen = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()

averagedVelocity = (0, 0)
averageRange = 6 # frames

def calculate_time(distance, revsPerSecond):
    theta = (distance * math.pi * 2) / (math.pi * 0.1 * 17)
    return theta / revsPerSecond

def multiply_by_constant(vec, const):
    return (vec[0] * const, vec[1] * const)

def add(vec1, vec2):
    return(vec1[0] + vec2[0], vec1[1] + vec2[1])

def sub(vec1, vec2):
    return(vec1[0] - vec2[0], vec1[1] - vec2[1])

def normalise(vec):
    magnitude = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])
    return multiply_by_constant(vec, 1/magnitude)

def magnitude(vec):
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])

# motor1: y
# motor2: -x

toggleTime = 60
penDown = True

while True:
    # if (toggleTime <= 0):
    #     toggleTime = 60
    #     penDown = not penDown
    #     if (penDown):
    #         servo.min()
    #     else:
    #         servo.mid()

    deltaTime = 1 / 60

    mousePos = (0, 0)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mousePos = event.pos
            targetPosition = multiply_by_constant(mousePos, 4 / windowSize[0])
            print(targetPosition)
            break
    
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 255, 255), mousePos, 10)
    pygame.display.flip()

    velocity = multiply_by_constant(normalise(sub(targetPosition, currentPosition)), 5)
    averagedVelocity = multiply_by_constant(add(multiply_by_constant(averagedVelocity, averageRange - 1), velocity), 1 / averageRange)
    if magnitude(averagedVelocity) < 0.1:
        averagedVelocity = (0, 0)
    DMC.motor2.setSpeed(-averagedVelocity[0])
    DMC.motor1.setSpeed(averagedVelocity[1])

    currentPosition = add(currentPosition, multiply_by_constant(averagedVelocity, deltaTime))

    clock.tick(60)
    toggleTime -= 1