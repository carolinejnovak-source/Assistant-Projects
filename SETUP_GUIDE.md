# How to Set Up Your AI Assistant (Mikalina / OpenClaw)
*Step-by-step recreation guide*

---

## What You're Building

A personal AI assistant that:
- Runs 24/7 on a cloud server (VPS)
- Is powered by Anthropic's Claude AI model
- You talk to it via **WhatsApp** (or any other messaging app)
- It can write and deploy code to the internet via GitHub + Render
- It remembers context between conversations

---

## What You Need (Accounts to Create First)

Before starting, create free/paid accounts at:

1. **A VPS provider** — [Hetzner](https://hetzner.com) (cheapest, recommended), DigitalOcean, or Linode
   - Plan: ~$4–6/month for a basic server is plenty
   - OS: **Ubuntu 24.04 LTS**

2. **Anthropic** — https://console.anthropic.com
   - Sign up and add a payment method
   - You'll create an API key here

3. **OpenClaw** — https://openclaw.ai
   - The software that runs the assistant and connects everything together

4. **GitHub** — https://github.com
   - For storing and deploying code

5. **Render** — https://render.com
   - For hosting live web apps (free tier available)

6. **WhatsApp Business** — https://business.whatsapp.com
   - You need a phone number NOT already on WhatsApp
   - A cheap SIM card or Google Voice number works fine

---

## Step 1: Create Your VPS

1. Log into Hetzner (or your provider of choice)
2. Create a new server:
   - **Location:** Any (pick closest to you)
   - **OS:** Ubuntu 24.04
   - **Plan:** CPX11 or CX22 (~$4–6/month) — 2 vCPU, 2–4GB RAM
3. Add your SSH key (or use a password)
4. Once created, note your server's **IP address**

---

## Step 2: Connect to Your Server

Open Terminal (Mac) or PowerShell (Windows) and run:

```bash
ssh root@YOUR_SERVER_IP
```

---

## Step 3: Install OpenClaw

Once connected to your server, run these commands one at a time:

```bash
# Update the system
apt update && apt upgrade -y

# Install Node.js (v22+)
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# Install OpenClaw globally
npm install -g openclaw

# Verify it installed
openclaw --version
```

---

## Step 4: Get Your Anthropic API Key

1. Go to https://console.anthropic.com
2. Click **API Keys** → **Create Key**
3. Copy the key (starts with `sk-ant-...`)
4. Keep this secret — it's your AI brain

---

## Step 5: Configure OpenClaw

Run the OpenClaw setup wizard:

```bash
openclaw configure
```

It will ask you:
- **Anthropic API key** → paste your `sk-ant-...` key
- **Model** → type `claude-sonnet-4-6` (or the latest Claude Sonnet)
- **Workspace** → press Enter for default (`~/.openclaw/workspace`)

---

## Step 6: Start the Gateway

```bash
# Start OpenClaw as a background service
openclaw gateway start

# Check it's running
openclaw gateway status
```

---

## Step 7: Connect WhatsApp

This uses **WhatsApp linking** (like WhatsApp Web — no Business API needed):

```bash
openclaw configure --section whatsapp
```

1. It will display a **QR code** in the terminal
2. On your phone, open WhatsApp → **Linked Devices** → **Link a Device**
3. Scan the QR code
4. Done — WhatsApp is now connected

> **Note:** The phone number you use here becomes your assistant's WhatsApp number.
> Using a second/separate number (not your personal one) is recommended.
> A cheap prepaid SIM or a Google Voice number works.

---

## Step 8: Make It Persist (Survive Reboots)

So the assistant keeps running even if the server restarts:

```bash
# Create a systemd service
openclaw gateway install-service

# Enable it to start on boot
systemctl enable openclaw
systemctl start openclaw

# Check it's running
systemctl status openclaw
```

---

## Step 9: Connect GitHub

1. Go to https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Give it a name (e.g. "Mikalina Assistant")
4. Select scopes: **repo** (full control of private repos)
5. Click **Generate token** — copy it immediately

Send the token to your assistant via WhatsApp:
> "Here's my GitHub token: ghp_xxxxxxxxxxxxx"

---

## Step 10: Connect Render

1. Go to https://render.com → sign in
2. Go to **Account Settings** → **API Keys** → **Create API Key**
3. Copy the key (starts with `rnd_...`)

Send it to your assistant via WhatsApp:
> "Here's my Render API key: rnd_xxxxxxxxxxxxx"

---

## Step 11: Personalize Your Assistant

Send messages to your assistant to set it up:
- **"Your name is [NAME]"**
- **"My name is [YOUR NAME]"**
- **"My email is [your@email.com]"**
- **"Here's my GitHub token: ..."**
- **"Here's my Render API key: ..."**

The assistant saves all of this and remembers it going forward.

---

## How It All Works Together

```
You (WhatsApp)
      ↓
OpenClaw Gateway (running on your VPS)
      ↓
Claude AI (Anthropic) — the brain
      ↓
GitHub — stores all code
      ↓
Render — hosts the live web apps
```

- You chat via **WhatsApp**
- The assistant uses **Claude** to think and respond
- When you want a web app built, the assistant writes the code,
  pushes it to **GitHub**, and deploys it to **Render**
- You get a live URL within minutes

---

## Cost Summary

| Service | Cost |
|---|---|
| VPS (Hetzner CX22) | ~$5/month |
| Anthropic API (Claude) | ~$5–20/month depending on usage |
| Render (free tier) | $0 |
| GitHub | $0 |
| WhatsApp | $0 (uses your existing app) |
| **Total** | **~$10–25/month** |

---

## Troubleshooting

**WhatsApp disconnects:**
```bash
openclaw gateway restart
# Then re-scan the QR code
```

**Check logs:**
```bash
openclaw gateway logs
# or
journalctl -u openclaw -f
```

**Restart everything:**
```bash
systemctl restart openclaw
```

---

## Security Tips

- Don't share your API keys publicly
- Use a dedicated phone number for the assistant, not your personal one
- The assistant only responds to phone numbers you authorize (configured in OpenClaw)
- Keep your VPS updated: `apt update && apt upgrade -y`

---

*Document created: February 2026*
*Setup created by: Caroline Novak*
*Assistant: Mikalina (OpenClaw + Claude Sonnet)*
