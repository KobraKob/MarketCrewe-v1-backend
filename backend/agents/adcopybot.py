# backend/agents/adcopybot.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path='../.env')

class AdCopyBot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("SAMBA_API_KEY"),
            base_url=os.getenv("SAMBA_BASE_URL")
        )
        self.model = os.getenv("SAMBA_MODEL_NAME")

    def generate_ads(self, context):
        prompt = f"""
You are a digital ad copywriter for a brand called {context['brand_name']} in the {context['industry']} industry.

Your job is to create short-form ad copy for 3–5 products:
{', '.join(context['products'])}

Target audience: {context['audience']}
Tone: {context['tone']}
Marketing goals: {', '.join(context['goals'])}

For each product, generate:
- 2 Ad Headlines (max 40 chars)
- 1 Short Ad Description (max 90 chars)
- 1 Call to Action (CTA)

IMPORTANT: Do not include any of your own thinking, analysis, or notes in the output. Only provide the final, formatted ad copy.

Output in clear Markdown sections.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content
