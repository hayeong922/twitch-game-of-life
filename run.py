from conway import Conway, create_block
game = Conway(100,100)
create_block(game.grid, 50, 50)
game.loop()