import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path='../.env')

class HashtagBot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("SAMBA_API_KEY"),
            base_url=os.getenv("SAMBA_BASE_URL")
        )
        self.model = os.getenv("SAMBA_MODEL_NAME")

    def generate_hashtags(self, context, post_text):
        prompt = f"""
You're a social media strategist.

Generate up to 10 relevant, non-generic hashtags for the following Instagram post.

Tone: {context['tone']}
Audience: {context['audience']}
Post:
{post_text}

IMPORTANT: Do not include any of your own thinking, analysis, or notes in the output. Only provide the final, formatted hashtags.

Output format:
#hashtag1 #hashtag2 #hashtag3 ...
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
