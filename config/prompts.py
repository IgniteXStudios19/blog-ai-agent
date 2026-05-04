"""
AI Prompt Templates - All prompts for content generation, SEO, and social media
These prompts are optimized for free LLMs like Groq (Llama 3) and Gemini
"""

class PromptTemplates:
    """Collection of prompt templates for various AI tasks"""
    
    # ========== NEWS ANALYSIS PROMPTS ==========
    
    RESEARCH_ANALYSIS = """You are an expert news analyst. Analyze the following news article and extract key information.

Article Title: {title}
Article Text: {text}
Source: {source}
Published: {published}

Extract and return a JSON object with the following fields:
- main_topic: The primary topic/subject of the article
- key_points: List of 5-7 key points from the article
- target_audience: Who would be most interested in this article
- trending_score: Rate trending potential 1-10 (10 = extremely trending)
- seo_keywords: List of 5-8 SEO keywords related to this topic
- summary: A 2-3 sentence summary of the article
- why_important: Why this news matters to readers

Return ONLY the JSON object, no other text."""

    # ========== BLOG WRITING PROMPTS ==========
    
    BLOG_OUTLINE = """You are an expert blog writer. Create a detailed outline for a blog post based on the following news analysis.

News Summary: {summary}
Key Points: {key_points}
Target Audience: {target_audience}
SEO Keywords: {seo_keywords}
Word Count Target: {min_words}-{max_words} words

Create a blog post outline with:
1. Catchy, SEO-optimized title (include 1-2 keywords)
2. Introduction (hook readers, state why this matters)
3. 4-6 main sections with subheadings (include keywords naturally)
4. Conclusion (summarize, call to action)

Return the outline in a clear, structured format."""

    BLOG_WRITING = """You are an expert blog writer specializing in {niche} content. Write a high-quality, SEO-optimized blog post following this outline.

Outline: {outline}
News Details: {news_details}
SEO Keywords: {seo_keywords}
Word Count: {min_words}-{max_words} words
Language: {language}

Requirements:
- Write in a natural, human-like tone (avoid AI clichés like "delve into", "in today's digital age")
- Use short paragraphs (2-3 sentences each)
- Include relevant examples or analogies
- Naturally integrate SEO keywords (don't stuff)
- Use proper heading hierarchy (H1 for title, H2 for sections, H3 for subsections)
- Include a meta description (150-160 characters) at the top
- Add a "Key Takeaways" section at the end
- Format in clean Markdown

Write the complete blog post now."""

    HUMANIZE_CONTENT = """You are an editor improving AI-generated content. Make this blog post sound more human and engaging.

Original Text: {text}

Improvements needed:
- Replace robotic phrases with natural language
- Add personal touches or relatable examples
- Vary sentence structure (mix short and long sentences)
- Add rhetorical questions to engage readers
- Ensure smooth transitions between paragraphs
- Keep all facts accurate, just improve the style

Return the improved text in Markdown format."""

    # ========== SEO OPTIMIZATION PROMPTS ==========
    
    SEO_METADATA = """Generate SEO metadata for this blog post.

Blog Title: {title}
Blog Content Summary: {summary}
Target Keywords: {keywords}

Return a JSON object with:
- meta_title: SEO title (60 characters max, include main keyword)
- meta_description: Meta description (150-160 characters, compelling, include keyword)
- slug: URL-friendly slug (lowercase, hyphens, include keyword, 3-5 words)
- tags: List of 5-7 relevant tags
- canonical_url: (leave empty, will be filled by publisher)

Return ONLY the JSON object."""

    # ========== SOCIAL MEDIA PROMPTS ==========
    
    TWITTER_POST = """Create a Twitter/X post to promote this blog article.

Blog Title: {title}
Blog Summary: {summary}
URL: {url}
Keywords: {keywords}

Requirements:
- Max 280 characters
- Include 2-3 relevant hashtags
- Compelling hook to make people click
- Use emojis sparingly (1-2 max)
- Include the URL at the end

Write the tweet now."""

    LINKEDIN_POST = """Create a LinkedIn post to promote this blog article.

Blog Title: {title}
Blog Summary: {summary}
Key Points: {key_points}
URL: {url}

Requirements:
- Professional, insightful tone
- 1000-1500 characters
- Start with a hook question or statement
- Share 2-3 key insights from the article
- Include a call to action (read more)
- Add 3-5 relevant hashtags
- Mention the blog name/URL

Write the LinkedIn post now."""

    REDDIT_POST = """Create a Reddit post to share this article in relevant subreddits.

Blog Title: {title}
Blog Summary: {summary}
Key Points: {key_points}
URL: {url}
Subreddit: {subreddit}

Requirements:
- Title: Catchy, matches subreddit culture (r/technology vs r/news have different styles)
- Body: 300-500 characters explaining why this is worth reading
- Don't be spammy - provide value first
- Include the URL at the end
- Add a question to encourage comments

Write the Reddit post (title and body) now."""

    TELEGRAM_POST = """Create a Telegram channel post to share this article.

Blog Title: {title}
Blog Summary: {summary}
URL: {url}

Requirements:
- Use HTML formatting (<b>bold</b>, <i>italic</i>, <a href="">links</a>)
- 200-400 characters
- Exciting, brief summary
- Include the link
- Use 1-2 emojis

Write the Telegram post now."""

    DISCORD_EMBED = """Create a Discord embed message to share this article.

Blog Title: {title}
Blog Summary: {summary}
URL: {url}
Image URL: {image_url}

Return a JSON object for Discord webhook embed:
- title: Blog title
- description: 200-300 character summary
- url: Blog URL
- color: Hex color code (use 0x1DA1F2 for blue or 0x5865F2 for Discord purple)
- thumbnail: {{"url": "{image_url}"}}
- footer: {{"text": "Blog AI Agent | {niche} News"}}

Return ONLY the JSON object."""

    MASTODON_POST = """Create a Mastodon post to share this article.

Blog Title: {title}
Blog Summary: {summary}
URL: {url}
Keywords: {keywords}

Requirements:
- Max 500 characters
- Include 2-3 hashtags (Mastodon uses hashtags differently than Twitter)
- Friendly, community-oriented tone
- Include the URL

Write the Mastodon post now."""

    # ========== CONTENT QUALITY PROMPTS ==========
    
    QUALITY_CHECK = """You are a content quality checker. Evaluate this blog post.

Blog Post: {text}
Target Word Count: {min}-{max} words

Check for:
1. Word count (is it within range?)
2. Readability (grade 8-10 level)
3. SEO optimization (keywords present naturally)
4. Factual accuracy (based on provided source)
5. Engagement (does it hook the reader?)

Return a JSON object:
- word_count: Actual word count
- readability_score: 1-10 (10 = very readable)
- seo_score: 1-10 (10 = well optimized)
- quality_score: 1-10 (10 = excellent)
- issues: List of any issues found
- passed: true/false (true if all checks pass)

Return ONLY the JSON object."""

    # ========== UTILITY METHODS ==========
    
    @classmethod
    def format_prompt(cls, template_name, **kwargs):
        """Format a prompt template with provided variables"""
        template = getattr(cls, template_name, None)
        if not template:
            raise ValueError(f"Prompt template '{template_name}' not found")
        return template.format(**kwargs)
