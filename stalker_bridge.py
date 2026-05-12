import socket
import time
import os
import tkinter as tk
from threading import Thread

# --- CONFIGURATION (VERIFIED) ---
TWITCH_CHANNEL = "[...your lowercase name...]"
OAUTH_TOKEN = "[... your OAuth ...]"
STALKER_PATH = r"[...full gamepath...]\gamedata\config\twitch_spawn.ltx"

# --- FULL ITEM DICTIONARY ---
COMMANDS = {
    # Medicine
    "!medkit": "medkit",
    "!army": "medkit_army",
    "!sci": "medkit_scientic",
    "!bandage": "bandage",
    "!antirad": "antirad",
    # Food/Drink
    "!bread": "bread",
    "!vodka": "vodka",
    "!energy": "energy_drink",
    "!sausage": "kolbasa",
    # Ammo - 5.45 (Warsaw)
    "!545": "ammo_5.45x39_fmj",
    "!545ap": "ammo_5.45x39_ap",
    # Ammo - 5.56 (NATO)
    "!556": "ammo_5.56x45_ss109",
    "!556ap": "ammo_5.56x45_ap",
    # Ammo - 7.62
    "!762": "ammo_7.62x39_fmj",
    "!762ap": "ammo_7.62x39_ap",
    "!sniper": "ammo_7.62x54_7h1",
    # Ammo - Shotgun
    "!buck": "ammo_12x70_buck",
    "!slug": "ammo_12x76_zhekan",
}

class StalkerBridge:
    def __init__(self, root):
        self.root = root
        self.root.title("STALKER Twitch Bridge v2.0")
        self.root.geometry("600x400")
        
        self.status_label = tk.Label(root, text="Status: Disconnected", fg="red", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=5)
        
        self.log_box = tk.Text(root, height=15, width=70, state='disabled', bg="black", fg="lime")
        self.log_box.pack(pady=10, padx=10)
        
        self.start_btn = tk.Button(root, text="START BRIDGE", command=self.start_bridge, bg="gray20", fg="white", width=20)
        self.start_btn.pack(pady=5)

    def log(self, text):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {text}\n")
        self.log_box.see(tk.END) # Auto-scroll to bottom
        self.log_box.config(state='disabled')

    def start_bridge(self):
        self.start_btn.config(state='disabled')
        Thread(target=self.worker, daemon=True).start()

    def worker(self):
        sock = socket.socket()
        try:
            sock.connect(('irc.chat.twitch.tv', 6667))
            sock.send(f"PASS {OAUTH_TOKEN}\n".encode('utf-8'))
            sock.send(f"NICK {TWITCH_CHANNEL}\n".encode('utf-8'))
            # Request Tags to ensure we don't miss anything
            sock.send("CAP REQ :twitch.tv/membership twitch.tv/commands twitch.tv/tags\n".encode('utf-8'))
            sock.send(f"JOIN #{TWITCH_CHANNEL}\n".encode('utf-8'))
            self.status_label.config(text="Status: Connected", fg="green")
        except Exception as e:
            self.log(f"CONN ERROR: {e}")
            return

        while True:
            try:
                data = sock.recv(4096).decode('utf-8')
                if not data: break

                if data.startswith('PING'):
                    sock.send("PONG\n".encode('utf-8'))
                    continue

                # PARSING LOGIC: Extract clean message from Tags/IRC junk
                if "PRIVMSG" in data:
                    parts = data.split(" PRIVMSG ", 1)
                    if len(parts) > 1:
                        message_content = parts[1].split(" :", 1)
                        if len(message_content) > 1:
                            raw_msg = message_content[1].lower().strip()
                            self.log(f"CHAT: {raw_msg}")

                            # Matching & Writing
                            for chat_cmd, game_item in COMMANDS.items():
                                if chat_cmd in raw_msg:
                                    uid = int(time.time())
                                    try:
                                        with open(STALKER_PATH, "w") as f:
                                            f.write(f"[twitch]\nitem = {game_item}\nid = {uid}")
                                            f.flush() # Clear Python buffer
                                            os.fsync(f.fileno()) # Force Windows disk write
                                        self.log(f"DISK WRITE SUCCESS: {game_item}")
                                    except Exception as e:
                                        self.log(f"FILE ERROR: {e}")
            except Exception as e:
                self.log(f"RECEIVE ERROR: {e}")
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = StalkerBridge(root)
    root.mainloop()
