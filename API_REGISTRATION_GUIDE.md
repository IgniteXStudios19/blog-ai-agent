# API Registration Guide - Get All Free API Keys

This guide walks you through registering for EVERY free API needed for the Blog AI Agent. **All services are 100% FREE with no credit card required.**

## Table of Contents
1. [AI APIs](#ai-apis)
   - [Groq API (Primary)](#groq-api-primary)
   - [Google Gemini API (Backup)](#google-gemini-api-backup)
   - [HuggingFace Token](#huggingface-token)
2. [News APIs](#news-apis)
   - [The Guardian API](#the-guardian-api)
   - [GNews API](#gnews-api)
   - [NewsAPI.org](#newsapi-org)
3. [Image APIs](#image-apis)
   - [Unsplash API](#unsplash-api)
   - [Pexels API](#pexels-api)
   - [Pixabay API](#pixabay-api)
4. [Blog Platform](#blog-platform)
   - [Hashnode](#hashnode)
5. [Social Media Platforms](#social-media-platforms)
   - [Telegram Bot](#telegram-bot)
   - [Twitter/X Developer](#twitter-x-developer)
   - [LinkedIn](#linkedin)
   - [Reddit](#reddit)
   - [Discord Webhook](#discord-webhook)
   - [Mastodon](#mastodon)

---

## AI APIs

### Groq API (Primary AI)
**Why:** Fastest free LLM API - 14,400 requests/day, 6000 tokens/minute

**Steps:**
1. Go to [console.groq.com](https://console.groq.com)
2. Click **"Sign up"** (or **"Log in"** if you have an account)
3. You can sign up with:
   - Google account
   - GitHub account
   - Email (enter email, check inbox for verification)
4. After logging in, click **"API Keys"** in the left sidebar
5. Click **"Create API Key"** button
6. Name it: `blog-ai-agent`
7. **COPY THE API KEY IMMEDIATELY** - it starts with `gsk_`
   - ⚠️ **WARNING:** You won't be able to see it again! If you lose it, delete and create a new one.
8. Paste into your `.env` file:
   ```
   GROQ_API_KEY=gsk_your_key_here
   ```

**Free Limits:**
- 14,400 requests/day
- 6000 tokens/minute
- Models: Llama 3.1 70B, Mixtral 8x7B (all free)

**Test your key:**
```bash
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_GROQ_KEY" \
  -d '{"model": "llama3-70b-8192", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

### Google Gemini API (Backup AI)
**Why:** Backup AI - 15 RPM, 1 million tokens/day free

**Steps:**
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **"Get API key"** in the left sidebar (or **"Sign in"** first)
3. Sign in with your Google account
4. Click **"Create API key"**
5. Select **"Create new project"** (name it `blog-ai-agent`)
6. Click **"Create API key in new project"**
7. **COPY THE API KEY** - it looks like: `AIzaSy...`
8. Paste into your `.env` file:
   ```
   GEMINI_API_KEY=AIzaSy_your_key_here
   ```

**Free Limits:**
- Gemini 1.5 Flash: 15 requests/minute, 1 million tokens/day
- Gemini 1.5 Pro: 2 requests/minute, 1 million tokens/day

**Test your key:**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_GEMINI_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text": "Hello"}]}]}'
```

---

### HuggingFace Token
**Why:** Access to free inference API and models

**Steps:**
1. Go to [huggingface.co](https://huggingface.co)
2. Click **"Sign up"** (top right)
3. Fill in:
   - Username
   - Email
   - Password
4. Verify your email
5. After logging in, click your **profile picture** (top right) → **"Settings"**
6. Click **"Access Tokens"** in the left sidebar
7. Click **"New token"** button
8. Name: `blog-ai-agent`
9. Role: **"read"** (sufficient for free inference)
10. Click **"Generate a token"**
11. **COPY THE TOKEN** - it starts with `hf_`
12. Paste into your `.env` file:
    ```
    HUGGINGFACE_TOKEN=hf_your_token_here
    ```

**Free Limits:**
- Inference API: Rate limited but generous for personal use
- No credit card required

---

## News APIs

### The Guardian API
**Why:** Completely FREE, UNLIMITED requests for developers

**Steps:**
1. Go to [open-platform.theguardian.com](https://open-platform.theguardian.com)
2. Click **"Sign up"** (top right)
3. Fill in:
   - Email
   - Password
   - Name
4. Verify your email
5. Log in to the dashboard
6. You'll see your **API Key** on the dashboard
   - It looks like: `abc12345-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
7. Paste into your `.env` file:
   ```
   GUARDIAN_API_KEY=your_guardian_key_here
   ```

**Free Limits:** UNLIMITED for developers!

**Test your key:**
```bash
curl "https://content.guardianapis.com/search?api-key=YOUR_GUARDIAN_KEY&page-size=1"
```

---

### GNews API
**Why:** 100 requests/day free

**Steps:**
1. Go to [gnews.io](https://gnews.io)
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with:
   - Google account (easiest)
   - GitHub account
   - Email
4. After logging in, go to **"Dashboard"**
5. You'll see your **API Key**
6. Paste into your `.env` file:
   ```
   GNEWS_API_KEY=your_gnews_key_here
   ```

**Free Limits:** 100 requests/day

---

### NewsAPI.org
**Why:** 100 requests/day free (developer plan)

**Steps:**
1. Go to [newsapi.org](https://newsapi.org)
2. Click **"Get API Key"**
3. Sign up with:
   - Google account
   - Email
4. After signing up, you'll see your **API Key** immediately
5. Paste into your `.env` file:
   ```
   NEWSAPI_KEY=your_newsapi_key_here
   ```

**Free Limits:** 100 requests/day (developer plan, never expires)

---

## Image APIs

### Unsplash API
**Why:** 50 requests/hour free, beautiful high-quality photos

**Steps:**
1. Go to [unsplash.com/developers](https://unsplash.com/developers)
2. Click **"Register as a developer"**
3. Sign up or log in
4. Click **"New Application"**
5. Accept the Terms of Service
6. Fill in:
   - Application name: `Blog AI Agent`
   - Description: `Automated blog content generation system`
7. Click **"Create application"**
8. You'll see your **Access Key** (not the Secret Key)
9. Paste into your `.env` file:
   ```
   UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here
   ```

**Free Limits:** 50 requests/hour

---

### Pexels API
**Why:** 200 requests/hour free, high-quality stock photos

**Steps:**
1. Go to [www.pexels.com/api/](https://www.pexels.com/api/)
2. Click **"Register"** (or log in)
3. After logging in, you'll see your **API Key**
4. Paste into your `.env` file:
   ```
   PEXELS_API_KEY=your_pexels_key_here
   ```

**Free Limits:** 200 requests/hour

---

### Pixabay API
**Why:** 100 requests/minute free, unlimited for practical purposes

**Steps:**
1. Go to [pixabay.com/api/docs/](https://pixabay.com/api/docs/)
2. Sign up or log in to Pixabay
3. After logging in, go to your **profile** → **"Edit profile"**
4. Scroll down to **"Search API"** section
5. You'll see your **API Key**
6. Paste into your `.env` file:
   ```
   PIXABAY_API_KEY=your_pixabay_key_here
   ```

**Free Limits:** 100 requests/minute (effectively unlimited)

---

## Blog Platform

### Hashnode
**Why:** Free blog platform, excellent API, custom domain support, SEO-friendly

**Steps:**
1. Go to [hashnode.com](https://hashnode.com)
2. Click **"Get Started"**
3. Sign up with:
   - Google account
   - GitHub account
   - Email
4. Create your blog:
   - Blog name: `Your Blog Name`
   - Subdomain: `yourname.hashnode.dev` (or connect custom domain later)
5. After creating, go to **Dashboard** → **"Settings"** → **"API"**
6. Click **"Generate API Key"**
7. **COPY THE API KEY**
8. Paste into your `.env` file:
   ```
   HASHNODE_API_KEY=your_hashnode_key_here
   ```
9. Also get your **Publication ID**:
   - Go to **Dashboard** → **"Settings"** → **"General"**
   - Look for **"Publication ID"** (looks like: `1234567890abcdef`)
   - Paste into your `.env` file:
     ```
     HASHNODE_PUBLICATION_ID=your_publication_id_here
     ```

**Free Limits:** Unlimited posts, unlimited API calls for personal use

---

## Social Media Platforms

### Telegram Bot
**Why:** EASIEST to set up, NO rate limits, completely free, unlimited posts

**Steps:**
1. Open **Telegram app** on your phone or desktop
2. Search for **@BotFather** (official bot)
3. Start a chat with BotFather
4. Send command: `/newbot`
5. Follow the prompts:
   - Enter your bot **display name**: `Blog AI Agent`
   - Enter your bot **username** (must end in `bot`): `blog_agente_bot`
6. BotFather will give you a **Bot Token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
7. **SAVE THIS TOKEN** - you'll need it!
8. Paste into your `.env` file:
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

**Create a Telegram Channel:**
1. In Telegram, click **"New Channel"** (or **"New Group"**)
2. Name it: `Your Blog Updates`
3. Set to **"Public Channel"** (so the bot can post)
4. After creating, add your bot as **Administrator**:
   - Go to Channel → **"Manage Channel"** → **"Administrators"** → **"Add Admin"**
   - Search for your bot (`@blog_agente_bot`)
   - Give it **"Post Messages"** permission
5. Get your **Channel ID**:
   - Go to Channel → **"Manage Channel"** → **"Channel Info"**
   - Look for **"Channel ID"** (starts with `-100...`)
   - OR forward a message from your channel to **@userinfobot** to get the ID
6. Paste into your `.env` file:
   ```
   TELEGRAM_CHANNEL_ID=-1001234567890
   ```

**Free Limits:** UNLIMITED posts, no rate limits!

---

### Twitter/X Developer
**Why:** 1500 tweets/month free (basic tier)

**Steps:**
1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Click **"Sign up"** (or log in with your Twitter account)
3. Apply for a developer account:
   - Click **"Apply"** or **"Create an app"**
   - Fill in the form:
     - **Use case:** `Automated news aggregation bot that reads public news and posts summaries. Content is AI-generated news commentary for public information purposes.`
     - **Use case details:** `I am building an automated blog system that researches trending news, generates blog posts using AI, and automatically posts summaries to social media platforms.`
   - Submit for review (usually approved instantly)
4. After approval, go to **"Projects & Apps"** → **"Create App"**
5. Fill in:
   - App name: `blog-ai-agent`
   - App description: `Automated blog content publishing system`
6. You'll get **API Key** and **API Secret Key**
7. Generate **Access Token** and **Access Token Secret**:
   - Go to your App → **"Keys and tokens"**
   - Click **"Generate"** under "Access Token and Secret"
8. Paste ALL FOUR keys into your `.env` file:
   ```
   TWITTER_API_KEY=your_api_key_here
   TWITTER_API_SECRET=your_api_secret_here
   TWITTER_ACCESS_TOKEN=your_access_token_here
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
   ```

**Free Limits:** 1500 tweets/month (read/write access)

---

### LinkedIn
**Why:** Free personal API access

**Steps:**
1. Go to [www.linkedin.com/developers/](https://www.linkedin.com/developers/)
2. Click **"Create app"**
3. Fill in:
   - App name: `Blog AI Agent`
   - LinkedIn Page: (select your personal profile)
   - App logo: (upload any image)
   - Legal agreement: Check the box
4. After creating, go to **"Auth"** tab
5. You'll see your **Client ID** and **Client Secret** (but we need an access token)
6. Go to **"Products"** tab → Request **"Share on LinkedIn"** product
7. After approval, generate an **Access Token**:
   - Use OAuth 2.0 flow (or use a tool like [OAuth Playground](https://www.linkedin.com/oauth/v2/))
   - The token looks like: `AQV...`
8. Paste into your `.env` file:
   ```
   LINKEDIN_ACCESS_TOKEN=AQV_your_token_here
   ```

**Note:** LinkedIn access tokens expire. You may need to refresh periodically.

---

### Reddit
**Why:** Free API, good for sharing to relevant communities

**Steps:**
1. Log in to [reddit.com](https://reddit.com)
2. Go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
3. Click **"create another app..."** (at the bottom)
4. Fill in:
   - **name:** `blog-ai-agent`
   - Select **"script"** (not web app or installed app)
   - **description:** `Automated blog posting system`
   - **about url:** (leave blank)
   - **redirect uri:** `http://localhost:8080`
5. Click **"create app"**
6. You'll see:
   - **CLIENT ID** (under the app name, in light grey text)
   - **CLIENT SECRET** (labeled "secret")
7. Paste into your `.env` file:
   ```
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_client_secret_here
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   ```

**Free Limits:** Generous rate limits for personal scripts

---

### Discord Webhook
**Why:** EASIEST to set up - just need a webhook URL, no API keys!

**Steps:**
1. Open **Discord** app
2. Create a server (or use an existing one):
   - Click **"+"** (left sidebar) → **"Create My Own"**
   - Name it: `Blog Updates`
3. Go to your server → **Channel** (where you want posts) → **"Edit Channel"** (gear icon)
4. Go to **"Integrations"** → **"Webhooks"** → **"New Webhook"**
5. Name it: `Blog AI Agent`
6. Click **"Copy Webhook URL"**
   - It looks like: `https://discord.com/api/webhooks/123456789/abc123...`
7. Paste into your `.env` file:
   ```
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url_here
   ```

**Free Limits:** UNLIMITED posts, no rate limits!

---

### Mastodon
**Why:** Completely free, open-source, no approval needed, unlimited posts

**Steps:**
1. Go to [mastodon.social](https://mastodon.social) (or any Mastodon instance)
2. Click **"Create account"**
3. Fill in:
   - Email
   - Username
   - Password
4. Verify your email
5. After logging in, go to **Settings** → **"Development"** (left sidebar)
6. Click **"New Application"**
7. Fill in:
   - Application name: `Blog AI Agent`
   - Application website: (leave blank or put your blog URL)
   - Scopes: Check **"write"** (to post) and **"read"** (to verify)
8. Click **"Submit"**
9. You'll see your **Access Token**
10. Paste into your `.env` file:
    ```
    MASTODON_ACCESS_TOKEN=your_mastodon_access_token_here
    MASTODON_API_BASE_URL=https://mastodon.social
    ```

**Free Limits:** UNLIMITED posts!

---

## Quick Reference: All API Keys in `.env`

After registering for all services, your `.env` file should look like:

```bash
# AI API KEYS
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxx
HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxx

# NEWS APIS
GUARDIAN_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
GNEWS_API_KEY=xxxxxxxxxxxxxxxx
NEWSAPI_KEY=xxxxxxxxxxxxxxxx

# IMAGE APIS
UNSPLASH_ACCESS_KEY=xxxxxxxxxxxxxxxx
PEXELS_API_KEY=xxxxxxxxxxxxxxxx
PIXABAY_API_KEY=xxxxxxxxxxxxxxxx

# BLOG PLATFORMS
HASHNODE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
HASHNODE_PUBLICATION_ID=xxxxxxxxxxxxxxxx

# SOCIAL MEDIA
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHANNEL_ID=-1001234567890

TWITTER_API_KEY=xxxxxxxxxxxxxxxx
TWITTER_API_SECRET=xxxxxxxxxxxxxxxx
TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxxxxx
TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxxxxxxxxxx

LINKEDIN_ACCESS_TOKEN=AQVxxxxxxxxxxxx

REDDIT_CLIENT_ID=xxxxxxxxxxxx
REDDIT_CLIENT_SECRET=xxxxxxxxxxxxxxxx
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password

DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxxxxxx/xxxxxxxx

MASTODON_ACCESS_TOKEN=xxxxxxxxxxxxxxxx
MASTODON_API_BASE_URL=https://mastodon.social

# SETTINGS
NICHE=technology
POSTS_PER_RUN=3
BLOG_LANGUAGE=english
MIN_ARTICLE_WORDS=800
MAX_ARTICLE_WORDS=1500
```

---

## Next Steps

After getting all API keys:
1. **Add them to GitHub Secrets** (see Phase 3)
2. **Test locally** with `python main.py`
3. **Push to GitHub** and let the automation run!

**Remember:** Never commit `.env` to GitHub! It's in `.gitignore` for safety.
