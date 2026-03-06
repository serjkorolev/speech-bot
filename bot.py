
import os
import sqlite3
import random
from typing import Optional

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)

BOT_NAME = "Шаги к чистой Речи"
TOKEN = os.getenv("BOT_TOKEN")
TEACHER_IDS = {781666546}

DB_NAME = "speech_bot.db"
PHOTO_DIR = "photos"
VOICE_DIR = "voices"

(
    ADD_TITLE,
    ADD_QUESTION,
    ADD_CORRECT,
    ADD_WRONG1,
    ADD_WRONG2,
    ADD_SOUND,
    ADD_PHOTO,
) = range(7)

DEFAULT_GAMES = [('Найди звук С 1', 'Выбери слово со звуком С', 'Сок', 'Дом', 'Рак', 'С'), ('Найди звук С 2', 'Выбери слово со звуком С', 'Сыр', 'Кит', 'Лук', 'С'), ('Найди звук С 3', 'Выбери слово со звуком С', 'Сани', 'Мяч', 'Дом', 'С'), ('Найди звук С 4', 'Выбери слово со звуком С', 'Сова', 'Река', 'Нож', 'С'), ('Найди звук С 5', 'Выбери слово со звуком С', 'Стол', 'Кот', 'Лук', 'С'), ('Звук С в начале 1', 'Выбери слово, которое начинается на С', 'Суп', 'Нос', 'Дом', 'С'), ('Звук С в начале 2', 'Выбери слово, которое начинается на С', 'Слон', 'Мак', 'Торт', 'С'), ('Звук С в конце 1', 'Выбери слово, которое заканчивается на С', 'Нос', 'Сани', 'Дом', 'С'), ('Звук С в конце 2', 'Выбери слово, которое заканчивается на С', 'Лес', 'Суп', 'Рука', 'С'), ('С или Ш 1', 'Выбери слово со звуком С', 'Сок', 'Шар', 'Жук', 'С'), ('Найди звук Ш 1', 'Выбери слово со звуком Ш', 'Шар', 'Дом', 'Рак', 'Ш'), ('Найди звук Ш 2', 'Выбери слово со звуком Ш', 'Шуба', 'Кот', 'Лук', 'Ш'), ('Найди звук Ш 3', 'Выбери слово со звуком Ш', 'Шишка', 'Мяч', 'Дом', 'Ш'), ('Найди звук Ш 4', 'Выбери слово со звуком Ш', 'Школа', 'Река', 'Нож', 'Ш'), ('Найди звук Ш 5', 'Выбери слово со звуком Ш', 'Шапка', 'Кит', 'Сок', 'Ш'), ('Звук Ш в начале 1', 'Выбери слово, которое начинается на Ш', 'Шкаф', 'Лес', 'Дом', 'Ш'), ('Звук Ш в начале 2', 'Выбери слово, которое начинается на Ш', 'Шило', 'Нос', 'Мак', 'Ш'), ('Звук Ш в конце 1', 'Выбери слово, которое заканчивается на Ш', 'Камыш', 'Шар', 'Лук', 'Ш'), ('Звук Ш в конце 2', 'Выбери слово, которое заканчивается на Ш', 'Малыш', 'Шапка', 'Дом', 'Ш'), ('Ш или С 1', 'Выбери слово со звуком Ш', 'Шум', 'Сок', 'Рак', 'Ш'), ('Найди звук Р 1', 'Выбери слово со звуком Р', 'Рак', 'Дом', 'Сок', 'Р'), ('Найди звук Р 2', 'Выбери слово со звуком Р', 'Рука', 'Кит', 'Лук', 'Р'), ('Найди звук Р 3', 'Выбери слово со звуком Р', 'Рыба', 'Мяч', 'Дом', 'Р'), ('Найди звук Р 4', 'Выбери слово со звуком Р', 'Роза', 'Нож', 'Суп', 'Р'), ('Найди звук Р 5', 'Выбери слово со звуком Р', 'Рама', 'Кот', 'Лиса', 'Р'), ('Звук Р в начале 1', 'Выбери слово, которое начинается на Р', 'Робот', 'Нос', 'Дом', 'Р'), ('Звук Р в начале 2', 'Выбери слово, которое начинается на Р', 'Река', 'Мак', 'Сыр', 'Р'), ('Звук Р в конце 1', 'Выбери слово, которое заканчивается на Р', 'Шар', 'Роза', 'Дом', 'Р'), ('Звук Р в конце 2', 'Выбери слово, которое заканчивается на Р', 'Комар', 'Рука', 'Лес', 'Р'), ('Р или Л 1', 'Выбери слово со звуком Р', 'Рука', 'Луна', 'Дом', 'Р'), ('Найди звук Л 1', 'Выбери слово со звуком Л', 'Лук', 'Дом', 'Рак', 'Л'), ('Найди звук Л 2', 'Выбери слово со звуком Л', 'Лиса', 'Кит', 'Нож', 'Л'), ('Найди звук Л 3', 'Выбери слово со звуком Л', 'Луна', 'Мяч', 'Дом', 'Л'), ('Найди звук Л 4', 'Выбери слово со звуком Л', 'Лампа', 'Река', 'Суп', 'Л'), ('Найди звук Л 5', 'Выбери слово со звуком Л', 'Лист', 'Кот', 'Жук', 'Л'), ('Звук Л в начале 1', 'Выбери слово, которое начинается на Л', 'Ложка', 'Нос', 'Дом', 'Л'), ('Звук Л в начале 2', 'Выбери слово, которое начинается на Л', 'Лев', 'Мак', 'Сыр', 'Л'), ('Звук Л в конце 1', 'Выбери слово, которое заканчивается на Л', 'Стол', 'Лиса', 'Дом', 'Л'), ('Звук Л в конце 2', 'Выбери слово, которое заканчивается на Л', 'Пенал', 'Луна', 'Рука', 'Л'), ('Л или Р 1', 'Выбери слово со звуком Л', 'Лук', 'Рука', 'Дом', 'Л'), ('Найди звук З 1', 'Выбери слово со звуком З', 'Зуб', 'Дом', 'Рак', 'З'), ('Найди звук З 2', 'Выбери слово со звуком З', 'Зонт', 'Кит', 'Лук', 'З'), ('Найди звук З 3', 'Выбери слово со звуком З', 'Заяц', 'Мяч', 'Дом', 'З'), ('Найди звук З 4', 'Выбери слово со звуком З', 'Замок', 'Нож', 'Суп', 'З'), ('Найди звук З 5', 'Выбери слово со звуком З', 'Зебра', 'Кот', 'Лиса', 'З'), ('Звук З в начале 1', 'Выбери слово, которое начинается на З', 'Зима', 'Нос', 'Дом', 'З'), ('Звук З в начале 2', 'Выбери слово, которое начинается на З', 'Змея', 'Мак', 'Сыр', 'З'), ('Звук З в конце 1', 'Выбери слово, которое заканчивается на З', 'Арбуз', 'Зонт', 'Дом', 'З'), ('Звук З в конце 2', 'Выбери слово, которое заканчивается на З', 'Таз', 'Заяц', 'Рука', 'З'), ('З или Ж 1', 'Выбери слово со звуком З', 'Зубы', 'Жук', 'Дом', 'З'), ('Найди звук Ж 1', 'Выбери слово со звуком Ж', 'Жук', 'Дом', 'Рак', 'Ж'), ('Найди звук Ж 2', 'Выбери слово со звуком Ж', 'Жираф', 'Кит', 'Лук', 'Ж'), ('Найди звук Ж 3', 'Выбери слово со звуком Ж', 'Жёлудь', 'Мяч', 'Дом', 'Ж'), ('Найди звук Ж 4', 'Выбери слово со звуком Ж', 'Жилет', 'Нож', 'Суп', 'Ж'), ('Найди звук Ж 5', 'Выбери слово со звуком Ж', 'Жаба', 'Кот', 'Лиса', 'Ж'), ('Звук Ж в начале 1', 'Выбери слово, которое начинается на Ж', 'Журнал', 'Нос', 'Дом', 'Ж'), ('Звук Ж в начале 2', 'Выбери слово, которое начинается на Ж', 'Жар', 'Мак', 'Сыр', 'Ж'), ('Звук Ж в конце 1', 'Выбери слово, которое заканчивается на Ж', 'Морж', 'Жук', 'Дом', 'Ж'), ('Звук Ж в конце 2', 'Выбери слово, которое заканчивается на Ж', 'Гараж', 'Жаба', 'Рука', 'Ж'), ('Ж или З 1', 'Выбери слово со звуком Ж', 'Жук', 'Зонт', 'Дом', 'Ж')]
VOICE_GAMES = {'С': [('Голосовой звук С 1', 'Скажи голосом: сок, сова, сани. Потом отправь голосовое сообщение.'), ('Голосовой звук С 2', 'Скажи голосом: суп, слон, сыр.'), ('Голосовой звук С 3', 'Скажи голосом: сам, сом, стол.'), ('Голосовой звук С 4', 'Скажи голосом: лес, нос, ананас.'), ('Голосовой звук С 5', 'Скажи голосом: Саша, солнце, сад.'), ('Голосовой звук С 6', 'Скажи голосом: совок, сапоги, салат.')], 'Ш': [('Голосовой звук Ш 1', 'Скажи голосом: шар, шуба, школа.'), ('Голосовой звук Ш 2', 'Скажи голосом: шапка, шкаф, шило.'), ('Голосовой звук Ш 3', 'Скажи голосом: мышь, камыш, малыш.'), ('Голосовой звук Ш 4', 'Скажи голосом: шум, шарик, шорты.'), ('Голосовой звук Ш 5', 'Скажи голосом: шина, шаль, шутка.'), ('Голосовой звук Ш 6', 'Скажи голосом: шишка, шоссе, шоколад.')], 'Р': [('Голосовой звук Р 1', 'Скажи голосом: рак, рыба, рука.'), ('Голосовой звук Р 2', 'Скажи голосом: роза, робот, рама.'), ('Голосовой звук Р 3', 'Скажи голосом: река, ромашка, рога.'), ('Голосовой звук Р 4', 'Скажи голосом: шар, комар, топор.'), ('Голосовой звук Р 5', 'Скажи голосом: трактор, тигр, ковер.'), ('Голосовой звук Р 6', 'Скажи голосом: рысь, рынок, радуга.')], 'Л': [('Голосовой звук Л 1', 'Скажи голосом: лук, ложка, лев.'), ('Голосовой звук Л 2', 'Скажи голосом: лампа, лиса, лист.'), ('Голосовой звук Л 3', 'Скажи голосом: мел, стол, пенал.'), ('Голосовой звук Л 4', 'Скажи голосом: лодка, ладонь, луна.'), ('Голосовой звук Л 5', 'Скажи голосом: лавка, лыжи, лимон.'), ('Голосовой звук Л 6', 'Скажи голосом: дятел, узел, факел.')], 'З': [('Голосовой звук З 1', 'Скажи голосом: зуб, зонт, зима.'), ('Голосовой звук З 2', 'Скажи голосом: замок, зебра, заяц.'), ('Голосовой звук З 3', 'Скажи голосом: таз, арбуз, мороз.'), ('Голосовой звук З 4', 'Скажи голосом: завод, зеркало, звезда.'), ('Голосовой звук З 5', 'Скажи голосом: коза, ваза, береза.'), ('Голосовой звук З 6', 'Скажи голосом: змея, звонок, занавес.')], 'Ж': [('Голосовой звук Ж 1', 'Скажи голосом: жук, жираф, журнал.'), ('Голосовой звук Ж 2', 'Скажи голосом: жар, жаба, жёлудь.'), ('Голосовой звук Ж 3', 'Скажи голосом: морж, гараж, нож.'), ('Голосовой звук Ж 4', 'Скажи голосом: жилет, жёлтый, жвачка.'), ('Голосовой звук Ж 5', 'Скажи голосом: пирожок, ежи, лужа.'), ('Голосовой звук Ж 6', 'Скажи голосом: художник, дружба, лыжник.')]}

