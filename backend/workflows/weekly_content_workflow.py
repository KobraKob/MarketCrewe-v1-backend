from agents.postgenbot import PostGenBot
from agents.adcopybot import AdCopyBot
from agents.designbriefbot import DesignBriefBot
from agents.qa_agent import QAAgent
from agents.hashtagbot import HashtagBot
from agents.platformsplitter import PlatformSplitterBot
from agents.whatsappcopybot import WhatsAppCopyBot
import os
import time

def run_weekly_content_plan(context):
    print("\n🧠 Running PostGenBot...")
    postgen = PostGenBot()
    posts = postgen.generate_weekly_posts(context)
    with open("delivery/weekly_posts.md", "w", encoding="utf-8") as f:
        f.write(posts)
    print("✅ Weekly posts saved.")
    time.sleep(20)

    print("\n🛠️ Running QA Agent...")
    qa = QAAgent()
    cleaned_posts = qa.edit_output(posts, context['tone'])
    with open("delivery/weekly_posts_cleaned.md", "w", encoding="utf-8") as f:
        f.write(cleaned_posts)
    print("✅ Cleaned posts saved.")
    time.sleep(20)

    print("\n💬 Running AdCopyBot...")
    adbot = AdCopyBot()
    ads = adbot.generate_ads(context)
    with open("delivery/ad_copies.md", "w", encoding="utf-8") as f:
        f.write(ads)
    print("✅ Ad copies saved.")
    time.sleep(20)

    print("\n🎨 Running DesignBriefBot...")
    designbot = DesignBriefBot()
    visuals = designbot.generate_visual_prompts(context)
    with open("delivery/visual_briefs.md", "w", encoding="utf-8") as f:
        f.write(visuals)
    print("✅ Visual prompts saved.")
    time.sleep(20)

    print("\n🏷 Running HashtagBot...")
    hashtagbot = HashtagBot()
    hashtag_output = hashtagbot.generate_hashtags(context, cleaned_posts)
    with open("delivery/hashtags.md", "w", encoding="utf-8") as f:
        f.write(hashtag_output)
    print("✅ Hashtags saved.")
    time.sleep(20)

    print("\n📣 Running PlatformSplitterBot...")
    platformbot = PlatformSplitterBot()
    platform_output = platformbot.split_post_by_platform(cleaned_posts)
    with open("delivery/platform_split.md", "w", encoding="utf-8") as f:
        f.write(platform_output)
    print("✅ Platform-specific posts saved.")
    time.sleep(20)

    print("\n📲 Running WhatsAppCopyBot...")
    whatsappbot = WhatsAppCopyBot()
    whatsapp_output = whatsappbot.generate_whatsapp_broadcast(context)
    with open("delivery/whatsapp_broadcast.md", "w", encoding="utf-8") as f:
        f.write(whatsapp_output)
    print("✅ WhatsApp broadcast messages saved.")

    print("\n🚀 All content successfully generated and saved in /delivery.")

    return {
        "weekly_posts": posts,
        "cleaned_posts": cleaned_posts,
        "ad_copies": ads,
        "visual_briefs": visuals,
        "hashtags": hashtag_output,
        "platform_split": platform_output,
        "whatsapp_broadcast": whatsapp_output
    }
