# 🐊 Discord Direct Message Spoofer
Make any user say any message, all from your browser. Add any user profile picture, role icon, role colour, BOT verified tag, add realistic embeds, add images, and add built in links all in the same place. It's never been easier to pretend your friend said something they truly didn't.

**Please take note...**
> - Many groups may ban you from their discords or punish you for forging evidence in reports, etc. You are held responsible for anything you use this tool to do.
> - The tool has multiple versions all which can do different things. Make sure you use one that suits your needs properly.
> - This code was contributed to the "heist" discord bot - and the owner of it has access to this repo. Please be wary if you see something that doesn't look right (contact me on discord @nwsfuz). I recommend you use the heist bot as it is very useful and has features like this which incorporate some of this technology (if you want to call it that).

# ✨ fakecord v2.0
A powerful, fully-local tool to generate highly accurate Discord message mockups. 

**Why a local version?** To provide the most accurate mockups (including decorations and animated avatars), fakecord needs to talk directly to the Discord API. Browsers block this for security reasons (CORS). fakecord v2.0 solves this by running a tiny, secure local Python bridge on your machine. This makes the tool vastly more powerful, secure, and reliable than previous web-only versions.

## 🚀 What's New in v2.0
* **Avatar Decorations:** Full support for custom profile decorations.
* **Animated Avatars:** GIF avatars now load natively via the Discord API.
* **Server/Clan Tags:** Accurately renders the new Discord guild/clan tags.
* **Deselect Block:** Click off a block to deselect it for easier canvas management.

---
## 🛠️ Requirements
Before you begin, you will need:
1. **Python 3.x** installed on your computer.
2. A modern web browser.

## 📖 Step-by-Step Installation Guide

### Phase 1: Get a Discord Bot Token
*fakecord requires a bot token purely to read public user data (like avatars and decorations) from Discord's API. We never store this token; it stays entirely inside your browser's local memory.*

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications/).
2. Click **New Application** in the top right corner and give it a name.
3. In the left sidebar, click on **Bot**.
4. Look for the "Token" section and click **Reset Token**. 
5. **Copy this token** and keep it somewhere safe. *(Warning: Never share your bot token with anyone!)*

### Phase 2: Running the Local Bridge
1. Download or clone this repository to your computer.
2. Double-click `index.html` to open the fakecord interface in your web browser.
3. Open your terminal or command prompt, navigate to the folder where you downloaded fakecord, and run the bridge script:
   ```bash
   python fakecord_bridge.py
   ```
   *(Note: Depending on your system, you might need to type `python3` instead). Make sure you install the required packages with `pip install _____`*
4. Keep the terminal window open! The script will print a **Port Number** (e.g., `running on port 54321`). 

### Phase 3: Connect and Create
1. Go back to `index.html` in your browser.
2. The UI will try to auto-detect the bridge. If it says "Bridge offline" (which often happens when opening files directly from your PC), simply click **Set Port manually** and type the port number from your terminal.
3. Click **Set Bot Token** and paste the token you got in Phase 1. *(Remember: This clears as soon as you refresh the page).*
4. Grab a **Discord User ID** (Right-click a user in Discord > Copy User ID).
5. Paste the ID into the sidebar and click **Fetch via Bridge**.
6. Once their profile card appears, select a message block on the canvas and click **Apply Everything** to instantly inject their real avatar, name, decorations, and tags!

---

## 💡 Usage Tips
* **Editing Text:** Just click on any username, timestamp, or message text on the canvas to edit it directly.
* **Reactions:** You can add reactions from the sidebar. To delete a reaction, just **right-click** it on the canvas.
* **Exporting:** Once your mockup is perfect, hit the **Export** button in the top left to save it as a high-quality, transparent PNG.
* **Themes:** Toggle between Light and Dark mode using the sun/moon icon at the top of the sidebar.
-# *Disclaimer: This project is not affiliated with, endorsed, or sponsored by Discord.*