REWARD_TEXTS = [
    "🌟 Молодец! Ещё один шаг к чистой речи!",
    "⭐ Отлично получилось!",
    "🏆 Умница! Так держать!",
    "✨ Супер! Продолжаем в том же духе!",
]

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            full_name TEXT,
            role TEXT,
            stars INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            wrong_answer_1 TEXT NOT NULL,
            wrong_answer_2 TEXT NOT NULL,
            sound_group TEXT,
            photo_path TEXT,
            created_by INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_telegram_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            selected_answer TEXT NOT NULL,
            is_correct INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS voice_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_telegram_id INTEGER NOT NULL,
            child_name TEXT,
            sound_group TEXT NOT NULL,
            prompt_title TEXT NOT NULL,
            file_path TEXT,
            telegram_file_id TEXT,
            review_score INTEGER,
            reviewed_by INTEGER,
            reviewed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("PRAGMA table_info(voice_submissions)")
    existing_cols = {row[1] for row in cur.fetchall()}
    if "review_score" not in existing_cols:
        cur.execute("ALTER TABLE voice_submissions ADD COLUMN review_score INTEGER")
    if "reviewed_by" not in existing_cols:
        cur.execute("ALTER TABLE voice_submissions ADD COLUMN reviewed_by INTEGER")
    if "reviewed_at" not in existing_cols:
        cur.execute("ALTER TABLE voice_submissions ADD COLUMN reviewed_at TIMESTAMP")

    conn.commit()
    conn.close()


