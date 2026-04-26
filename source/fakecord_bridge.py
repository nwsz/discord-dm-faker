#!/usr/bin/env python3
"""
fakecord Discord Bridge
------------------------
Fixed Version: Cross-platform compatible. 
Runs the server in the main thread for better stability and easier shutdown.
"""

import http.server
import json
import os
import sys
import base64
import urllib.request
import urllib.error
import socket

# ── helpers ──────────────────────────────────────────────────────────────────

CDN = "https://cdn.discordapp.com"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_free_port():
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def fetch_json(url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bot {token}",
            "User-Agent": "fakecord-bridge/2.0",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def img_to_data_uri(url: str) -> str | None:
    if not url:
        return None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "fakecord-bridge/2.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            ct = resp.headers.get("Content-Type", "image/png").split(";")[0].strip()
            b64 = base64.b64encode(data).decode()
            return f"data:{ct};base64,{b64}"
    except Exception as e:
        print(f"  ⚠ Could not download {url[:60]}... : {e}")
        return url


def build_user_payload(user: dict) -> dict:
    uid = user["id"]

    # Avatar
    ah = user.get("avatar")
    if ah:
        ext = "gif" if ah.startswith("a_") else "png"
        avatar_url = f"{CDN}/avatars/{uid}/{ah}.{ext}?size=256"
    else:
        disc = user.get("discriminator", "0") or "0"
        idx = (int(uid) >> 22) % 6 if disc == "0" else int(disc) % 5
        avatar_url = f"{CDN}/embed/avatars/{idx}.png"

    # Banner
    bh = user.get("banner")
    banner_url = None
    if bh:
        ext = "gif" if bh.startswith("a_") else "png"
        banner_url = f"{CDN}/banners/{uid}/{bh}.{ext}?size=600"

    # Decoration
    deco = user.get("avatar_decoration_data") or {}
    deco_url = None
    if deco.get("asset"):
        deco_url = f"{CDN}/avatar-decoration-presets/{deco['asset']}.png?size=96&passthrough=true"

    # Clan
    clan = user.get("clan") or {}
    clan_badge_url = None
    if clan.get("badge") and clan.get("identity_guild_id"):
        clan_badge_url = f"{CDN}/clan-badges/{clan['identity_guild_id']}/{clan['badge']}.png?size=16"

    disc = user.get("discriminator", "0") or "0"
    handle = f"@{user['username']}" if disc == "0" else f"{user['username']}#{disc}"
    display_name = user.get("global_name") or user["username"]
    accent = user.get("accent_color")
    accent_hex = f"#{accent:06x}" if accent else "#5865f2"

    print(f"  → Downloading assets...")
    avatar_uri = img_to_data_uri(avatar_url)
    deco_uri = img_to_data_uri(deco_url) if deco_url else None
    clan_badge_uri = img_to_data_uri(clan_badge_url) if clan_badge_url else None

    return {
        "id": uid,
        "username": user["username"],
        "global_name": user.get("global_name"),
        "display_name": display_name,
        "handle": handle,
        "discriminator": disc,
        "bot": user.get("bot", False),
        "accent_color": accent_hex,
        "avatar_url": avatar_url,
        "avatar_data_uri": avatar_uri,
        "banner_url": banner_url,
        "decoration_url": deco_url,
        "decoration_data_uri": deco_uri,
        "clan": {
            "tag": clan.get("tag"),
            "badge_url": clan_badge_url,
            "badge_data_uri": clan_badge_uri,
            "identity_guild_id": clan.get("identity_guild_id"),
        } if clan.get("tag") else None,
    }


# ── HTTP handler ──────────────────────────────────────────────────────────────

class BridgeHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass  # silence default access log

    def send_json(self, code: int, obj: dict):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/ping":
            self.send_json(200, {"status": "ok", "name": "fakecord-bridge"})
        else:
            self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/fetch":
            self.send_json(404, {"error": "Not found"})
            return

        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length).decode())
        except Exception:
            self.send_json(400, {"error": "Bad JSON"})
            return

        token = body.get("token", "").strip()
        user_id = body.get("userId", "").strip()

        if not token or not user_id:
            self.send_json(400, {"error": "Missing token or userId"})
            return

        print(f"\n📥 Fetch request → user {user_id}")

        try:
            user = fetch_json(f"https://discord.com/api/v10/users/{user_id}", token)
        except urllib.error.HTTPError as e:
            err_body = {}
            try:
                err_body = json.loads(e.read().decode())
            except Exception:
                pass
            msg = err_body.get("message", f"HTTP {e.code}")
            print(f"  ✗ Discord API error {e.code}: {msg}")
            self.send_json(e.code, {"error": msg, "code": err_body.get("code")})
            return
        except Exception as e:
            print(f"  ✗ Error: {e}")
            self.send_json(500, {"error": str(e)})
            return

        display = user.get("global_name") or user["username"]
        print(f"  ✓ Found: {display} (@{user['username']})")

        try:
            payload = build_user_payload(user)
        except Exception as e:
            print(f"  ✗ Build error: {e}")
            self.send_json(500, {"error": f"Asset build failed: {e}"})
            return

        print(f"  ✓ Done → sending to browser")
        self.send_json(200, payload)


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    port = find_free_port()
    port_file = os.path.join(SCRIPT_DIR, "bridge_port.txt")

    server = http.server.HTTPServer(("127.0.0.1", port), BridgeHandler)

    with open(port_file, "w") as f:
        f.write(str(port))

    print("=" * 52)
    print("  fakecord Bridge  ·  running on port", port)
    print("=" * 52)
    print(f"\n  ✓ Port written to: bridge_port.txt")
    print(f"  ✓ Open fakecord.html — it will auto-detect")
    print(f"\n  Press Ctrl+C to stop.\n")

    try:
        # This keeps the script running and listening until you hit Ctrl+C
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nStopping bridge...")
    finally:
        # Cleanup happens here whether you hit Ctrl+C or it crashes
        if os.path.exists(port_file):
            os.remove(port_file)
        server.server_close()
        sys.exit(0)


if __name__ == "__main__":
    main()
