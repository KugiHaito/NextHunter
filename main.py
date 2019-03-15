from MyGame import Gameboard

game = Gameboard.Game(
    name = "Next Hunter",
    icon = "resources/img/icon.png",
    size = (1280, 640),
    tile_size = 32,
    resources = {
        "maps": "resources/maps",
        "tilemaps": "resources/img/tilemaps",
        "entities": "resources/img/entities",
        "font": ["resources/fonts/8_bit_light.ttf", 12]
    }
)

game.selectDefault(1, 2)

if __name__ == '__main__':
	game.run()