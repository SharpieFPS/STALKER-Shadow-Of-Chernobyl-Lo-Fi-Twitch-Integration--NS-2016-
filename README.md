# STALKER-Shadow-Of-Chernobyl-Lo-Fi-Twitch-Integration
A program that builds a bridge between Twitch and game's bind_stalker.script file to spawn medkits, food, ammo.

To build it inside a folder that you are in, make sure python is installed on your computer and run:

1)pip install pyinstaller

2)pyinstaller --onefile --noconsole stalker_bridge.py

<img width="592" height="424" alt="image" src="https://github.com/user-attachments/assets/fd252816-ff62-4260-a935-8036bb240708" />

-----------INSTALLATION OF SCRIPTS------------

Put twitch_integration.script and bind_stalker.script in [game directory]\gamedata\scripts.

Make sure stuff in fsgame.ltx that relates to $game_data$ = true|	true| is set to as such, to true.

Get a unpacker and unpack your mod's files to get stalker_bridge.py and, inside of it, under object_binder.update(self, delta)
put twitch_integration.check_twitch_commands() - this calls for the twitch integration script when the game is running.

Or get it from this repo if you happen to be using the same NS version as I am (NS 2016 + 2023 Update).

And if you are not running any mods, unpack game's file and get it.

It's highly important because incompatible files are guaranteed to crash your game. 


I'm using Windows 10.

To run the program you need two script files.

One is bind_stalker.script.

And since I've created this program (with the use of AI of course, I'm not a programmer)
to work with the Narodnaya Solyanka mod and on non-enhanced STALKER (Steam version),
I had to extract bind_stalker.script from NS's files by using a unpacker (don't bother rar'ing or zip'ing it won't work)
and insert a line of code there that references the main script that works as a local Twitch agent so to say.

The AI called it twitch_integration.script and it's a script that check every two seconds for the content of another custom file, twitch_spawn.ltx.

Which is the last piece of the chain.

It's the file where the python script (the exe file) writes the items that are parsed from us typing stuff in our chat.


Again. It's a bespoke small program made specifically for NS to tackle its jankiness and it hasn't been tested properly and thoroughly.

It's working and I decided to post it here so it doens't get lost.

Hopefully no one else finds this repository lol.

But it can't be that bad since this script was made with AI.

If you are looking to adopt the script in your mod/version/build, just feed it to AI and it'll fix it for you.
