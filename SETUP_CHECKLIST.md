# API Keys Setup Checklist - Step by Step

Follow these steps IN ORDER. After each step, you'll get a key/token. 
Paste ALL keys into the `.env` file I'll create for you.

## STEP 1: Groq API (REQUIRED - Primary AI)
**What you do:**
1. Open browser, go to: https://console.groq.com
2. Click **"Sign up"** (use Google/GitHub/Email)
3. After login, click **"API Keys"** (left sidebar)
4. Click **"Create API Key"**
5. Name: `blog-ai-agent`
6. **COPY THE KEY** (starts with `gsk_`)
7. **⚠️ IMPORTANT:** You won't see it again!

**Then tell me:** "Groq key: [paste your key here]"

---

## STEP 2: Hashnode (REQUIRED - Blog Platform)
**What you do:**
1. Go to: https://hashnode.com
2. Click **"Get Started"**
3. Sign up (Google/GitHub/Email)
4. Create blog: Name it, choose subdomain (e.g., `yourname.hashnode.dev`)
5. Go to **Dashboard → Settings → API**
6. Click **"Generate API Key"**
7. **COPY THE KEY**
8. Also get **Publication ID**: Settings → General → look for "Publication ID"

**Then tell me:** "Hashnode key: [paste key]" and "Publication ID: [paste ID]"

---

## STEP 3: Telegram Bot (EASIEST Social Media)
**What you do:**
1. Open **Telegram app** on phone/desktop
2. Search for: `@BotFather`
3. Send: `/newbot`
4. Follow prompts:
   - Enter display name: `Blog AI Agent`
   - Enter username (must end in `bot`): `yourname_bot`
5. BotFather gives you a **Bot Token** (looks like: `123456789:ABCdef...`)
6. **COPY THIS TOKEN**
7. Create a Telegram Channel:
   - In Telegram: Click "New Channel"
   - Name it: `Your Blog Updates`
   - Set to "Public Channel"
8. Add your bot as admin:
   - Channel → Manage → Administrators → Add Admin → search your bot
   - Give it "Post Messages" permission
9. Get Channel ID:
   - Forward any message from your channel to `@userinfobot`
   - It will tell you the channel ID (starts with `-100...`)

**Then tell me:** "Telegram token: [paste token]" and "Channel ID: [paste ID]"

---

## STEP 4: Google Gemini API (Backup AI - Optional)
**What you do:**
1. Go to: https://aistudio.google.com
2. Sign in with Google account
3. Click **"Get API key"** (left sidebar)
4. Create key in new project
5. **COPY THE KEY** (starts with `AIzaSy...`)

**Then tell me:** "Gemini key: [paste key]"

---

## STEP 5: Discord Webhook (EASIEST - No API key needed!)
**What you do:**
1. Open **Discord app**
2. Create a server (or use existing):
   - Click "+" → "Create My Own" → Name it
3. Go to channel → Click gear icon (Edit Channel)
4. Go to **Integrations → Webhooks → New Webhook**
5. Name: `Blog AI Agent`
6. Click **"Copy Webhook URL"** (looks like: `https://discord.com/api/webhooks/...`)

**Then tell me:** "Discord webhook: [paste URL]"

---

## STEP 6: Twitter/X (Optional - 1500 tweets/month free)
**What you do:**
1. Go to: https://developer.twitter.com
2. Sign up/log in with Twitter account
3. Apply for developer account:
   - Use case: `Automated news aggregation bot that reads public news and posts summaries`
4. After approval, create app:
   - Go to Projects & Apps → Create App
5. Get these FOUR keys:
   - API Key
   - API Secret Key
   - Access Token
   - Access Token Secret

**Then tell me:** "Twitter keys: [paste all 4 keys]"

---

## STEP 7: Reddit (Optional)
**What you do:**
1. Log in to: https://reddit.com
2. Go to: https://www.reddit.com/prefs/apps
3. Click **"create another app..."**
4. Fill in:
   - name: `blog-ai-agent`
   - Select **"script"**
   - about url: (leave blank)
   - redirect uri: `http://localhost:8080`
5. Click **"create app"**
6. You'll see:
   - **CLIENT ID** (under app name, grey text)
   - **CLIENT SECRET** (labeled "secret")

**Then tell me:** "Reddit keys: [paste client ID and secret]" + your Reddit username & password

---

## STEP 8: LinkedIn (Optional)
**What you do:**
1. Go to: https://www.linkedin.com/developers/
2. Click **"Create app"**
3. Fill in: name, logo, description
4. After creating, go to **Auth tab**
5. Generate an **Access Token**

**Then tell me:** "LinkedIn token: [paste token]"

---

## STEP 9: Mastodon (Optional - Unlimited, Free)
**What you do:**
1. Go to: https://mastodon.social
2. Sign up
3. Go to **Settings → Development → New Application**
4. Name: `Blog AI Agent`
5. Scopes: Check `read` and `write`
6. Submit
7. **COPY THE ACCESS TOKEN**

**Then tell me:** "Mastodon token: [paste token]"

---

## STEP 10: Image APIs (Optional - for video generation)
Choose ONE or ALL:

### Unsplash (50 requests/hour)
1. https://unsplash.com/developers
2. Register as developer → New Application
3. Get **Access Key**

### Pexels (200 requests/hour)
1. https://www.pexels.com/api/
2. Sign up → Get API key

### Pixabay (100 requests/minute)
1. https://pixabay.com/api/docs/
2. Sign up → Get API key

**Then tell me:** "Image API keys: [paste keys]"

---

## ✅ AFTER YOU PROVIDE ALL KEYS:

I will:
1. Create the `.env` file with ALL your keys
2. Help you add them to GitHub Secrets
3. Test the system

---

## 🚀 START HERE:

**Do STEP 1 (Groq API) first, then tell me your Groq key!**
