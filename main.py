# Servo Control
import time

import wiringpi
from find_ball import FindBall
from csv_writer import CSVWriter

x_min = 14
x_max = 388
x_goal = (x_min + x_max) / 2

s_max = 114
s_min = 80
s_mid = 94

kp = .05
ki = 0.01
kd = 0.008

error = 0
integral = 0
deriv = 0
time_last_loop = time.time()
last_error = 0

fb = FindBall(0)
csvw = CSVWriter("data.csv")

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
    deriv = (error - last_error) / (time_this_loop - time_last_loop)
    print(time_this_loop - time_last_loop)
    time_last_loop = time_this_loop
    print('err: {}'.format(error))
    print('integral: {}'.format(integral))
    print('deriv: {}'.format(deriv))
    print('x_ball: {}'.format(x_ball))
    val = s_mid + kp*error + ki*integral + kd*deriv
    val = min(val, s_max)
    val = max(val, s_min)
    wiringpi.pwmWrite(18, int(val))
    csvw.write(error, integral, deriv, time_last_loop, val)
