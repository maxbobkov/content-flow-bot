import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import uuid

from config import BOT_TOKEN, CHANNEL_ID, ADMIN_IDS, PHOTOS_DIR, DB_PATH
from database import Database

# Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot and database initialization
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database(DB_PATH)

def is_admin(user_id: int):
    return user_id in ADMIN_IDS

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if not is_admin(message.from_user.id):
        return await message.answer("Sorry, you don't have access to the bot.")
    
    await message.answer("Hi! I'm a bot for posting photos. "
                        "Send me a photo (with or without a caption), "
                        "and I'll save it for later posting in the channel.")

@dp.message(lambda message: message.photo)
async def handle_photo(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    
    # Get the largest version of the photo
    photo = message.photo[-1]
    
    # Generate a unique file name
    file_name = f"{uuid.uuid4()}.jpg"
    file_path = PHOTOS_DIR / file_name
    
    # Download and save the photo
    await bot.download(
        photo,
        destination=file_path
    )
    
    # Save the information to the database
    db.add_photo(
        file_path=str(file_path),
        caption=message.caption
    )
    
    await message.answer("The photo has been saved")

async def post_random_photo():
    # Get a random unpublished photo
    photo = db.get_random_unposted_photo()
    
    if not photo:
        # Notifying the admins that we're out of photos.
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    admin_id,
                    "⚠️ Warning. All photos have been published. "
                    "Please add new photos."
                )
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id}: {e}")
        return
    
    photo_id, file_path, caption = photo
    
    try:
        # Send a photo to the channel
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=types.FSInputFile(file_path),
            caption=caption
        )
        
        # Mark the photo as published
        db.mark_as_posted(photo_id)
        logger.info(f"Successfully posted photo {photo_id}")
        
    except Exception as e:
        logger.error(f"Failed to post photo {photo_id}: {e}")

async def main():
    # Setting up the scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        post_random_photo,
        trigger='cron',
        hour='9,21'  # Publication at 9:00 and 21:00 UTC
    )
    scheduler.start()
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())