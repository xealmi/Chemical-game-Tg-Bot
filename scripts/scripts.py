from random import randint, choices

def case_roll(case):
    val = randint(0,1000)
    
    
    if case == 'common_case':
        if 0<=val<950:
            return randint(400, 1400)
        else:
            return 'epic_case'
    
    
    elif case == 'epic_case':
        if 0<=val<950:
            return randint(3000, 6500)
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
            return randint(30000, 65500)
        elif 750<=val<875:
            return 'mythical_case'
        elif 875<=val<935:
            return 'add_is'
        elif 935<=val<980:
            return 'add_el'
        else:
            return 'prem3d'


def lab_price_calc(x):
    return round(
        500 +100*4.5**x
    )

def lab_income_calc(x):
    return 1+x/10



def ch_el_price_calc(x):
    return round(
        10*3.2**x
    )

def ch_el_income_calc(x):
    return round(
        (1-1.4**x)/(-0.4)
    )



def is_price_calc(x):
    return round(
        10*(1.63)**x
    )

def is_income_calc(x):
    return round(
        (1-1.05**x)/(-0.05)
    )

def income_calc(ch_el, iso, labs):
    return round(
        (is_income_calc(iso) + ch_el_income_calc(ch_el)) * lab_income_calc(labs)
    )

def case_price():
    return [1000,5000,20000,50000]