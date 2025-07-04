import os
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

load_dotenv(dotenv_path='../.env')

class PlatformSplitterBot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("SAMBA_API_KEY"),
            base_url=os.getenv("SAMBA_BASE_URL")
        )
        self.model = os.getenv("SAMBA_MODEL_NAME")

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def split_post_by_platform(self, post_text):
        prompt = f"""
You are a social media assistant.

Take the following post and reformat it for 4 platforms:
- Instagram: short, emoji-rich
- LinkedIn: professional, value-driven
- Twitter/X: punchy, max 280 chars
- Facebook: engaging, conversational

Original Post:
{post_text}

IMPORTANT: Do not include any of your own thinking, analysis, or notes in the output. Only provide the final, formatted posts.

Output format:
---
📸 Instagram:
...

💼 LinkedIn:
...

🐦 Twitter/X:
...

📘 Facebook:
...
---
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        return response.choices[0].message.content