def seed_default_games():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT title FROM games")
    existing_titles = {row[0] for row in cur.fetchall()}

    for title, question, correct, wrong1, wrong2, sound in DEFAULT_GAMES:
        if title not in existing_titles:
            cur.execute("""
                INSERT INTO games (
                    title, question, correct_answer, wrong_answer_1, wrong_answer_2, sound_group, created_by
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, question, correct, wrong1, wrong2, sound, 0))

    conn.commit()
    conn.close()


def get_user_role(telegram_id: int) -> str:
    return "teacher" if telegram_id in TEACHER_IDS else "child"


def save_user(telegram_id: int, full_name: str, role: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO users (telegram_id, full_name, role)
        VALUES (?, ?, ?)
    """, (telegram_id, full_name, role))
    conn.commit()
    conn.close()


def get_stars(telegram_id: int) -> int:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT stars FROM users WHERE telegram_id = ?", (telegram_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def add_star(telegram_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE users SET stars = COALESCE(stars, 0) + 1 WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()


def get_all_sound_groups():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT sound_group
        FROM games
        WHERE sound_group IS NOT NULL AND TRIM(sound_group) != ''
        ORDER BY sound_group
    """)
    rows = [row[0] for row in cur.fetchall()]
    conn.close()
    return rows


def get_random_game(sound_group: Optional[str] = None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if sound_group:
        cur.execute("""
            SELECT id, title, question, correct_answer, wrong_answer_1, wrong_answer_2, sound_group, photo_path
            FROM games
            WHERE sound_group = ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (sound_group,))
    else:
        cur.execute("""
            SELECT id, title, question, correct_answer, wrong_answer_1, wrong_answer_2, sound_group, photo_path
            FROM games
            ORDER BY RANDOM()
            LIMIT 1
        """)
    game = cur.fetchone()
    conn.close()
    return game


