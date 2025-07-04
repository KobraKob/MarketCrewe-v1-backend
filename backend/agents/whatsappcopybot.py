import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path='../.env')

class WhatsAppCopyBot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("SAMBA_API_KEY"),
            base_url=os.getenv("SAMBA_BASE_URL")
        )
        self.model = os.getenv("SAMBA_MODEL_NAME")

    def generate_whatsapp_broadcast(self, context):
        prompt = f"""
You're a marketing assistant for {context['brand_name']}.

Create 2 WhatsApp broadcast message options promoting this week's content or products:
- Text only
- Max 2–3 lines
- Friendly, urgency-driven, and include a CTA

Audience: {context['audience']}
Goals: {', '.join(context['goals'])}
Products: {', '.join(context['products'])}
Tone: {context['tone']}

IMPORTANT: Do not include any of your own thinking, analysis, or notes in the output. Only provide the final, formatted WhatsApp messages.

Output:
1. ...
2. ...
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        return response.choices[0].message.content
