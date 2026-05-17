import aiosqlite
from datetime import datetime

async def check_wear(bot):
    async with aiosqlite.connect("spinbox.db") as db:
        async with db.execute("SELECT id, user_id, install_date FROM my_equipment WHERE active=1") as cursor:
            eqs = await cursor.fetchall()
        for eq_id, user_id, install_date in eqs:
            # Суммируем минуты тренировок, где использовалась эта ракетка после даты установки
            async with db.execute(
                "SELECT SUM(duration_minutes) FROM trainings WHERE racket_id=? AND datetime >= ?",
                (eq_id, install_date)
            ) as c:
                total = (await c.fetchone())[0] or 0
            hours = total / 60
            if hours >= 100:
                try:
                    await bot.send_message(user_id,
                        f"⚠️ Ваша ракетка (ID {eq_id}) набрала {hours:.0f} часов игры. Рекомендуется заменить накладки.")
                except Exception as e:
                    print(f"Не удалось отправить уведомление пользователю {user_id}: {e}")