def save_result(child_telegram_id: int, game_id: int, selected_answer: str, is_correct: bool):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO results (child_telegram_id, game_id, selected_answer, is_correct)
        VALUES (?, ?, ?, ?)
    """, (child_telegram_id, game_id, selected_answer, int(is_correct)))
    conn.commit()
    conn.close()


def save_voice_submission(child_telegram_id: int, child_name: str, sound_group: str, prompt_title: str, file_path: str, telegram_file_id: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO voice_submissions (child_telegram_id, child_name, sound_group, prompt_title, file_path, telegram_file_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (child_telegram_id, child_name, sound_group, prompt_title, file_path, telegram_file_id))
    submission_id = cur.lastrowid
    conn.commit()
    conn.close()
    return submission_id


def set_voice_review(submission_id: int, teacher_id: int, score: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        UPDATE voice_submissions
        SET review_score = ?, reviewed_by = ?, reviewed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (score, teacher_id, submission_id))
    conn.commit()
    conn.close()


def get_voice_submission(submission_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, child_telegram_id, child_name, sound_group, prompt_title, file_path, telegram_file_id, review_score
        FROM voice_submissions
        WHERE id = ?
    """, (submission_id,))
    row = cur.fetchone()
    conn.close()
    return row


def get_progress_text():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT
            u.full_name,
            COALESCE(COUNT(DISTINCT r.id), 0) as total_answers,
            COALESCE(SUM(r.is_correct), 0) as correct_answers,
            COALESCE(u.stars, 0) as stars,
            COALESCE(COUNT(DISTINCT vs.id), 0) as voice_total,
            ROUND(AVG(vs.review_score), 1) as avg_voice_score
        FROM users u
        LEFT JOIN results r ON u.telegram_id = r.child_telegram_id
        LEFT JOIN voice_submissions vs ON u.telegram_id = vs.child_telegram_id
        WHERE u.role = 'child'
        GROUP BY u.telegram_id, u.full_name, u.stars
        ORDER BY u.full_name
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return "Пока нет данных по детям."

    lines = ["📊 Прогресс детей:\n"]
    for full_name, total_answers, correct_answers, stars, voice_total, avg_voice_score in rows:
        percent = int((correct_answers / total_answers) * 100) if total_answers > 0 else 0
        avg_voice_text = avg_voice_score if avg_voice_score is not None else "нет оценки"
        lines.append(
            f"• {full_name}\n"
            f"  Ответов: {total_answers}\n"
            f"  Правильных: {correct_answers}\n"
            f"  Успех: {percent}%\n"
            f"  Звёзды: {stars}\n"
            f"  Голосовых: {voice_total}\n"
            f"  Средняя оценка голоса: {avg_voice_text}\n"
        )
    return "\n".join(lines)


