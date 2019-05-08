# Servo Control
import time

import wiringpi
from find_ball import FindBall

x_min = 20
x_max = 30
x_goal = (x_min + x_max) / 2

kp = 1
ki = 0
kd = 0

error = 0
integral = 0
deriv = 0
time_last_loop = time.time()
last_error = 0

fb = FindBall(0)

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

while True:
    x_ball = fb.get_x_location()
    if x_ball is None:
        print('No ball in frame')
        continue
    time_this_loop = time.time()
    error = x_goal - x_ball
    integral += (time_this_loop - time_last_loop) * error
    deriv = error - last_error
    time_last_loop = time_this_loop
    print('err: {}'.format(error))
    print('integral: {}'.format(integral))
    print('deriv: {}'.format(deriv))
    print('x_ball: {}'.format(x_ball))
