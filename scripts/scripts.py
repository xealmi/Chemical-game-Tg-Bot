from random import randint, choices

def case_roll(case):
    val = randint(0,1000)
    if case == 'common_case':
        if 0<=val<950:
            return randint(200, 1500)
        elif 950<=val<=1000:
            return 'epic_case'
    elif case == 'epic_case':
        if 0<=val<950:
            return randint(200, 2000)
        elif 950<=val<985:
            return 'legendary_case'
        else:
            return 'add_is'
    elif case == 'legendary_case':
        items = []
    elif case == 'mythical_case':
        items = []