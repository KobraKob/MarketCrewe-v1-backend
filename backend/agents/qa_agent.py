# backend/agents/qa_agent.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path='../.env')

class QAAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("SAMBA_API_KEY"),
            base_url=os.getenv("SAMBA_BASE_URL")
        )
        self.model = os.getenv("SAMBA_MODEL_NAME")

    def edit_output(self, raw_text, tone):
        prompt = f"""
You're an editorial assistant.

Your job is to improve the following content:
- Fix grammar and structure
- Make sure it uses a consistent tone: {tone}
- Keep formatting (markdown) intact
- Do NOT add new ideas

IMPORTANT: Do not include any of your own thinking, analysis, or notes in the output. Only provide the final, edited content.

Here is the content:
---
{raw_text}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content
