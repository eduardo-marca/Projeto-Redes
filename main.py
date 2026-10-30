import argparse

import pygame

from consts import *
from player import Player
from network import NetworkConnection

def main():
    parser = argparse.ArgumentParser(description = "Network Chess")

    group = parser.add_mutually_exclusive_group(required = True)

    group.add_argument("--host", action = "store_true", help = "Host the game")

    group.add_argument("--client", metavar = "IP", help = "Connect to a game hosted at this IP address")

    args = parser.parse_args()

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Network Chess")

    try:
        icon = pygame.image.load("imgs/icon.png")
        pygame.display.set_icon(icon)
    except pygame.error:
        pass

    clock = pygame.time.Clock()

    try:
        if args.host:
            connection = NetworkConnection.create_server()
            color = PieceColor.WHITE
        else:
            connection = NetworkConnection.connect_to_server(args.client)
            color = PieceColor.BLACK

    except OSError as error:
        print(f"Network error: {error}")
        pygame.quit()
        return

    player = Player(color, screen, connection)

    running = True

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    player.handle_click(x, y)

            player.tick()
            screen.fill(BACKGROUND_COLOR)

            player.render()

            pygame.display.flip()

            clock.tick(60)

    except (ConnectionError, OSError) as error:
        print(f"Connection lost: {error}")

    finally:
        connection.close()
        pygame.quit()


if __name__ == "__main__":
    main()
    