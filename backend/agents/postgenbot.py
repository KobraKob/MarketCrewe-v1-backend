# backend/agents/postgenbot.py

import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

load_dotenv(dotenv_path='../.env')

class PostGenBot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("SAMBA_API_KEY"),
            base_url=os.getenv("SAMBA_BASE_URL")
        )
        self.model = os.getenv("SAMBA_MODEL_NAME")

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generate_weekly_posts(self, context):
        prompt = f"""
You are a marketing assistant for {context['brand_name']} in the {context['industry']} space.
Tone: {context['tone']}.
Audience: {context['audience']}.
Goals: {', '.join(context['goals'])}.

Create a 7-day content calendar. Each post should:
- Focus on 1 of the products: {', '.join(context.get('products', []))}
- Be value-driven (education, story, or benefits)

IMPORTANT: Do not include any of your own thinking, analysis, or notes in the output. Only provide the final, formatted content calendar.

Output in this format:

### **Dr. Squatch: 7-Day Content Calendar**

---

#### **Day 1: [Product]**
*   **Title:** [Title]
*   **Post:** [Post]

---

#### **Day 2: [Product]**
*   **Title:** [Title]
*   **Post:** [Post]

---
(and so on for 7 days)
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        raw_output = response.choices[0].message.content
        
        # Clean the output
        cleaned_output = self.clean_output(raw_output)
        return cleaned_output
    
    def clean_output(self, text):
        """Remove internal thinking markers and ensure proper formatting"""
        # Remove lines with thinking markers
        text = re.sub(r'^``.*$', '', text, flags=re.MULTILINE)
        
        # Ensure consistent formatting
        text = re.sub(r'^---\s*$', '---', text, flags=re.MULTILINE)
        
        # Remove any empty lines at start/end
        return text.strip()
