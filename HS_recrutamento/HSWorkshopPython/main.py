from random import randint
import numpy as np
import pygame as pg
import math as m


class Slot:
    def __init__(self, credits_start):
        self.credits = credits_start
        prob_1 = np.ones(50)  # Define desired probabilities
        prob_2 = np.ones(40) * 2
        prob_3 = np.ones(30) * 3
        prob_4 = np.ones(20) * 4
        prob_5 = np.ones(10) * 5
        prob_6 = np.ones(5) * 6
        prob_7 = [7]
        self.prob = np.concatenate([prob_1, prob_2, prob_3, prob_4, prob_5, prob_6, prob_7])
        self.payout = [5, 10, 20, 70, 200, 1000, 100000]  # Get associated jackpot payout
        self.outcome = [0, 0, 0]
        self.bet = 0

    def roll(self, bet=''):
        if not pygame:
            print('----------------------------------------------------------')
            print(f'Current credits: {self.credits}')  # Get user bet value
            self.bet = int(input('Credits to bet: '))
            while self.bet > self.credits:
                print('Insufficient funds. Please enter a lower bet')
                self.bet = int(input('Credits to bet: '))
            self.credits -= self.bet  # Deduct bet from credit total
            self.outcome = [int(self.prob[randint(0, 155)]),
                            int(self.prob[randint(0, 155)]),
                            int(self.prob[randint(0, 155)])]  # Pick 3 random numbers from the prob list
            print(f'{self.outcome[0]} {self.outcome[1]} {self.outcome[2]}')
            self.check_win()
        else:
            if int(bet) > self.credits:
                bet = 'Insufficient credits'
                return bet
            elif int(bet) <= 0:
                bet = 'Invalid bet'
                return bet
            else:
                print(f'bet = {int(bet)}')
                self.bet = int(bet)
                self.credits -= self.bet
                print(self.credits)
                self.outcome = [int(self.prob[randint(0, 155)]), int(self.prob[randint(0, 155)]),
                                int(self.prob[randint(0, 155)])]
                print(self.outcome)
                return ''

    def check_win(self):
        if self.outcome[0] == self.outcome[1] and self.outcome[0] == self.outcome[2]:  # If outcomes are equal = jackpot
            win = self.payout[self.outcome[0] - 1] * self.bet
            self.credits += win  # Add payout * bet to current credits
            print(f'You won {win} credits')
            return True
        else:
            print(f'No prize')
            return False

    def over(self):
        return self.credits == 0