def add_game_to_db(title, question, correct, wrong1, wrong2, sound_group, photo_path, created_by):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO games (
            title, question, correct_answer, wrong_answer_1, wrong_answer_2, sound_group, photo_path, created_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, question, correct, wrong1, wrong2, sound_group, photo_path, created_by))
    conn.commit()
    conn.close()


def build_teacher_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["📊 Прогресс", "➕ Добавить игру"],
            ["📋 Список звуков"]
        ],
        resize_keyboard=True
    )


def build_child_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["🎮 Начать игру", "🧩 Выбрать звук"],
            ["🎤 Голосовая игра", "⭐ Мои награды"],
            ["⏹ Закончить звук"]
        ],
        resize_keyboard=True
    )


async def send_game(update: Update, context: ContextTypes.DEFAULT_TYPE, sound_group: Optional[str] = None):
    game = get_random_game(sound_group)
    if not game:
        await update.message.reply_text("Пока игр нет для этого звука.", reply_markup=build_child_keyboard())
        return

    game_id, title, question, correct, wrong1, wrong2, sound_group_value, photo_path = game
    answers = [correct, wrong1, wrong2]
    random.shuffle(answers)

    context.user_data["current_game_id"] = game_id
    context.user_data["correct_answer"] = correct
    context.user_data["current_sound_group"] = sound_group_value

    markup = ReplyKeyboardMarkup([[answers[0]], [answers[1]], [answers[2]]], resize_keyboard=True, one_time_keyboard=True)
    text = f"🎯 {title}\nЗвук: {sound_group_value}\n\n{question}"

    if photo_path and os.path.exists(photo_path):
        with open(photo_path, "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=text, reply_markup=markup)
    else:
        await update.message.reply_text(text, reply_markup=markup)


async def send_voice_game(update: Update, context: ContextTypes.DEFAULT_TYPE, sound_group: str):
    variants = VOICE_GAMES.get(sound_group)
    if not variants:
        await update.message.reply_text("Для этого звука голосовая игра пока не добавлена.", reply_markup=build_child_keyboard())
        return

    title, prompt = random.choice(variants)
    context.user_data["waiting_voice_sound"] = sound_group
    context.user_data["waiting_voice_title"] = title
    context.user_data["selected_voice_sound"] = sound_group

    await update.message.reply_text(
        f"🎤 {title}\nЗвук: {sound_group}\n\n{prompt}",
        reply_markup=ReplyKeyboardMarkup([["⬅️ Назад"], [f"🎤 Ещё голосовое на звук {sound_group}"]], resize_keyboard=True, one_time_keyboard=True)
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    telegram_id = user.id
    full_name = user.full_name
    role = get_user_role(telegram_id)
    save_user(telegram_id, full_name, role)

    if role == "teacher":
        text = (
            f"Здравствуйте, {full_name}!\n"
            f"Вы в режиме педагога бота «{BOT_NAME}».\n"
            "Можно смотреть прогресс, принимать голосовые и добавлять новые игры."
        )
        await update.message.reply_text(text, reply_markup=build_teacher_keyboard())
    else:
        stars = get_stars(telegram_id)
        text = (
            f"Привет, {full_name}! 👋\n"
            f"Это бот «{BOT_NAME}».\n"
            "Давай потренируем речь в игре.\n"
            f"Твои звёзды: {stars} ⭐"
        )
        await update.message.reply_text(text, reply_markup=build_child_keyboard())


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    telegram_id = user.id
    role = get_user_role(telegram_id)
    text = update.message.text

    if role == "teacher":
        if text == "📊 Прогресс":
            await update.message.reply_text(get_progress_text(), reply_markup=build_teacher_keyboard())
            return
        if text == "📋 Список звуков":
            sounds = get_all_sound_groups()
            if not sounds:
                await update.message.reply_text("Пока звуки не добавлены.", reply_markup=build_teacher_keyboard())
            else:
                await update.message.reply_text("Доступные звуки: " + ", ".join(sounds), reply_markup=build_teacher_keyboard())
            return
        if text == "➕ Добавить игру":
            await update.message.reply_text("Введи название игры:")
            return ADD_TITLE
        await update.message.reply_text("Выберите действие кнопкой.", reply_markup=build_teacher_keyboard())
        return

    if text == "🎮 Начать игру":
        context.user_data.pop("selected_sound", None)
        await send_game(update, context)
        return

    if text == "🧩 Выбрать звук":
        sounds = get_all_sound_groups()
        if not sounds:
            await update.message.reply_text("Пока звуки не добавлены.", reply_markup=build_child_keyboard())
            return
        keyboard = [[f"🔤 {sound}"] for sound in sounds]
        keyboard.append(["⬅️ Назад"])
        await update.message.reply_text("Выбери звук:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return

    if text == "🎤 Голосовая игра":
        sounds = [sound for sound in get_all_sound_groups() if sound in VOICE_GAMES]
        if not sounds:
            await update.message.reply_text("Голосовые игры пока не добавлены.", reply_markup=build_child_keyboard())
            return
        keyboard = [[f"🎤 {sound}"] for sound in sounds]
        keyboard.append(["⬅️ Назад"])
        await update.message.reply_text("Выбери звук для голосовой игры:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return

    if text == "⭐ Мои награды":
        stars = get_stars(telegram_id)
        await update.message.reply_text(f"У тебя {stars} звёзд ⭐\nПродолжай заниматься!", reply_markup=build_child_keyboard())
        return

    if text == "⏹ Закончить звук":
        context.user_data.pop("selected_sound", None)
        context.user_data.pop("selected_voice_sound", None)
        context.user_data.pop("waiting_voice_sound", None)
        context.user_data.pop("waiting_voice_title", None)
        await update.message.reply_text("Серия заданий по звуку остановлена.", reply_markup=build_child_keyboard())
        return

    if text == "⬅️ Назад":
        context.user_data.pop("waiting_voice_sound", None)
        context.user_data.pop("waiting_voice_title", None)
        await update.message.reply_text("Главное меню.", reply_markup=build_child_keyboard())
        return

    if text.startswith("🔤 "):
        sound = text.replace("🔤 ", "", 1).strip()
        context.user_data["selected_sound"] = sound
        await send_game(update, context, sound_group=sound)
        return

    if text.startswith("🎤 Ещё голосовое на звук "):
        sound = text.replace("🎤 Ещё голосовое на звук ", "", 1).strip()
        context.user_data["selected_voice_sound"] = sound
        await send_voice_game(update, context, sound_group=sound)
        return

    if text.startswith("🎤 "):
        sound = text.replace("🎤 ", "", 1).strip()
        context.user_data["selected_voice_sound"] = sound
        await send_voice_game(update, context, sound_group=sound)
        return

    if "current_game_id" in context.user_data:
        game_id = context.user_data["current_game_id"]
        correct_answer = context.user_data["correct_answer"]
        current_sound = context.user_data.get("current_sound_group")
        selected_sound = context.user_data.get("selected_sound")

        is_correct = text == correct_answer
        save_result(telegram_id, game_id, text, is_correct)

        if is_correct:
            add_star(telegram_id)
            stars = get_stars(telegram_id)
            reward_text = random.choice(REWARD_TEXTS)
            await update.message.reply_text(f"✅ Правильно!\n{reward_text}\nТеперь у тебя {stars} ⭐")
        else:
            await update.message.reply_text(f"❌ Пока не так. Правильный ответ: {correct_answer}")

        context.user_data.pop("current_game_id", None)
        context.user_data.pop("correct_answer", None)
        context.user_data.pop("current_sound_group", None)

        if selected_sound:
            await update.message.reply_text("Следующее задание на тот же звук 👇")
            await send_game(update, context, sound_group=selected_sound)
            return

        await update.message.reply_text("Выбери, что делать дальше:", reply_markup=build_child_keyboard())
        return

    await update.message.reply_text("Нажми кнопку в меню.", reply_markup=build_child_keyboard())


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sound_group = context.user_data.get("waiting_voice_sound")
    prompt_title = context.user_data.get("waiting_voice_title")

    if not sound_group or not prompt_title:
        await update.message.reply_text("Сначала выбери голосовую игру.", reply_markup=build_child_keyboard())
        return

    user = update.effective_user
    voice = update.message.voice
    if not voice:
        await update.message.reply_text("Отправь именно голосовое сообщение.")
        return

    os.makedirs(VOICE_DIR, exist_ok=True)
    telegram_file = await voice.get_file()
    file_name = f"voice_{user.id}_{update.message.message_id}.ogg"
    file_path = os.path.join(VOICE_DIR, file_name)
    await telegram_file.download_to_drive(file_path)

    submission_id = save_voice_submission(
        child_telegram_id=user.id,
        child_name=user.full_name,
        sound_group=sound_group,
        prompt_title=prompt_title,
        file_path=file_path,
        telegram_file_id=voice.file_id,
    )

    add_star(user.id)
    stars = get_stars(user.id)

    review_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1", callback_data=f"rate:{submission_id}:1"),
            InlineKeyboardButton("2", callback_data=f"rate:{submission_id}:2"),
            InlineKeyboardButton("3", callback_data=f"rate:{submission_id}:3"),
            InlineKeyboardButton("4", callback_data=f"rate:{submission_id}:4"),
            InlineKeyboardButton("5", callback_data=f"rate:{submission_id}:5"),
        ],
        [
            InlineKeyboardButton("✅ Правильно", callback_data=f"rate:{submission_id}:5"),
            InlineKeyboardButton("🔁 Доработать", callback_data=f"rate:{submission_id}:2"),
        ]
    ])

    for teacher_id in TEACHER_IDS:
        try:
            await context.bot.send_message(
                chat_id=teacher_id,
                text=(
                    f"🎤 Новое голосовое от ребёнка\n"
                    f"Имя: {user.full_name}\n"
                    f"ID: {user.id}\n"
                    f"Звук: {sound_group}\n"
                    f"Упражнение: {prompt_title}\n"
                    f"ID записи: {submission_id}\n\n"
                    "Поставьте оценку кнопкой ниже:"
                ),
                reply_markup=review_markup
            )
            await context.bot.forward_message(
                chat_id=teacher_id,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.message_id,
            )
        except Exception as e:
            print(f"Не удалось отправить голосовое педагогу {teacher_id}: {e}")

    context.user_data.pop("waiting_voice_sound", None)
    context.user_data.pop("waiting_voice_title", None)

    selected_voice_sound = context.user_data.get("selected_voice_sound")
    if selected_voice_sound:
        next_keyboard = ReplyKeyboardMarkup(
            [["🎤 Ещё голосовое на звук " + selected_voice_sound], ["⏹ Закончить звук"], ["⭐ Мои награды"]],
            resize_keyboard=True
        )
        await update.message.reply_text(
            f"✅ Голосовое отправлено педагогу!\nМолодец! Теперь у тебя {stars} ⭐\n"
            f"Можно сразу записать следующее голосовое на звук {selected_voice_sound}.",
            reply_markup=next_keyboard
        )
        return

    await update.message.reply_text(
        f"✅ Голосовое отправлено педагогу!\nМолодец! Теперь у тебя {stars} ⭐",
        reply_markup=build_child_keyboard()
    )


async def handle_voice_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data or ""
    if not data.startswith("rate:"):
        return

    try:
        _, submission_id_str, score_str = data.split(":")
        submission_id = int(submission_id_str)
        score = int(score_str)
    except ValueError:
        await query.answer("Не удалось прочитать оценку", show_alert=True)
        return

    teacher_id = query.from_user.id
    if teacher_id not in TEACHER_IDS:
        await query.answer("Оценку может ставить только педагог", show_alert=True)
        return

    submission = get_voice_submission(submission_id)
    if not submission:
        await query.answer("Запись не найдена", show_alert=True)
        return

    _, child_telegram_id, child_name, sound_group, prompt_title, file_path, telegram_file_id, current_score = submission
    set_voice_review(submission_id, teacher_id, score)

    updated_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1", callback_data=f"rate:{submission_id}:1"),
            InlineKeyboardButton("2", callback_data=f"rate:{submission_id}:2"),
            InlineKeyboardButton("3", callback_data=f"rate:{submission_id}:3"),
            InlineKeyboardButton("4", callback_data=f"rate:{submission_id}:4"),
            InlineKeyboardButton("5", callback_data=f"rate:{submission_id}:5"),
        ],
        [InlineKeyboardButton(f"✅ Выбрано: {score}/5", callback_data=f"rate:{submission_id}:{score}")]
    ])

    new_text = (
        f"🎤 Голосовое от ребёнка\n"
        f"Имя: {child_name}\n"
        f"ID: {child_telegram_id}\n"
        f"Звук: {sound_group}\n"
        f"Упражнение: {prompt_title}\n"
        f"ID записи: {submission_id}\n\n"
        f"Текущая оценка: {score}/5"
    )

    try:
        await query.edit_message_text(text=new_text, reply_markup=updated_markup)
    except Exception:
        try:
            await query.edit_message_reply_markup(reply_markup=updated_markup)
        except Exception:
            pass

    try:
        await context.bot.send_message(
            chat_id=child_telegram_id,
            text=(
                f"📩 Педагог оценил твоё голосовое!\n"
                f"Звук: {sound_group}\n"
                f"Упражнение: {prompt_title}\n"
                f"Оценка: {score}/5"
            )
        )
    except Exception as e:
        print(f"Не удалось отправить оценку ребёнку {child_telegram_id}: {e}")


