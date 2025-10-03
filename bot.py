from telethon import TelegramClient, events
import os

# Get credentials from environment variables
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
target_bot = os.environ.get('TARGET_BOT')  # The bot you want to search in

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(pattern=r'/search (.+)', outgoing=True))
async def search_handler(event):
    """Search for messages containing specific text/emoji"""
    search_term = event.pattern_match.group(1)
    
    await event.respond(f"🔍 Searching for '{search_term}'...")
    
    results = []
    count = 0
    
    # Search through messages
    async for msg in client.iter_messages(target_bot, limit=5000):
        if msg.text and search_term in msg.text:
            results.append(msg)
            count += 1
            if count >= 10:  # Limit to 10 results
                break
    
    if results:
        await event.respond(f"✅ Found {len(results)} messages:")
        for msg in results:
            date_str = msg.date.strftime('%Y-%m-%d %H:%M')
            text_preview = msg.text[:100] + "..." if len(msg.text) > 100 else msg.text
            await event.respond(f"📅 {date_str}\n{text_preview}\n")
    else:
        await event.respond(f"❌ No messages found with '{search_term}'")

@client.on(events.NewMessage(pattern='/help', outgoing=True))
async def help_handler(event):
    """Show help message"""
    help_text = """
🤖 **Search Bot Commands**

/search <text> - Search for messages containing text or emoji
/help - Show this help message

**Examples:**
/search 🎉
/search hello
/search payment
    """
    await event.respond(help_text)

async def main():
    await client.start()
    print("Bot is running! Send yourself /help to see commands")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())