pygame = True  # pygame = False will run program using only the terminal, True will open a pygame window
if pygame:
    pg.init()  # Initialize pygame and set screen parameters
    screen = pg.display.set_mode([800, 600])
    screen.fill((0, 0, 0))

    pg.mixer.init()  # Get sound effects
    slot_sound = pg.mixer.Sound('slot_machine.wav')
    jackpot_sound = pg.mixer.Sound('jackpot.wav')
    slot_sound.set_volume(0.3)  # Lower sound effect volume
    jackpot_sound.set_volume(0.3)

    base_font = pg.font.Font(None, 32)
    user_text = ''
    input_rect = pg.Rect(180, 500, 220, 32)
    credit_rect = pg.Rect(220, 50, 140, 32)
    color_active = pg.Color('lightskyblue3')
    color_passive = pg.Color('chartreuse4')
    color = color_passive
    active = False

    slot_pull = False
    play = False
    colors = [(255, 10, 10), (240, 130, 0), (255, 255, 20), (0, 153, 0), (0, 102, 204), (0, 0, 240), (102, 0, 204)]
    rand_color = [[(), (), ()], [(), (), ()], [(), (), ()]]

    sound_timer = [False, 490, 490]
    run = True
    quit_game = False
    begin = True
    slot1 = Slot(100)
    i = 100
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        if not begin:
            pg.draw.rect(screen, (100, 100, 200), [100, 150, 100, 300])
            pg.draw.rect(screen, (100, 100, 200), [100 + 140, 150, 100, 300])
            pg.draw.rect(screen, (100, 100, 200), [100 + 280, 150, 100, 300])
            if sound_timer[0] and sound_timer[1] > 0:
                k_1 = m.ceil((-100 - i) / 450)
                k_2 = m.ceil((-250 - i) / 450)
                k_3 = m.ceil((-400 - i) / 450)
                if i == 100:
                    k_1_old, k_2_old, k_3_old = k_1, k_2, k_3
                    for i in range(3):
                        for j in range(3):
                            rand_color[i][j] = colors[randint(0, 6)]
                else:
                    if k_1 != k_1_old:
                        rand_color[0][0] = colors[randint(0, 6)]
                        rand_color[1][0] = colors[randint(0, 6)]
                        rand_color[2][0] = colors[randint(0, 6)]
                        k_1_old = k_1
                    if k_2 != k_2_old:
                        rand_color[0][1] = colors[randint(0, 6)]
                        rand_color[1][1] = colors[randint(0, 6)]
                        rand_color[2][1] = colors[randint(0, 6)]
                        k_2_old = k_2
                    if k_3 != k_3_old:
                        rand_color[0][2] = colors[randint(0, 6)]
                        rand_color[1][2] = colors[randint(0, 6)]
                        rand_color[2][2] = colors[randint(0, 6)]
                        k_3_old = k_3
                pg.draw.rect(screen, rand_color[0][0], (120, 150 + i + 450 * k_1, 60, 100))
                pg.draw.rect(screen, rand_color[0][1], (120, 300 + i + 450 * k_2, 60, 100))

                pg.draw.rect(screen, rand_color[1][0], (260, 150 + i + 450 * k_1, 60, 100))
                pg.draw.rect(screen, rand_color[1][1], (260, 300 + i + 450 * k_2, 60, 100))

                pg.draw.rect(screen, rand_color[2][0], (400, 150 + i + 450 * k_1, 60, 100))
                pg.draw.rect(screen, rand_color[2][1], (400, 300 + i + 450 * k_2, 60, 100))

                if k_3 < 5:
                    pg.draw.rect(screen, rand_color[0][2], (120, 450 + i + 450 * k_3, 60, 100))
                    pg.draw.rect(screen, rand_color[1][2], (260, 450 + i + 450 * k_3, 60, 100))
                    pg.draw.rect(screen, rand_color[2][2], (400, 450 + i + 450 * k_3, 60, 100))
                else:
                    pg.draw.rect(screen, colors[slot1.outcome[0] - 1], (120, 450 + i + 450 * k_3, 60, 100))
                    pg.draw.rect(screen, colors[slot1.outcome[1] - 1], (260, 450 + i + 450 * k_3, 60, 100))
                    pg.draw.rect(screen, colors[slot1.outcome[2] - 1], (400, 450 + i + 450 * k_3, 60, 100))

                sound_timer[1] -= 1
                sound_timer[2] -= 1
                i -= 5
            elif sound_timer[0] and sound_timer[1] == 0:
                pg.draw.rect(screen, colors[slot1.outcome[0] - 1], (120, 250, 60, 100))
                pg.draw.rect(screen, colors[slot1.outcome[1] - 1], (260, 250, 60, 100))
                pg.draw.rect(screen, colors[slot1.outcome[2] - 1], (400, 250, 60, 100))
                if sound_timer[2] == 0:
                    if slot1.check_win():
                        jackpot_sound.play()
                    sound_timer[2] = 490
            pg.draw.rect(screen, (0, 0, 0), [100, 0, 100, 150])
            pg.draw.rect(screen, (0, 0, 0), [100, 450, 100, 600])
            pg.draw.rect(screen, (0, 0, 0), [260, 0, 100, 150])
            pg.draw.rect(screen, (0, 0, 0), [260, 450, 100, 600])
            pg.draw.rect(screen, (0, 0, 0), [400, 0, 100, 150])
            pg.draw.rect(screen, (0, 0, 0), [400, 450, 100, 600])
            pg.draw.polygon(screen, (0, 0, 0), [(640, 50), (640, 550), (740, 550), (740, 50)])
            pg.draw.polygon(screen, (50, 50, 50), [(680, 100), (700, 100), (700, 500), (680, 500)])

            if pg.mouse.get_pressed()[0]:
                position = pg.mouse.get_pos()
                if input_rect.collidepoint(position):
                    active = True
                    if user_text == 'Insufficient credits' or user_text == 'Invalid bet':
                        user_text = ''
                else:
                    active = False

                d_roll = m.sqrt((position[0] - 690)**2 + (position[1] - 100)**2)
                if d_roll < 50:
                    slot_pull = True
                    play = True
                if slot_pull:
                    pg.draw.circle(screen, (255, 0, 0), (690, position[1]), 50) if 100 < position[1] < 500 else 0
                    if slot1.credits == 0:
                        quit_game = True
                else:
                    pg.draw.circle(screen, (255, 0, 0), (690, 100), 50)

                d_quit = m.sqrt((position[0] - 100)**2 + (position[1] - 520)**2)
                if d_quit < 30:
                    quit_game = True
            else:
                pg.draw.circle(screen, (255, 0, 0), (690, 100), 50)
                slot_pull = False
                if play and (not sound_timer[0] or sound_timer[1] == 0):
                    if user_text != '' and user_text != 'Insufficient credits':
                        user_text = slot1.roll(bet=user_text)
                        if user_text == '':
                            slot_sound.play()
                            sound_timer = [True, 490, 490]
                            i = 100
                        play = False
                else:
                    play = False

            pg.draw.rect(screen, (100, 150, 120), credit_rect)
            cred_text_surf = base_font.render(str(slot1.credits).encode("utf-8").decode("utf-8"), True, (255, 255, 255))
            screen.blit(cred_text_surf, (credit_rect.x + 5, credit_rect.y + 5))

            color = color_active if active else color_passive
            pg.draw.rect(screen, color, input_rect)
            text_surf = base_font.render(user_text, True, (255, 255, 255))
            screen.blit(text_surf, (input_rect.x + 5, input_rect.y + 5))
            input_rect.w = max(220, text_surf.get_width() + 10)

            cred_ind_rect = [pg.Rect(205, 18, 150, 32), pg.Rect(200, 50, 20, 32), pg.Rect(360, 50, 20, 32)]
            pg.draw.rect(screen, (0, 0, 0), cred_ind_rect[0])
            pg.draw.rect(screen, (0, 0, 0), cred_ind_rect[1])
            pg.draw.rect(screen, (0, 0, 0), cred_ind_rect[2])
            cred_ind_text = [base_font.render('Current Credits', True, (255, 255, 255)),
                             base_font.render('$', True, (255, 255, 255))]

            screen.blit(cred_ind_text[0], (cred_ind_rect[0].x + 5, cred_ind_rect[0].y + 5))
            screen.blit(cred_ind_text[1], (cred_ind_rect[1].x + 5, cred_ind_rect[1].y + 5))
            screen.blit(cred_ind_text[1], (cred_ind_rect[2].x + 5, cred_ind_rect[2].y + 5))

            bet_ind_rect = pg.Rect(265, 532, 50, 32)
            pg.draw.rect(screen, (0, 0, 0), bet_ind_rect)
            bet_ind_text = base_font.render('Bet', True, (255, 255, 255))
            screen.blit(bet_ind_text, (bet_ind_rect.x + 5, bet_ind_rect.y + 5))

            pg.draw.circle(screen, (200, 100, 200), (100, 520), 30)
            quit_text_surf = base_font.render('Quit', True, (255, 255, 255))
            quit_text_rect = pg.Rect(70, 550, 60, 32)
            screen.blit(quit_text_surf, (quit_text_rect.x + 5, quit_text_rect.y + 5))

            if quit_game:
                end_credits_text_surf1 = base_font.render('Final score: ', True, (0, 200, 120))
                end_credits_text_surf2 = base_font.render(str(slot1.credits).encode("utf-8").decode("utf-8"),
                                                          True, (0, 200, 120))
                end_credits_rect1 = pg.Rect(450, 500, 140, 32)
                end_credits_rect2 = pg.Rect(590, 500, 140, 32)
                screen.blit(end_credits_text_surf1, (end_credits_rect1.x + 5, end_credits_rect1.y + 5))
                screen.blit(end_credits_text_surf2, (end_credits_rect2.x + 5, end_credits_rect2.y + 5))
                run = False
                pg.display.flip()
                pg.time.delay(1000)
        else:
            starting_credits_rect = pg.Rect(330, 284, 140, 32)
            if pg.mouse.get_pressed()[0]:
                position = pg.mouse.get_pos()
                if starting_credits_rect.collidepoint(position):
                    active = True
                else:
                    active = False

                d_start = m.sqrt((position[0] - 400)**2 + (position[1] - 400)**2)
                if d_start < 30:
                    slot1.credits = int(user_text)
                    user_text = ''
                    begin = False

            color = color_active if active else color_passive
            pg.draw.rect(screen, color, starting_credits_rect)
            text_surf = base_font.render(user_text, True, (255, 255, 255))
            screen.blit(text_surf, (starting_credits_rect.x + 5, starting_credits_rect.y + 5))
            starting_credits_rect.w = max(140, text_surf.get_width() + 10)

            begin_text_surf = base_font.render('Enter starting credits', True, (255, 255, 255))
            begin_text_rect = pg.Rect(280, 252, 140, 32)
            screen.blit(begin_text_surf, (begin_text_rect.x + 5, begin_text_rect.y + 5))

            pg.draw.circle(screen, (200, 0, 0), (400, 400), 30)
            start_text_surf = base_font.render('Start', True, (255, 255, 255))
            start_text_rect = pg.Rect(369, 384, 60, 32)
            screen.blit(start_text_surf, (start_text_rect.x + 5, start_text_rect.y + 5))

            if not begin:
                screen.fill((0, 0, 0))

        pg.time.delay(10)
        pg.display.flip()
    pg.quit()
else:
    cred_start = int(input('How many starting credits? '))
    slot1 = Slot(cred_start)
    while not slot1.over():
        slot1.roll()
        slot1.check_win()
        if slot1.credits == 0:
            print('Insufficient credits to play. Game Over')
            break
        cont = input('Do you wish to proceed (y, n)?')
        if cont.lower() == 'n':
            break

    print(f'\nFinal balance: {slot1.credits} credits!') if slot1.credits != 0 else 0