async def add_game_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_game_title"] = update.message.text
    await update.message.reply_text("Теперь введи вопрос для ребёнка:")
    return ADD_QUESTION


async def add_game_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_game_question"] = update.message.text
    await update.message.reply_text("Теперь введи правильный ответ:")
    return ADD_CORRECT


async def add_game_correct(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_game_correct"] = update.message.text
    await update.message.reply_text("Теперь введи неправильный ответ 1:")
    return ADD_WRONG1


async def add_game_wrong1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_game_wrong1"] = update.message.text
    await update.message.reply_text("Теперь введи неправильный ответ 2:")
    return ADD_WRONG2


async def add_game_wrong2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_game_wrong2"] = update.message.text
    await update.message.reply_text("Теперь введи звук/группу, например: С, Ш, Р:")
    return ADD_SOUND


async def add_game_sound(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_game_sound"] = update.message.text.strip()
    await update.message.reply_text("Теперь отправь фото для задания.\nЕсли фото не нужно — напиши: нет")
    return ADD_PHOTO


async def add_game_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = None

    if update.message.photo:
        os.makedirs(PHOTO_DIR, exist_ok=True)
        photo = update.message.photo[-1]
        file = await photo.get_file()
        safe_name = f"game_{update.effective_user.id}_{random.randint(1000, 999999)}.jpg"
        photo_path = os.path.join(PHOTO_DIR, safe_name)
        await file.download_to_drive(photo_path)
    elif update.message.text and update.message.text.lower().strip() == "нет":
        photo_path = None
    else:
        await update.message.reply_text("Отправь фото или напиши «нет».")
        return ADD_PHOTO

    title = context.user_data["new_game_title"]
    question = context.user_data["new_game_question"]
    correct = context.user_data["new_game_correct"]
    wrong1 = context.user_data["new_game_wrong1"]
    wrong2 = context.user_data["new_game_wrong2"]
    sound_group = context.user_data["new_game_sound"]
    teacher_id = update.effective_user.id

    add_game_to_db(title, question, correct, wrong1, wrong2, sound_group, photo_path, teacher_id)
    context.user_data.clear()
    await update.message.reply_text("Игра добавлена ✅", reply_markup=build_teacher_keyboard())
    return ConversationHandler.END


async def cancel_add_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Добавление игры отменено.", reply_markup=build_teacher_keyboard())
    return ConversationHandler.END


def main():
    init_db()
    seed_default_games()

    app = Application.builder().token(TOKEN).build()

    add_game_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^➕ Добавить игру$"), handle_text)],
        states={
            ADD_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_game_title)],
            ADD_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_game_question)],
            ADD_CORRECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_game_correct)],
            ADD_WRONG1: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_game_wrong1)],
            ADD_WRONG2: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_game_wrong2)],
            ADD_SOUND: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_game_sound)],
            ADD_PHOTO: [MessageHandler((filters.PHOTO | filters.TEXT) & ~filters.COMMAND, add_game_photo)],
        },
        fallbacks=[CommandHandler("cancel", cancel_add_game)],
        per_chat=True,
        per_user=True,
        per_message=False,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_voice_rating))
    app.add_handler(add_game_conv)
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print(f"Бот «{BOT_NAME}» запущен")
    app.run_polling()


if __name__ == "__main__":
    main()

