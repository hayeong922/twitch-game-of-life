import socket

from settings import PASS, USER

class Chat:
    def __init__(self):
        s = socket.socket()
        s.connect(("irc.twitch.tv", 6667))
        s.send(b"PASS " + PASS + b"\r\n")
        s.send(b"NICK " + USER + b"\r\n")
        s.send(b"JOIN #" + USER + b"\r\n")
        s.recv(1024)
        self.socket = s

    def get_messages(self):
        try:
            input = self.socket.recv(1024).decode("utf8").split("\r\n")[:-1]
            return [s.split(":", 2)[2] for s in input]
        except:
            return []