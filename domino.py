import random

# Empty list for set of domino
full_set_domino = []

# The function creates full set
def createSet():
    global full_set_domino

    for i in range(7):
        for j in range(i, 7):
            full_set_domino.append([i, j])

    return full_set_domino

createSet()

stock = []
computer_pieces = []
player_pieces = []
status = ''
domino_snake = []


# The function splites pieces between computer, player and stock
def splitDominos():
    global full_set_domino, stock, computer_pieces, player_pieces

    # Shuffle pieces
    random.shuffle(full_set_domino)

    stock = full_set_domino[:14]
    computer_pieces = full_set_domino[14:21]
    player_pieces = full_set_domino[21:]

    return stock, computer_pieces, player_pieces


# Function runs last two functions and find who have to
# make the first (gives a snake) and next move
def start_of_domino_game():
    global computer_pieces, player_pieces, domino_snake, status

    while len(domino_snake) == 0:
        # Creating full set and split between players and stock
        splitDominos()

        # Finding the double domino
        all_players_peaces = computer_pieces + player_pieces
        domino_snake = [el for el in all_players_peaces if el[0] == el[1]]

    # Finding max domino in list of double dominos
    else:
        domino_snake = [max(domino_snake)]

        # Determine who makes the next move
        if domino_snake[0] in computer_pieces:
            status = 'player'
            computer_pieces.remove(domino_snake[0])

        elif domino_snake[0] in player_pieces:
            status = 'computer'
            player_pieces.remove(domino_snake[0])


start_of_domino_game()

# Print game
def game():
    global domino_snake
    print('=' * 70)
    print(f'Stock size: {len(stock)}')
    print(f'Computer pieces: {len(computer_pieces)}')
    print()
    print()

    if len(domino_snake) <= 6:
        for i in domino_snake:
            print(i, end=" ")
    else:
        # If snake has more than 6 pieces print first and last three pieces
        i = 0
        while i < 3:
            print(domino_snake[i], end='')
            i += 1

        print('...', end='')

        i = -3
        while i < 0:
            print(domino_snake[i], end='')
            i += 1

    print()
    print()
    print('Your pieces:')
    for i, val in enumerate(player_pieces):
        print(f'{i + 1}: {val}')

game()

# Function for calculating the most successful AI move
def aiCalculateMove():
    count = computer_pieces + domino_snake

    # Open nested lists (peaces)
    count = [x for y in count for x in y]

    # Empty dictionary for counted numbers
    count_dict = {}

    # Сount the number of digits from 0 to 6
    for i in range(7):
        count_dict[i] = count.count(i)
    print(count_dict)

    # Create a dictionary where key is a piece
    # and value is a sum of number's quantity in this piece
    scores = {}
    for i, el in enumerate(computer_pieces):
        scores[str(el)] = count_dict[el[0]] + count_dict[el[1]]

    # Sort dict in descending order
    scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}
    scores = dict(reversed(list(scores.items())))

    return scores

# Function for computer's move
def aiMove():
    global stock, status, domino_snake
    move = input('>')

    possible_moves = []
    best_moves_order = aiCalculateMove()

    # Computer looking for possible moves
    for el in computer_pieces:
        if (el[1] == domino_snake[0][0] or el[0] == domino_snake[0][0]) or \
                (el[0] == domino_snake[-1][-1] or el[1] == domino_snake[-1][-1]):
            possible_moves.append(el)

    # If there are no possible moves computer takes the piece from stock
    if len(possible_moves) == 0:
        if len(stock):
            computer_pieces.append(stock.pop(0))
        else:
            print('Stock is empty')
    else:
        piece = []

        # Choose a move in the calculated order
        for key in best_moves_order:
            for el in possible_moves:
                if str(el) == key:
                    piece.append(el)

        if piece[0][1] == domino_snake[0][0]:
            domino_snake.insert(0, piece[0])

        elif piece[0][0] == domino_snake[0][0]:
            piece.reverse()
            domino_snake.insert(0, piece[0])

        elif piece[0][0] == domino_snake[-1][-1]:
            domino_snake.append(piece[0])

        elif piece[0][1] == domino_snake[-1][-1]:
            piece[0].reverse()
            domino_snake.append(piece[0])

        possible_moves.clear()
        computer_pieces.remove(piece[0])

    status = 'player'
    game()


# Function for player move
def playerMove(inp):
    global domino_snake, stock, status

    if inp < 0:
        piece = player_pieces.pop(abs(inp) - 1)

        if piece[1] == domino_snake[0][0]:
            domino_snake.insert(0, piece)

        elif piece[0] == domino_snake[0][0]:
            piece.reverse()
            domino_snake.insert(0, piece)

        else:
            player_pieces.insert((abs(inp) - 1), piece)
            print('Illegal move. Please try again.')
            return

    elif inp > 0:
        piece = player_pieces.pop(abs(inp) - 1)

        if piece[0] == domino_snake[-1][-1]:
            domino_snake.append(piece)

        elif piece[1] == domino_snake[-1][-1]:
            piece.reverse()
            domino_snake.append(piece)

        else:
            player_pieces.insert((abs(inp) - 1), piece)
            print('Illegal move. Please try again.')
            return

    elif inp == 0:

        if len(stock):
            player_pieces.append(stock.pop(0))
        else:
            print('Stock is empty')

    status = 'computer'
    game()

# Check the game
def endOfGame():

    # global domino_snake
    first_domino = domino_snake[0][1]
    last_domino = domino_snake[-1][-2]  # numbers on the ends

    join_domino_snake = [el for piece in domino_snake for el in piece]
    end = True

    # One of the players runs out of pieces:
    if len(player_pieces) == 0:
        print("Status: The game is over. You won!")

    elif len(computer_pieces) == 0:
        print("Status: The game is over. The computer won!")

    # The numbers on the ends of the snake are identical and appear within the snake 8 times:
    elif first_domino == last_domino and join_domino_snake.count(first_domino) >= 8:
        print("Status: The game is over. It's a draw!")
    else:
        end = False

    return end


# Game loop
while True:

    if status == 'computer':
        print('Status: Computer is about to make a move. Press Enter to continue...')
        aiMove()

    elif status == 'player':
        print("Status: It's your turn to make a move. Enter your command.")

        while True:
            try:
                move = int(input('>'))

                if abs(move) > len(player_pieces):
                    print('Invalid input. Please try again.')
                    continue
                else:
                    playerMove(move)
                break
            except ValueError:
                print('Invalid input. Please try again.')
                continue

    if endOfGame():
        break