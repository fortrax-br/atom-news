from . import updater, app
# Load callbacks and commands
from . import callbacks, commands
from threading import Thread
from pyrogram import idle


app.start()
update_loop = Thread(target=updater.run)
update_loop.start()
update_loop._tstate_lock.release()
print("Bot started! Press CTRL+C to stop.")
idle()
print("Stopping bot...")
app.stop()