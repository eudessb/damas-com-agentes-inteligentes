
from src.game.board import Board
from src.game.game import CheckersGame
from src.agents.random_agent import RandomAgent


def print_moves(moves):
    for index, move in enumerate(moves):
        if isinstance(move, list):
            description = " -> ".join(
                str(step["to"]) for step in move
            )
            description = f'{move[0]["from"]} -> {description}'
        else:
            description = f'{move["from"]} -> {move["to"]}'

        print(f"{index}: {description}")


def main():
    game = CheckersGame()
    agent = RandomAgent()

    human_player = Board.WHITE

    print("=== DAMAS: VOCÊ VS RANDOM AGENT ===")
    print("Você joga com as brancas.")
    print("O agente joga com as pretas.")

    while not game.is_over():
        game.print_game()

        if game.current_player == human_player:
            moves = game.get_legal_moves()

            print("\nSeus movimentos disponíveis:")
            print_moves(moves)

            while True:
                try:
                    choice = int(input("\nEscolha o número do movimento: "))

                    if 0 <= choice < len(moves):
                        break

                    print("Número inválido.")

                except ValueError:
                    print("Digite um número válido.")

            game.play_move(moves[choice])

        else:
            print("\nRandom Agent está pensando...")

            move = agent.choose_move(game)
            print(f"Random Agent escolheu: {move}")

            game.play_move(move)

    game.print_game()

    result = game.get_result()

    print("\n=== FIM DE JOGO ===")

    if result["winner"] == human_player:
        print("Você venceu!")
    elif result["winner"] is not None:
        print("Random Agent venceu!")
    else:
        print("Empate!")


if __name__ == "__main__":
    main()
