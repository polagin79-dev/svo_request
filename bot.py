import asyncio
from aiogram import Dispatcher

from handlers import start, operator, start_user
from settings import Settings
from mydb.db_work import CreateDB

# Запуск бота
async def main():

    CreateDB()
    
    dp = Dispatcher()

    dp.include_routers(start.router, operator.router, start_user.router)

    # Альтернативный вариант регистрации роутеров по одному на строку
    # dp.include_router(questions.router)
    # dp.include_router(different_types.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    #await Settings.bot.delete_webhook(drop_pending_updates=True)
    try:
        task1=dp.start_polling(Settings.bot)
        #task2 = workDB(Settings.db_path, Settings.sources)
        #task3=mailing_photo(Settings.bot, f, 'случайное фото')        
        #task4=mailing_video(Settings.bot, f2, 'случайное фото')        
        await asyncio.gather(task1)#, task2, task3, task4)
        #await dp.start_polling(Settings.bot)
    finally:
        await Settings.bot.session.close()
    #await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
