import chess


def position_from_string(position_string):
    pass


all_list = []


with open('properties.py', 'r') as props:
    for line in props:
        if line[0:3] == 'def' and line[4] != '_':
            function_name = ''
            for char in line[4:]:
                if char != '(':
                    function_name += char
                else:
                    break
            all_list.append(function_name)

print(all_list)
