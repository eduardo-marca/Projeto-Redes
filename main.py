from multiprocessing import Process, Queue, freeze_support, set_start_method
from threading import Thread

from comunicador import Comunicador
from consts import PieceColor
from player import Player

def run_player(
    piece_color: PieceColor,
    window_position: tuple[int, int],
    outgoing_moves: Queue,
    incoming_moves: Queue,
) -> None:
    Player(piece_color, window_position, outgoing_moves, incoming_moves).start()


def forward_moves(
    source: Queue,
    destination: Queue,
    sender: Comunicador,
    receiver: Comunicador,
) -> None:
    """Bridge a process-safe queue through the supplied Comunicador.

    Comunicador stores messages in ordinary Python lists, so both endpoints must
    live in this (parent) process.  The queues are only the boundary between
    that shared memory and the two child processes.
    """
    while (message := source.get()) is not None:
        sender.enviarMensagem(message)
        destination.put(receiver.receberMensagem())


def main() -> None:
    white_to_server = Queue()
    black_to_server = Queue()
    to_white = Queue()
    to_black = Queue()

    # Same id => both endpoints use the Buffer supplied with the assignment.
    white_communicator = Comunicador(1)
    black_communicator = Comunicador(1)
    relays = [
        Thread(
            target=forward_moves,
            args=(white_to_server, to_black, white_communicator, black_communicator),
            name="white-to-black-relay",
        ),
        Thread(
            target=forward_moves,
            args=(black_to_server, to_white, black_communicator, white_communicator),
            name="black-to-white-relay",
        ),
    ]

    processes = [
        Process(
            target=run_player,
            args=(PieceColor.WHITE, (40, 40), white_to_server, to_white),
            name="white-player",
        ),
        Process(
            target=run_player,
            args=(PieceColor.BLACK, (880, 40), black_to_server, to_black),
            name="black-player",
        ),
    ]

    for relay in relays:
        relay.start()

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    for relay in relays:
        relay.join()

if __name__ == '__main__':
    freeze_support()
    set_start_method("spawn")
    main()
