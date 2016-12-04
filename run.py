'''from threading import Thread

from conway import Conway, create_block
from chat import Chat

def update_flips(game, chat):
    while True:
        for message in chat.get_messages():
            if message.startswith("flip"):
                split = message[4:].strip().split(",")
                if len(split) == 2 and all([n.isnumeric() for n in split]):
                    print("Flipped {}".format(split)) 
                    game.flip_queue.append(split)

game = Conway(200,200)
chat = Chat()
create_block(game.grid, 100, 100)
if __name__ == "__main__":
    game_thread = Thread(target=game.loop)
    chat_thread = Thread(target=update_flips, args=(game,chat))
    game_thread.start()
    chat_thread.start()'''

from conway import Conway, create_block
game = Conway(100,100)
create_block(game.grid, 50, 50)
game.loop()