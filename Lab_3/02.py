import turtle as t

a = 50
input_str = '141700'

paint_dict = {
    '0': [(0, a), 'pendown', (270, 2*a), (90, a), (90, 2*a), (90, a), 'penup', (180, a)],
    '1': [(0, a), (270, a), 'pendown', (135, a * 2**0.5), (225, 2*a), 'penup', (180, 2*a), (270, 0)],
    '2': [(0, a), 'pendown', (0, a), (270, a), (315, a * 2**0.5), (135, a), 'penup', (90, 2*a), (270, 0)],
    '3': [(0, a), 'pendown', (0, a), (225, a * 2**0.5), (135, a), (225, a * 2**0.5), 'penup', (135, a), (90, 2*a), (270, 0)],
    '4': [(0, a), 'pendown', (270, a), (90, a), (270, a), (180, 2*a), (270, 0), 'penup'],
    '5': [(0, a), 'pendown', (270, a), (90, a), (270, a), (270, a), 'penup', (270, 2*a), 'pendown', (270, a), 'penup'],
    '6': [(0, 2*a), 'pendown', (225, a * 2**0.5), (45, a), (90, a), (90, a), (90, a), 'penup', (225, a * 2**0.5), (315, 0)],
    '7': [(0, a), 'pendown', (0, a), (225, a * 2**0.5), (45, a), 'penup', (180, a), (315, a * 2**0.5), (315, 0)],
    '8': [(0, a), 'pendown', (0, a), (270, a), (270, a), (270, a), (180, 2*a), (90, a), (90, 2*a), 'penup', (270, 0)],
    '9': [(0, a), 'pendown', (0, a), (270, a), (270, a), (270, a), 'penup', (180, 2*a), 'pendown', (135, a * 2**0.5), 'penup', (45, a), (270, 0)]
    }

if __name__ == '__main__':
    move_list = []
    for num in input_str:
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
