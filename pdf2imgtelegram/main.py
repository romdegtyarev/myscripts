import os
import logging
import sys
import asyncio
import asyncpg
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from pdf2image import convert_from_path
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_ADMIN_ID = int(os.getenv("TG_ADMIN_ID"))
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    encoding='utf-8'
)
logger = logging.getLogger("pdf_bot")
bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()
router = Router()

db_pool = None
user_temp_files = {}


async def init_db():
    """DB init"""
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY
            )
            """
        )
    logger.info("init_db: Done")

async def is_registered(user_id: int) -> bool:
    """"""
    async with db_pool.acquire() as conn:
        result = await conn.fetchval("SELECT user_id FROM users WHERE user_id = $1", user_id)
    return result is not None

@dp.message(Command("add_user"))
async def add_user(message: types.Message):
    """"""
    if message.from_user.id != TG_ADMIN_ID:
        return

    try:
        user_id = int(message.text.split()[1])
        logger.info(f"add_user: Try to add user: {user_id}")
        async with db_pool.acquire() as conn:
            await conn.execute("INSERT INTO users (user_id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)
    except (IndexError, ValueError):
        pass
    except Exception as e:
        logger.error(f"add_user Error: {e}")

@router.message(lambda message: message.document and message.document.mime_type == "application/pdf")
async def handle_pdf(message: types.Message):
    """"""
    user_id = message.from_user.id
    if not await is_registered(user_id):
        return

    document = message.document
    user_dir = f"/tmp/{user_id}"
    file_path = os.path.join(user_dir, f"{user_id}.pdf")

    try:
        os.makedirs(user_dir, exist_ok=True)
        await bot.download(document, destination=file_path)
        user_temp_files[user_id] = file_path
        logger.info(f"handle_pdf: Download file: {file_path} from user: {user_id}")
    except Exception as e:
        logger.error(f"handle_pdf: Error: {e}")

@dp.message(Command("convert"))
async def convert_page(message: types.Message):
    """"""
    user_id = message.from_user.id
    if user_id not in user_temp_files:
        return

    try:
        page_number = int(message.text.split()[1]) - 1
    except (IndexError, ValueError):
        return

    file_path = user_temp_files[user_id]
    logger.info(f"convert_page: Сonvert page: {page_number} in file: {file_path} for user: {user_id}")
    try:
        images = convert_from_path(file_path, dpi=150)
        if 0 <= page_number < len(images):
            img = images[page_number]
            img_buffer = BytesIO()
            img.save(img_buffer, format="JPEG", quality=80)
            img_bytes = img_buffer.getvalue()
            if len(img_bytes) <= 10 * 1024 * 1024:
                await message.reply_photo(BufferedInputFile(img_bytes, filename="converted.jpg"))
            else:
                await message.reply_document(BufferedInputFile(img_bytes, filename="converted.jpg"))
    except Exception as e:
        logger.error(f"convert_page: Error: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        user_temp_files.pop(user_id, None)

async def main():
    """"""
    global db_pool
    logger.info("Starting PDF bot...")

    await init_db()
    dp.include_router(router)
    await dp.start_polling(bot)

    if db_pool:
        await db_pool.close()

if __name__ == "__main__":
    asyncio.run(main())
