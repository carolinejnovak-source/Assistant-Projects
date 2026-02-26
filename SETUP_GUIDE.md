# How to Build Your AI Assistant — VPS Setup Guide
*Everything done from the command line. No GUI required.*

---

## What You're Building

A personal AI assistant that:
- Runs 24/7 on a cloud server (VPS)
- You talk to it via **WhatsApp**
- It can write and deploy live web apps via GitHub + Render
- It remembers context between sessions

---

## Before You Start — Accounts to Create (on your laptop/phone)

Create these accounts first before touching the terminal:

| Account | URL | What you need from it |
|---|---|---|
| VPS Host | Hetzner, Hostinger, DigitalOcean, etc. | Server IP address |
| Anthropic | https://console.anthropic.com | API key (sk-ant-...) |
| GitHub | https://github.com | Personal access token |
| Render | https://render.com | API key (rnd_...) |
| WhatsApp | On your phone | A spare phone number not already on WhatsApp |

> **Important — Anthropic billing:** New accounts start on Tier 1 with a 30,000 token/minute limit. Add at least $5 of credit at [console.anthropic.com/settings/billing](https://console.anthropic.com/settings/billing) to unlock higher rate limits. Otherwise your assistant may hit errors when first starting up.

---

## PART 1: Create Your VPS

Choose any VPS provider. Recommended specs:

- **OS:** Ubuntu 22.04 or 24.04
- **RAM:** 2 GB minimum (4 GB recommended)
- **Cost:** ~$4–6/month (e.g. Hetzner CX22, Hostinger KVM 2, DigitalOcean Basic)

After creating your server, copy the **Public IP address** from your provider's dashboard.

---

## PART 2: Connect to Your VPS

**All setup commands run on your VPS — not your local computer.**
Your local terminal (PowerShell, Terminal app, etc.) is just the doorway to get there.

**On Mac/Linux** — open Terminal and run:
```bash
ssh root@YOUR_SERVER_IP
```

**On Windows** — open **PowerShell** (built into Windows — press Win+X and click Terminal or PowerShell):
```
ssh root@YOUR_SERVER_IP
```

> No need to install extra software on Windows — PowerShell has SSH built in.
> Type `yes` when asked about the fingerprint. You're now inside your server.

Once connected, **every command below runs inside this SSH session.**

---

## PART 3: Update the Server

```bash
apt update && apt upgrade -y
```

Wait 1–2 minutes for it to finish.

---

## PART 4: Install Node.js

OpenClaw requires Node.js version 20 or higher.

```bash
# Add the Node.js 22 repo
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -

# Install Node.js
apt install -y nodejs

# Verify
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

## PART 6: Run the Setup Wizard

OpenClaw has an interactive setup wizard that handles everything:

```bash
openclaw onboard
```

The wizard walks you through:
1. If asked **"Where will the Gateway run?"** → select **Local (this machine)**
2. Entering your **Anthropic API key** (`sk-ant-...`) — paste directly, never via chat
3. Choosing a default model (accept the default)
4. Setting your workspace directory (press Enter to accept default)
5. A gateway token is generated and saved automatically

When asked **"How do you want to hatch your bot?"** — select **Hatch in TUI (recommended)** and press Enter.

The TUI (terminal interface) will open. You'll see your assistant come online with the message **"Wake up, my friend!"**

---

## PART 7: Authorize Your Phone Number

In the TUI, or in a separate SSH session, run:

```bash
openclaw configure --section auth
```

Enter your WhatsApp phone number in international format (e.g. `+16202108235`).

This is the number your assistant will listen to.

---

## PART 8: Connect WhatsApp

Works exactly like WhatsApp Web — scan a QR code with your phone:

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

> **Tip:** If the QR code looks garbled, make your terminal font smaller so the full code fits on screen.

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

**Do not skip this step.** Without it, the assistant stops whenever the server restarts.

Open a second SSH session (or a new PowerShell window and SSH in again) and run:

```bash
# Install as a system service
openclaw gateway install-service

# Reload systemd so it sees the new service file
systemctl daemon-reload

# Try system-level first:
systemctl enable openclaw-gateway
systemctl start openclaw-gateway
systemctl status openclaw-gateway
```

If you see **`Unit openclaw-gateway.service not found`**, the service was installed at user level instead. Run these instead:

```bash
systemctl --user daemon-reload
systemctl --user enable openclaw-gateway
systemctl --user start openclaw-gateway
loginctl enable-linger root
systemctl --user status openclaw-gateway
```

You should see **`Active: active (running)`** in green either way.

> **Note:** The service is registered as `openclaw-gateway`, not `openclaw`. Always use `openclaw-gateway` with systemctl commands.

---

## PART 11: Personalize Your Assistant

Switch to WhatsApp and introduce yourself:

```
Your name is [PICK A NAME]
My name is [YOUR NAME]
```

Your assistant will remember this going forward.

> **Security note:** Never send API keys or tokens over WhatsApp (or any chat). Always paste credentials directly into the terminal. See Parts 12 & 13 for how to add your GitHub and Render keys securely via the terminal.

---

## PART 12: Add Your GitHub Token

**Step 1 — Get the token** (in your browser):
1. Log into GitHub → go to: **https://github.com/settings/tokens**
2. Click **Generate new token (classic)**
3. Name: `AI Assistant`
4. Expiration: `No expiration`
5. Check **repo** (full control of private repos)
6. Scroll down → **Generate token**
7. Copy the token (starts with `ghp_...`)

**Step 2 — Save it on your VPS** (in your terminal):
```bash
openclaw configure
```
If asked **"Where will the Gateway run?"** → select **Local (this machine)**.
Arrow down to **Web tools** (or the GitHub section) → paste your token when prompted.

> ⚠️ Never paste API keys or tokens into WhatsApp or any chat app. Always enter them directly in the terminal.

---

## PART 13: Add Your Render API Key

**Step 1 — Get the key** (in your browser):
1. Log into Render → go to: **https://dashboard.render.com/u/settings/api-keys**
2. Click **Create API Key**
3. Name: `AI Assistant`
4. Copy the key (starts with `rnd_...`)

**Step 2 — Save it on your VPS** (in your terminal):
```bash
openclaw configure
```
Navigate to the relevant section and paste your Render key when prompted.

> ⚠️ Same rule — terminal only, never via chat.

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
systemctl status openclaw-gateway

# Restart it
systemctl restart openclaw-gateway

# View live logs
openclaw gateway logs
# (press Ctrl+C to stop watching)

# Stop it
systemctl stop openclaw-gateway

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

**HTTP 429 rate_limit_error on first message:**
Your Anthropic account is on Tier 1 (30k token/min limit).
→ Add credit at [console.anthropic.com/settings/billing](https://console.anthropic.com/settings/billing) to unlock higher limits.
→ Wait 60 seconds and try again — limits reset per minute.

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
# Upgrade your VPS plan if needed (next tier up is usually ~$8–10/month)
```

---

## Cost Summary

| Item | Cost |
|---|---|
| VPS (e.g. Hetzner CX22, Hostinger KVM 2) | ~$4–6/month |
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
*Updated: February 2026 — added Windows PowerShell instructions, Anthropic billing note, rate limit troubleshooting, onboard wizard clarifications*  
*For: Caroline Novak / VTC Assistant Project*
