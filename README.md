# TokenOfCareBot

[![CI/CD Pipeline](https://github.com/yuriisurzhykov/TokenOfCareBot/actions/workflows/deploy.yml/badge.svg)](https://github.com/yuriisurzhykov/TokenOfCareBot/actions)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram&logoColor=white)](https://t.me/tokenofcarebot)
[![OpenAI](https://img.shields.io/badge/OpenAI-Powered-4527A0?logo=openai&logoColor=white)](https://openai.com/api/)
[![GitHub issues](https://img.shields.io/github/issues/yuriisurzhykov/TokenOfCareBot)](https://github.com/yuriisurzhykov/TokenOfCareBot/issues)
[![License](https://img.shields.io/github/license/yuriisurzhykov/TokenOfCareBot)](https://github.com/yuriisurzhykov/TokenOfCareBot/blob/main/LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/yuriisurzhykov/TokenOfCareBot)](https://github.com/yuriisurzhykov/TokenOfCareBot/commits/main)

---

## Overview

**TokenOfCareBot** is a Telegram bot designed to help husbands and boyfriends surprise their wives or girlfriends with thoughtful, unexpected gifts. Powered by OpenAI, it generates creative gift ideas and schedules randomized reminders within your specified intervals — so you never miss a chance to show you care.

---

## Features

- 🎁 **AI-driven gift ideas:** Get fresh, creative gift suggestions tailored to your needs.
- ⏰ **Randomized reminders:** Configure flexible intervals for random gift reminders.
- 🔄 **Persistent user settings:** All preferences are securely saved using Firebase Firestore.
- 🚀 **CI/CD ready:** Fully integrated with GitHub Actions for seamless deployment.
- 🐳 **Docker support:** Easy containerized setup for reliable operation.

---

## Requirements

- Python 3.10+
- Telegram Bot Token (from [BotFather](https://core.telegram.org/bots#6-botfather))
- OpenAI API Key
- Firebase service account JSON credentials for Firestore
- Firebase Project ID

Environment variables to configure:

| Variable               | Description                              |
|------------------------|------------------------------------------|
| `TELEGRAM_BOT_TOKEN`   | Telegram bot token                        |
| `OPENAI_API_KEY`       | OpenAI API key                            |
| `FIREBASE_CREDENTIALS` | Path to Firebase service account JSON     |
| `FIREBASE_PROJECT_ID`  | Firebase GCP project ID                   |

---

## Installation & Usage

### Docker (recommended)

Build the Docker image:

```bash
docker build -t tokenofcarebot .
```

Run the container:

```bash
docker run -d --name tokenofcarebot \
  -e TELEGRAM_BOT_TOKEN=<your_telegram_token> \
  -e OPENAI_API_KEY=<your_openai_key> \
  -e FIREBASE_CREDENTIALS=/app/serviceAccountKey.json \
  -e FIREBASE_PROJECT_ID=<your_firebase_project_id> \
  tokenofcarebot
```

> **Note:** Make sure to mount your Firebase JSON credentials into the container or bake them into the image securely.

---

### Local setup

1. Clone the repo:

```bash
git clone https://github.com/yuriisurzhykov/TokenOfCareBot.git
cd TokenOfCareBot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables (or create a `.env` file):

```bash
export TELEGRAM_BOT_TOKEN=<your_telegram_token>
export OPENAI_API_KEY=<your_openai_key>
export FIREBASE_CREDENTIALS=<path_to_your_firebase_json>
export FIREBASE_PROJECT_ID=<your_firebase_project_id>
```

4. Run the bot:

```bash
python src/app.py
```

---

## Usage

Interact with the bot on Telegram by searching for its username and sending commands:

- `/start` — show welcome message and instructions  
- `/setinterval <min_days> <max_days>` — set the random reminder interval in days (e.g., `/setinterval 7 14`)  
- `/showinterval` — display current reminder interval  
- `/generate` — get instant AI-generated gift ideas  

The bot will send you randomized gift reminders within the configured interval.

---

## Contribution

Contributions, bug reports, and feature requests are welcome! Please open issues or pull requests on GitHub. Code quality is enforced through CI/CD pipelines.

---

## License

This project is licensed under a custom non-commercial license.  
You may not use or redistribute the code without explicit permission.  
See the full [LICENSE](./LICENSE.md) for details.

---

© 2025 Yurii Surzhykov — TokenOfCareBot
