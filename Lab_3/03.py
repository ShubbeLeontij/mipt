import turtle as t

input_filename = 'input.txt'
font_filename = 'font.txt'

if __name__ == '__main__':
    with open(font_filename, 'r') as f_f:
        paint_dict = {}
        for line in f_f.readlines():
            line = line.rstrip()
            local_list = list(line[line.find('[') + 1: line.rfind(']')].split('; '))
            answer_list = []
            for i in local_list:
                if i[0] == "'":
                    answer_list.append(i[1:-1])
                else:
                    a = int(i[1: i.find(', ')])
                    b = float(i[i.find(', ') + 1: -1])
                    answer_list.append((a, b))
            paint_dict[line[:line.find(' ')]] = answer_list

    with open(input_filename, 'r') as i_f:
        input_str = i_f.readline()
    move_list = []
    for num in input_str.rstrip():
        move_list += paint_dict[num]

    t.shape('turtle')
    t.penup()
    t.backward(500)

    for element in move_list:
        if element == 'penup':
            t.penup()
        elif element == 'pendown':
            t.pendown()
        else:
            alpha, length = element
            t.left(alpha)
            t.forward(length)
