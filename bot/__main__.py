from . import updater, app
# Load callbacks and commands
from . import callbacks, commands
from threading import Thread
from pyrogram import idle


app.start()
Thread(target=updater.run, args=()).start()
print("Bot started!")
idle()