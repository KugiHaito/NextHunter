from MyGame.Gameboard import Game

game = Game(
    name="Next Hunter",
    icon="icon.png",
    size=(1280, 640),
    tile_size=32,
    resources="resources/texturepacks"
)

if __name__ == "__main__":
    game.run()
