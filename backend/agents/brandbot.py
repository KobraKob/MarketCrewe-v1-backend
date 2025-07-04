# backend/agents/brandbot.py

class BrandBot:
    def __init__(self):
        pass

    def load_context(self, intake_file_path):
        import json

        with open(intake_file_path, "r") as f:
            intake_data = json.load(f)

        brand_context = {
            "brand_name": intake_data.get("brand_name"),
            "industry": intake_data.get("industry"),
            "tone": intake_data.get("brand_voice"),
            "audience": intake_data.get("audience"),
            "products": intake_data.get("products"),
            "goals": intake_data.get("goals")
        }

        print("✅ Brand context initialized.")
        return brand_context
