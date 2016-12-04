#twitch-game-of-life

Submission for CU Local Hack Day 2016

#Usage

First, install requirements.

    $ pip install -r requirements.txt
    
Then create a file called settings.py with this in it:

    PASS = b"oath:xxx"
    USER = b"username"
  
replacing values where necessary. Note the string must be bytes. PASS is your streaming key to connect to chat. 
USER is the username associate to the streaming key. Note you will join the chat room of USER too. 
Finally, run 

    $ python run.py
    
to start the game window. You can use OBS to then stream the window to Twitch.