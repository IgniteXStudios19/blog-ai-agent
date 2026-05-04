# Blog AI Agent - Fully Automated News-to-Content System

[![GitHub Actions Status](https://github.com/yourusername/blog-ai-agent/workflows/Blog%20AI%20Agent%20Automation/badge.svg)](https://github.com/yourusername/blog-ai-agent/actions)

A **completely free, fully automated** AI agent that researches, writes, and publishes blog posts with audio and video - running entirely on GitHub Actions (no server needed!).

## 🎯 What This System Does

Every 6 hours, this AI agent automatically:

1. **🔍 Researches** - Fetches trending news from RSS feeds, Google News, Reddit, and free news APIs
2. **🧠 Analyzes** - Uses free AI models (Groq/Gemini) to identify the most important stories
3. **✍️ Writes** - Generates 800-1500 word SEO-optimized blog posts
4. **🎧 Creates Audio** - Converts blog posts to MP3 using Microsoft's free neural TTS (Edge-TTS)
5. **🎥 Creates Video** - Generates engaging videos with images, text overlays, and audio
6. **📢 Publishes** - Automatically posts to Hashnode, Telegram, Twitter, LinkedIn, Reddit, Discord, and Mastodon
7. **📊 Tracks** - Maintains a database to prevent duplicates and logs all activities

**All completely FREE with no credit card required!**

## 🏗️ Project Structure

```
blog-ai-agent/
├── .github/workflows/     # GitHub Actions automation (runs every 6 hours)
├── agents/                 # AI agents for each task
│   ├── news_researcher.py      # Fetches and analyzes news
│   ├── content_writer.py       # Generates blog posts with AI
│   ├── social_formatter.py     # Creates platform-specific posts
│   ├── audio_generator.py      # Creates MP3 audio from text
│   └── video_creator.py       # Creates MP4 videos
├── publishers/             # Publishing modules for each platform
│   ├── hashnode_publisher.py   # Posts to Hashnode blog
│   ├── telegram_publisher.py   # Posts to Telegram channel
│   ├── twitter_publisher.py    # Posts to Twitter/X
│   ├── linkedin_publisher.py   # Posts to LinkedIn
│   ├── reddit_publisher.py     # Posts to Reddit
│   ├── discord_publisher.py    # Posts to Discord
│   └── mastodon_publisher.py  # Posts to Mastodon
├── database/               # Database management
│   └── db_manager.py          # SQLite operations
├── utils/                  # Utility functions
│   ├── text_cleaner.py         # Cleans and formats text
│   ├── image_downloader.py     # Downloads free stock images
│   ├── music_manager.py        # Manages background music
│   └── logger.py              # Logging configuration
├── config/                 # Configuration files
│   ├── settings.py             # All settings and API keys
│   ├── news_sources.py        # RSS feeds and API configs
│   └── prompts.py             # AI prompt templates
├── assets/                 # Static assets
│   ├── music/                 # Background music files
│   ├── fonts/                 # Fonts for video text
│   └── templates/             # Video/image templates
├── output/                 # Generated content (temp)
│   ├── blogs/                 # Generated blog posts
│   ├── audio/                 # Generated MP3 files
│   └── videos/                # Generated MP4 files
├── tests/                  # Test files
├── main.py                 # Main orchestrator (runs everything)
├── requirements.txt        # Python dependencies
├── .env.example           # Template for API keys
└── README.md              # This file
```

## 🚀 Quick Start Guide

### Step 1: Prerequisites (5 minutes)

1. **Python 3.11+** - Download from [python.org](https://python.org) (Check "Add Python to PATH" during install)
2. **VS Code** - Download from [code.visualstudio.com](https://code.visualstudio.com)
3. **Git** - Download from [git-scm.com](https://git-scm.com)
4. **GitHub Account** - Sign up at [github.com](https://github.com) (free)

### Step 2: Get Free API Keys (30-60 minutes)

You need at least ONE AI API key and ONE blog platform key:

**Required (Minimum to run):**
- **Groq API** (Free 14,400 requests/day) - Get at [console.groq.com](https://console.groq.com)
- **Hashnode** (Free blog platform) - Get at [hashnode.com](https://hashnode.com)

**Optional (For more features):**
- Google Gemini API (Backup AI)
- Telegram Bot (Easiest social media)
- Twitter/X API (1500 tweets/month free)
- Reddit API (Free)
- Discord Webhook (Easiest to set up)
- Unsplash API (Free images)

See [Phase 2 in the full guide](link-to-guide) for detailed registration steps for each service.

### Step 3: Clone and Setup (5 minutes)

```bash
# Clone this repository
git clone https://github.com/yourusername/blog-ai-agent.git
cd blog-ai-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure API Keys (5 minutes)

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   GROQ_API_KEY=your_groq_key_here
   HASHNODE_API_KEY=your_hashnode_key_here
   HASHNODE_PUBLICATION_ID=your_publication_id_here
   # ... add other keys as needed
   ```

3. **NEVER commit `.env` to GitHub!** (It's in `.gitignore`)

### Step 5: Add Secrets to GitHub (5 minutes)

1. Go to your GitHub repository
2. Navigate to **Settings → Secrets and variables → Actions**
3. Add EACH variable from your `.env` file as a secret
4. Name them exactly as they appear in `.env` (e.g., `GROQ_API_KEY`)

### Step 6: Run the Automation! (1 minute)

1. Go to the **Actions** tab in your GitHub repository
2. Click on "Blog AI Agent Automation" workflow
3. Click "Run workflow" → "Run workflow" (to test manually)
4. Watch the logs in real-time!
5. The workflow will also run automatically every 6 hours

## 📊 Free Tier Limits

| Service | Free Limit | Our Usage |
|---------|------------|-----------|
| GitHub Actions | 2000 min/month (public repo) | ~1800 min/month |
| Groq AI | 14,400 requests/day | ~120 requests/month |
| Hashnode | Unlimited | Unlimited |
| Telegram | Unlimited | Unlimited |
| Twitter/X | 1500 tweets/month | ~120 posts/month |
| Discord | Unlimited | Unlimited |
| Mastodon | Unlimited | Unlimited |

**Total cost: $0.00/month** 🎉

## 🛠️ Local Testing

To test the system locally (without publishing):

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the agent
python main.py
```

Check the logs in `blog_agent.log` for details.

## 📝 Customization

Edit `config/settings.py` to change:
- `NICHE` - Your blog topic (technology, business, science, health, etc.)
- `POSTS_PER_RUN` - How many posts per 6-hour run (default: 3)
- `MIN_ARTICLE_WORDS` / `MAX_ARTICLE_WORDS` - Blog post length

## 🐛 Troubleshooting

**Problem: GitHub Actions fails with "Module not found"**
- Solution: Check `requirements.txt` has all dependencies, commit and push

**Problem: AI API errors**
- Solution: Verify API keys in GitHub Secrets (Settings → Secrets)

**Problem: Publishing fails**
- Solution: Check platform-specific API keys and permissions

**Problem: Database conflicts**
- Solution: The workflow automatically pulls latest changes before running

## 📚 Full Documentation

For the complete step-by-step guide (from absolute beginner to advanced), see the full documentation (link to be added).

## ⚠️ Important Notes

1. **Personal Data Safety** - This agent only handles news content and API calls. Your personal files are never accessed.
2. **Rate Limits** - Stay within free tier limits by adjusting `POSTS_PER_RUN`
3. **Content Quality** - AI-generated content should be reviewed periodically
4. **Legal Compliance** - Respect copyright, add sources, follow platform terms

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📜 License

MIT License - Feel free to use this project for any purpose!

## ⭐ Showcase

Want to see this in action? Check out these blogs running the agent:
- (Add your blog URL here after setup!)

---

**Built with ❤️ using 100% free tools and services**
