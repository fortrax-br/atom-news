# Load callbacks, commands and other things
from threading import Thread
from pyrogram import idle
from . import app, updater, callbacks, commands


STOP = False

app.start()
update_loop = Thread(target=updater.run, args=(lambda: STOP,))
update_loop.start()
print("Bot started! Press CTRL+C to stop.")
idle()
print("Please await...")
STOP = True
app.stop()
update_loop.join()
print("Bot finished!")
