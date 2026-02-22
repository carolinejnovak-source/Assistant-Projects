# How to Build Your AI Assistant — VPS Terminal Only
*Everything done from the command line. No GUI required.*

---

## What You're Building

A personal AI assistant that:
- Runs 24/7 on a cloud server
- You talk to it via **WhatsApp**
- It can write and deploy live web apps via GitHub + Render
- It remembers context between sessions

---

## Before You Start — Accounts to Create (on your laptop/phone)

Create these accounts first before touching the terminal:

| Account | URL | What you need from it |
|---|---|---|
| Hetzner (VPS host) | https://hetzner.com | Server IP address |
| Anthropic | https://console.anthropic.com | API key (sk-ant-...) |
| OpenClaw | https://openclaw.ai | License / account |
| GitHub | https://github.com | Personal access token |
| Render | https://render.com | API key (rnd_...) |
| WhatsApp | On your phone | A spare phone number not already on WhatsApp |

---

## PART 1: Create Your VPS on Hetzner

1. Log into https://hetzner.com → Cloud Console
2. Click **New Project** → name it anything
3. Click **Add Server**:
   - **Location:** Any (pick nearest to you)
   - **Image:** Ubuntu 24.04
   - **Type:** Shared CPU → **CX22** (~$4/month, 2 vCPU, 4GB RAM)
   - **SSH Keys:** Add your public key (recommended) OR use root password
4. Click **Create & Buy**
5. Wait ~30 seconds → copy your server's **Public IP address**

---

## PART 2: Connect to Your VPS

**On Mac/Linux** — open Terminal and run:
```bash
ssh root@YOUR_SERVER_IP
```

**On Windows** — use PowerShell or install [PuTTY](https://putty.org):
```
ssh root@YOUR_SERVER_IP
```

Type `yes` when asked about the fingerprint. You're now inside your server.

---

## PART 3: Update the Server

Run these commands to make sure everything is up to date:

```bash
apt update && apt upgrade -y
```

Wait for it to finish (1–2 minutes).

---

## PART 4: Install Node.js

OpenClaw requires Node.js version 20 or higher.

```bash
# Add the Node.js 22 repo
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -

# Install Node.js
apt install -y nodejs

# Verify it installed correctly
node --version
npm --version
```

You should see something like `v22.x.x` — that's correct.

---

## PART 5: Install OpenClaw

```bash
# Install OpenClaw globally
npm install -g openclaw

# Verify
openclaw --version
```

---

## PART 6: Configure OpenClaw with Your API Key

```bash
openclaw configure
```

The wizard will ask:
- **Anthropic API key** → paste your `sk-ant-...` key, press Enter
- **Default model** → type `anthropic/claude-sonnet-4-6`, press Enter
- **Workspace directory** → press Enter to accept default

---

## PART 7: Authorize Your Phone Number

This tells the assistant which WhatsApp number is allowed to talk to it:

```bash
openclaw configure --section auth
```

Enter your phone number in international format (e.g. `+16202108235`).

---

## PART 8: Connect WhatsApp

This works exactly like WhatsApp Web — scan a QR code with your phone:

```bash
openclaw configure --section whatsapp
```

A QR code will appear in the terminal.

On your phone:
1. Open WhatsApp
2. Tap the **three dots** (top right) → **Linked Devices**
3. Tap **Link a Device**
4. Point camera at the QR code in your terminal
5. Done ✅

> **Tip:** If the QR code looks garbled, make your terminal font smaller
> so the whole code fits on screen. Or zoom out with Ctrl+- (minus).

---

## PART 9: Start the Gateway

```bash
openclaw gateway start
```

To check it's running:
```bash
openclaw gateway status
```

You should see `running` or `active`. Send yourself a WhatsApp message to test — the assistant should respond.

---

## PART 10: Make It Run Forever (Survive Reboots)

Without this step, the assistant stops if the server restarts.

```bash
# Install as a system service
openclaw gateway install-service

# Enable it to start automatically on boot
systemctl enable openclaw

# Start it now
systemctl start openclaw

# Confirm it's running
systemctl status openclaw
```

You should see `Active: active (running)` in green.

---

## PART 11: Personalize Your Assistant

Now switch to WhatsApp and send these messages to your assistant:

```
Your name is [PICK A NAME]
My name is [YOUR NAME]
```

Then send your GitHub and Render tokens (see below how to get them):

```
Here's my GitHub token: ghp_xxxxxxxxxxxxxxxxx
Here's my Render API key: rnd_xxxxxxxxxxxxxxxxx
```

The assistant will save everything and remember it.

---

## PART 12: Get Your GitHub Token (on your laptop browser)

1. Log into GitHub → go to:
   **https://github.com/settings/tokens**
2. Click **Generate new token (classic)**
3. Name: `AI Assistant`
4. Expiration: `No expiration`
5. Check the box for **repo** (full control of private repos)
6. Scroll down → **Generate token**
7. Copy the token immediately (starts with `ghp_...`)
8. Send it to your assistant via WhatsApp

---

## PART 13: Get Your Render API Key (on your laptop browser)

1. Log into Render → go to:
   **https://dashboard.render.com/u/settings/api-keys**
2. Click **Create API Key**
3. Name: `AI Assistant`
4. Copy the key (starts with `rnd_...`)
5. Send it to your assistant via WhatsApp

---

## PART 14: Test Everything

In WhatsApp, ask your assistant:
```
Can you create a test GitHub repo called "hello-world" for me?
```

If it creates the repo, everything is wired up correctly. 🎉

---

## Useful Terminal Commands (for later)

```bash
# Check if the assistant is running
systemctl status openclaw

# Restart it
systemctl restart openclaw

# View live logs
openclaw gateway logs
# (press Ctrl+C to stop watching)

# Stop it
systemctl stop openclaw

# Update OpenClaw to latest version
npm update -g openclaw
```

---

## Troubleshooting

**WhatsApp disconnected / not responding:**
```bash
systemctl restart openclaw
# Then re-scan the WhatsApp QR code:
openclaw configure --section whatsapp
```

**"Command not found" errors:**
```bash
# Make sure Node is installed
node --version
# Re-install OpenClaw if needed
npm install -g openclaw
```

**Server ran out of memory:**
```bash
# Check usage
free -h
# Upgrade your Hetzner plan if needed (CX32 is next step up)
```

---

## Cost Summary

| Item | Cost |
|---|---|
| Hetzner CX22 VPS | ~$5/month |
| Anthropic API (Claude) | ~$5–20/month (depends on usage) |
| Render | Free tier = $0 |
| GitHub | Free = $0 |
| Extra phone number (optional) | ~$1–3/month or one-time SIM |
| **Total** | **~$10–25/month** |

---

## Architecture Summary

```
You → WhatsApp → OpenClaw Gateway (on VPS) → Claude AI (Anthropic)
                        ↓
              GitHub (code storage) + Render (live web apps)
```

---

*Guide created: February 2026*
*For: Caroline Novak / VTC Assistant Project*
