from machine import Pin,PWM
from time import sleep_ms
from LCDmodule import LCD_1inch14, BL


class rocket_class():
    def __init__(self):
        self.x = 90
        self.width = 40
        self.score = 0

    def spawn(self):
        LCD.fill_rect(self.x, 120, self.width, 8, LCD.white)


class ball_class():
    def __init__(self):
        self.x = 120
        self.y = 20
        self.directionV = 1
        self.directionH = -1

    def spawn(self):
        LCD.ellipse(self.x, self.y, 4, 4, LCD.blue, True)

    def bounce(self):
        if (rocket_instance.x - 3) < self.x < (rocket_instance.x + rocket_instance.width + 3):
            self.directionV = -1
            rocket_instance.score += 1


def counter():
    if rocket_instance.score >= 100:
        LCD.hline(160, 0, 80, LCD.red)
        LCD.hline(160, 15, 80, LCD.red)
        LCD.vline(160, 0, 15, LCD.red)
        LCD.vline(239, 0, 15, LCD.red)
        LCD.text(f"Score:{rocket_instance.score}", 165, 5, LCD.green)

    elif rocket_instance.score >= 10:
        LCD.hline(170, 0, 80, LCD.red)
        LCD.hline(170, 15, 80, LCD.red)
        LCD.vline(170, 0, 15, LCD.red)
        LCD.vline(239, 0, 15, LCD.red)
        LCD.text(f"Score:{rocket_instance.score}", 175, 5, LCD.green)

    else:
        LCD.hline(180, 0, 80, LCD.red)
        LCD.hline(180, 15, 80, LCD.red)
        LCD.vline(180, 0, 15, LCD.red)
        LCD.vline(239, 0, 15, LCD.red)
        LCD.text(f"Score:{rocket_instance.score}", 183, 5, LCD.green)


if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768) # max 65535
    # 32768
    LCD = LCD_1inch14()
    rocket_instance = rocket_class()
    ball_instance = ball_class()
    # color BRG
    LCD.fill(LCD.black)

    move_left = Pin(16, Pin.IN, Pin.PULL_UP)
    move_right = Pin(20, Pin.IN, Pin.PULL_UP)

    while True:
        LCD.fill(LCD.black)

        rocket_instance.spawn()
        ball_instance.spawn()
        ball_instance.x += 1*ball_instance.directionH # movement left-right
        if move_left.value() == 0 and rocket_instance.x > 0:
            rocket_instance.x -= 5

        if move_right.value() == 0 and rocket_instance.x < 240-rocket_instance.width:
            rocket_instance.x += 5

        ball_instance.x += ball_instance.directionH*2

        if ball_instance.y <= 128:
            ball_instance.y += ball_instance.directionV*3

        else:
            ball_instance.y = 15
            ball_instance.x = 120

        if ball_instance.x < 0 or ball_instance.x > 240:
            ball_instance.directionH *= -1

        if ball_instance.y <= 0:
            ball_instance.directionV *= -1

        if ball_instance.y >= 112:
            ball_instance.bounce()

        counter()

        sleep_ms(1)
        LCD.show()
