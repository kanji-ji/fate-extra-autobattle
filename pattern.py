def stronger_than(x):
    if x == 'A':
        return 'G'
    if x == 'B':
        return 'A'
    if x == 'G':
        return 'B'
    if x == 'S':
        return 'G'


def which_is_strong(atk_type_a, atk_type_b):
    if atk_type_a == atk_type_b:
        return atk_type_a
    if stronger_than(atk_type_a) == atk_type_b:
        return atk_type_b
    if stronger_than(atk_type_b) == atk_type_a:
        return atk_type_a


def which_is_weak(atk_type_a, atk_type_b):
    if atk_type_a == atk_type_b:
        return atk_type_a
    if stronger_than(atk_type_a) == atk_type_b:
        return atk_type_a
    if stronger_than(atk_type_b) == atk_type_a:
        return atk_type_b


def calc_optim_type(atk_type_dict):
    zero_cnt = 0
    for value in atk_type_dict.values():
        if value == 0:
            zero_cnt += 1
    if zero_cnt == 3:
        return 'W'
    if zero_cnt == 2:
        for key, value in atk_type_dict.items():
            if value != 0:
                return stronger_than(key)
    if zero_cnt == 1:
        for key, value in atk_type_dict.items():
            if value == 0:
                if key == 'A':
                    return 'B'
                if key == 'B':
                    return 'G'
                if key == 'G':
                    return 'A'
    if zero_cnt == 0:
        max_value = 0
        equal_cnt = 0
        for key, value in atk_type_dict.items():
            if value > max_value:
                ans = key
                max_value = value
            elif value == max_value:
                equal_cnt += 1
                if equal_cnt == 2:
                    return '*'
                ans = which_is_weak(ans, key)
        return stronger_than(ans)
                

def todict(enemy_action):
    ret = {}
    if len(enemy_action) > 6:
        raise Exception('input string must be 6 or less')
    for i in range(len(enemy_action)):
        if enemy_action[i] != '*':
            ret[i] = enemy_action[i]
    return ret



def insert_star(string):
    stars = ''
    for i in range(len(string)):
        if string[i] == '\t':
            stars += '*'
        else:
            if stars != '':
                string = string[:i] + stars[:-1] + string[i:]
            stars = ''
    string = string.replace('\t', '')
    while len(string) < 6:
        string += '*'
    return string


def clean_string(string):
    string = string.strip()
    string = string.replace(',', '')
    string = string.replace('?','*')
    string = insert_star(string)
    return string


def calc_optim_action(enemy_action):
    with open('pattern.txt', 'r') as f:
        pattern_list = f.readlines()
    pattern_list = [clean_string(pattern) for pattern in pattern_list]
    pattern_dict = todict(enemy_action)
    for key, atk_type in pattern_dict.items():
        pattern_list = [pattern 
        for pattern in pattern_list 
        if pattern[key] == atk_type or pattern[key] == '*']
    
    pattern_list = [pattern.replace('S', 'A').replace('W','*').replace('E', 'A') for pattern in pattern_list]
    action = ''
    for i in range(6):
        abgs_dict = {'A':0, 'B':0, 'G':0}
        for pattern in pattern_list:
            if pattern[i] != '*':
                abgs_dict[pattern[i]] += 1
        optim_type = calc_optim_type(abgs_dict)
        action += optim_type
    return action


print(calc_optim_action('G**A'))
#2