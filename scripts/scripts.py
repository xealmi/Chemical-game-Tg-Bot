from random import randint, choices

def case_roll(case):
    val = randint(0,1000)
    
    
    if case == 'common_case':
        if 0<=val<950:
            return 
        elif 950<=val<=1000:
            return 'epic_case'
    
    
    elif case == 'epic_case':
        if 0<=val<950:
            return randint(1500, 4000)
        elif 950<=val<985:
            return 'legendary_case'
        else:
            return 'add_is'
    
    
    elif case == 'legendary_case':
        if 0<=val<850:
            return randint(15000, 23500)
        elif 850<=val<955:
            return 'mythical_case'
        elif 955<=val<985:
            return 'add_is'
        else:
            return 'add_el'
    
    
    elif case == 'mythical_case':
        if 0<=val<750:
            return randint(15000, 23500)
        elif 750<=val<875:
            return 'mythical_case'
        elif 875<=val<935:
            return 'add_is'
        elif 935<=val<980:
            return 'add_el'
        else:
            return 'prem3d'


def prem_chek(user_data):
    if isinstance(user_data['premium'], int):
        return [False]