# 🤖 RecProg ITMO Bot

@itmo_recs_bot

Telegram‑бот, который помогает абитуриентам выбрать между двумя магистерскими программами ИТМО:

- **Искусственный интеллект**  
- **Управление ИИ‑продуктами**

Бот ведёт диалог, задаёт наводящие вопросы и на основе описаний и учебных планов программ (JSON‑файлы с программами направлений) помогает пользователю понять, какая программа ему больше подходит.

---

## 🚀 Функционал

- `/start` — приветственное сообщение и выбор режима.  
- **Начать 🚀** — запуск диалога с ботом.  
- Бот задаёт вопросы и сам подсказывает, какая программа больше соответствует интересам пользователя.  
- **Завершить ❌** — выход из диалога.  
- Хранение истории сообщений и шагов пользователя в базе (PostgreSQL).  
- Парсинг PDF учебных планов и описаний программ с сайта ИТМО (локально)
- Использование LLM моделей для ответов на вопросы (OpenAI API)

---

## 🛠️ Технологии

- [Python 3.9+](https://www.python.org/)  
- [Telethon](https://github.com/LonamiWebs/Telethon) — Telegram API клиент  
- [OpenAI API](https://platform.openai.com/) — генерация ответов (GPT‑4o mini)  
- [PostgreSQL](https://www.postgresql.org/) — база данных для хранения пользователей и диалогов  
- [pdfplumber](https://github.com/jsvine/pdfplumber) — парсинг учебных планов  
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — парсинг описаний программ с сайта  

---

## ⚙️ Установка и запуск

### 1. Клонирование проекта
```bash
git clone https://github.com/<your-repo>/rec_prog_itmo.git
cd rec_prog_itmo

python3 -m venv venv
source venv/bin/activate

nano config/config.yml (необходимо добавить ваши ключи)
nano config.json (креды к БД)

python -m bot.main / nohup ./venv/bin/python3 -m bot.main > bot.log 2>&1 &
```

## Как делал

- Собрал данные о программах с сайта abit.itmo.ru.
- Распарсил PDF учебные планы через pdfplumber + ChatGPT
- Преобразовал их в JSON (openai), чтобы использовать как контекст для GPT
- Реализовал Telegram‑бота на Telethon, который:

- ведёт диалог с пользователем,

- хранит историю сообщений и шаги в Postgres,

- взаимодействует с OpenAI API для ответов.

- Настроил деплой на сервер (Ubuntu) с venv и запуском через nohup/systemd.
