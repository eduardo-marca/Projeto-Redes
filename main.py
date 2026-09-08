from multiprocessing import Process, freeze_support, set_start_method

from consts import PieceColor
from player import Player

def run_player(piece_color: PieceColor, window_position: tuple[int, int]) -> None:
    Player(piece_color, window_position).start()


def main() -> None:
    processes = [
        Process(
            target=run_player,
            args=(PieceColor.WHITE, (40, 40)),
            name="white-player",
        ),
        Process(
            target=run_player,
            args=(PieceColor.BLACK, (880, 40)),
            name="black-player",
        ),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

if __name__ == '__main__':
    freeze_support()
    set_start_method("spawn")
    main()
