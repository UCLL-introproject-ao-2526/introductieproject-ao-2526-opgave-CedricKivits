import copy
import random
import pygame

pygame.init()

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Fantasy Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
status_font = pygame.font.Font('freesansbold.ttf', 22)
active = False
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'ENEMY WINS :(', 'TIE GAME...']

player_hp = 100

# [dn] als je het op deze manier schrijft, ga je altijd moet onthouwen dat '1' 'Orc' is
# ORC_INDEX = 1 is een stuk duidelijker waar je het gebruik, en maakt je leven ook makkelijker ;)
GOBLIN_INDEX = 0
ORC_INDEX = 1
DRAGON_INDEX = 2

enemies = ['Goblin', 'Orc', 'Dragon']
enemy_health = [100, 120, 150]

# [dn] number in het engels wordt eerder gezien als 'aantal'. Gebruik beter 'index', dat is een plaats in een verzameling (kort door de bocht)
enemy_index = GOBLIN_INDEX
enemy_name = enemies[enemy_index]
enemy_hp = enemy_health[enemy_index]

# [dn] hiervoor gebruikte je een array, en nu plots niet? 1 van de 2 is beter, maar het belangrijkste is consistentie (want het is voorspelbaar)
enemy_defeated = [False, False, False]

kingdom_saved = False


def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck) - 1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
    return current_hand, current_deck


def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))


def draw_health():
    screen.blit(smaller_font.render(f'{enemy_name} HP: {enemy_hp}', True, 'green'), (20, 110))
    screen.blit(smaller_font.render(f'Hero HP: {player_hp}', True, 'red'), (20, 410))


def draw_enemy_status():
    # [dn] kan korter met een loop, als je je arrays gebruikt
    for i in range(len(enemies)):
        if enemy_defeated[i]:
            enemy_text = f'{enemies[i]}: DEFEATED'
        else:
            enemy_text = f'{enemies[i]}: UNDEFEATED'

        screen.blit(status_font.render(enemy_text, True, 'white'), (20, 810 + (30 * i)))


def draw_cards(player, dealer, reveal):
    card_spacing = 70

    for i in range(len(player)):
        # [dn] je hergebruikt hier een paar variabele heel vaak. Specifiek 70. Dat is geen willekeurig getal
        # Steek het in een variabele, dan heb je een naam met een betekenis, en als je ooit een andere 
        # waarde nodig hebt moet je het maar aanpassen op 1 plek. 
        pygame.draw.rect(screen, 'white', [card_spacing + (card_spacing * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + card_spacing * i, 465 + 5 * i))
        screen.blit(font.render(player[i], True, 'black'), (75 + card_spacing * i, 635 + 5 * i))
        pygame.draw.rect(screen, 'gold', [card_spacing + (card_spacing * i), 460 + (5 * i), 120, 220], 5, 5)

    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [card_spacing + (card_spacing * i), 160 + (5 * i), 120, 220], 0, 5)

        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + card_spacing * i, 165 + 5 * i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + card_spacing * i, 335 + 5 * i))

        else:
            screen.blit(font.render('???', True, 'black'), (75 + card_spacing * i, 165 + 5 * i))
            screen.blit(font.render('???', True, 'black'), (75 + card_spacing * i, 335 + 5 * i))

        pygame.draw.rect(screen, 'green', [card_spacing + (card_spacing * i), 160 + (5 * i), 120, 220], 5, 5)


def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')

    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])

        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10

        elif hand[i] == 'A':
            hand_score += 11

    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10

    return hand_score


def draw_game(act, record, result):
    button_list = []

    if not act:
        screen.blit(font.render('FANTASY BLACKJACK', True, 'gold'), (60, 180))
        screen.blit(smaller_font.render('Defeat all enemies!', True, 'white'), (125, 250))

        deal = pygame.draw.rect(screen, 'white', [150, 350, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'gold', [150, 350, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 380))
        button_list.append(deal)

    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'gold', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'gold', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)

        draw_enemy_status()

    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))

        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'gold', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)

    if kingdom_saved:
        screen.blit(font.render('KINGDOM SAVED!', True, 'gold'), (100, 330))

    elif player_hp <= 0:
        screen.blit(font.render('HERO DEFEATED!', True, 'red'), (90, 330))

    return button_list


def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    global player_hp
    global enemy_hp
    global enemy_index
    global enemy_name
    global kingdom_saved

    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        # [dn] je whitespace (lege regels) maken het hier minder leesbaar, niet meer.
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4

        if add:

            if result == 1 or result == 3:
                totals[1] += 1
                player_hp -= 20

            elif result == 2:
                totals[0] += 1
                enemy_hp -= play_score

            else:
                totals[2] += 1

            add = False

            if enemy_hp <= 0 and enemy_index == GOBLIN_INDEX:
                enemy_defeated[GOBLIN_INDEX] = True
                enemy_index = ORC_INDEX
                enemy_name = enemies[enemy_index]
                enemy_hp = enemy_health[enemy_index]

                player_hp = 100

            elif enemy_hp <= 0 and enemy_index == ORC_INDEX:
                enemy_defeated[ORC_INDEX] = True
                enemy_index = DRAGON_INDEX
                enemy_name = enemies[enemy_index]
                enemy_hp = enemy_health[enemy_index]

                player_hp = 100

            elif enemy_hp <= 0 and enemy_index == DRAGON_INDEX:
                enemy_defeated[DRAGON_INDEX] = True
                kingdom_saved = True

    return result, totals, add


run = True

while run:
    timer.tick(fps)
    screen.fill('black')

    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)

        initial_deal = False

    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        draw_health()

        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)

            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)

        draw_scores(player_score, dealer_score)

    buttons = draw_game(active, records, outcome)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:

            if not active:

                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True

            else:

                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active and not kingdom_saved:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)

                elif buttons[1].collidepoint(event.pos) and not reveal_dealer and not kingdom_saved:
                    reveal_dealer = True
                    hand_active = False

                elif len(buttons) == 3:

                    if buttons[2].collidepoint(event.pos):

                        if player_hp <= 0 or kingdom_saved:
                            player_hp = 100

                            enemy_index = GOBLIN_INDEX
                            enemy_name = enemies[enemy_index]
                            enemy_hp = enemy_health[enemy_index]

                            enemy_defeated = [False, False, False]

                            kingdom_saved = False
                            records = [0, 0, 0]

                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(
        hand_active,
        dealer_score,
        player_score,
        outcome,
        records,
        add_score
    )

    pygame.display.flip()

pygame.quit()