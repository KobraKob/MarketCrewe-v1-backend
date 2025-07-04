# backend/agents/designbriefbot.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path='../.env')

class DesignBriefBot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("SAMBA_API_KEY"),
            base_url=os.getenv("SAMBA_BASE_URL")
        )
        self.model = os.getenv("SAMBA_MODEL_NAME")

    def generate_visual_prompts(self, context):
        prompt = f"""
You are a creative director for {context['brand_name']}.

Based on the brand tone "{context['tone']}", and products: {', '.join(context['products'])},
generate visually descriptive prompts for social media creatives.

Make prompts usable in tools like Canva, Midjourney, or Sora.
Create 1 image concept per product.

IMPORTANT: Do not include any of your own thinking, analysis, or notes in the output. Only provide the final, formatted visual prompts.

Format:
- Product Name
- Visual Description Prompt (for AI generation)
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )

        return response.choices[0].message.content
