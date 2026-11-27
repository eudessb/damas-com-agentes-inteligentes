from src.game.game import CheckersGame

game = CheckersGame()

while not game.is_over():
    game.print_game()

    moves = game.get_legal_moves()

    print("\nMovimentos disponíveis:")

    for index, move in enumerate(moves):
        print(index, move)

    choice = int(input("\nEscolha um movimento: "))

    game.play_move(moves[choice])

print("\nPartida encerrada!")
print(game.get_result())
