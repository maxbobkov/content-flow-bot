# Telegram content-flow-bot

This Telegram bot helps manage photo content for your channel by allowing administrators to submit photos and automatically posting them on a schedule. Perfect for content managers who want to automate their channel's photo posting workflow.

## Features

- **Admin-only Access**: Only authorized administrators can submit photos
- **Photo Storage**: Automatically saves photos with optional captions
- **Scheduled Posting**: Posts photos twice or more daily at specified times
- **No Duplicates**: Tracks posted photos to avoid repetition
- **Admin Notifications**: Alerts admins when content pool is depleted
- **Docker Support**: Easy deployment with Docker and volume persistence

## Prerequisites

- Docker and Docker Compose installed
- Telegram Bot Token (get it from [@BotFather](https://t.me/BotFather))
- Public channel where the bot is an administrator
- Python 3.11+ (if running without Docker)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/maxbobkov/content-flow-bot.git
cd content-flow-bot
```

2. Create a `.env` file in the project root:
```env
BOT_TOKEN=your_bot_token_here
CHANNEL_ID=your_channel_id_here  # e.g., -100123456789
```

3. Configure admin access by editing `config.py`:
```python
ADMIN_IDS = [
    123456789,  # Replace with actual admin user IDs
    987654321
]
```

4. Build and start the container:
```bash
docker-compose up -d
```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to verify your admin access
3. Send photos (with optional captions) to add them to the queue
4. The bot will automatically post photos twice daily (9:00 and 21:00 by default)

## Project Structure

```
content-flow-bot/
├── bot.py           # Main bot logic
├── database.py      # Database operations
├── config.py        # Configuration settings
├── requirements.txt # Python dependencies
├── Dockerfile       # Docker image configuration
├── docker-compose.yml
└── data/           # Mounted volume for persistence
    ├── photos/     # Stored photos
    └── database.sqlite
```

## Data Storage

- Photos are stored in `data/photos/`
- Database file is located at `data/database.sqlite`
- Both directories are persisted through Docker volumes

## Customization

### Changing Post Schedule

To modify the posting schedule, edit the following in `bot.py`:

```python
scheduler.add_job(
    post_random_photo,
    trigger='cron',
    hour='9,21'  # Change these hours (24-hour format UTC)
)
```

### Adding Admins

Add new administrator IDs in `config.py`:

```python
ADMIN_IDS = [
    123456789,  # Your admin IDs here
]
```

## Development

To run the bot without Docker:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the bot:
```bash
python bot.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- [aiogram](https://github.com/aiogram/aiogram) for the excellent Telegram Bot framework
- [APScheduler](https://github.com/agronholm/apscheduler) for scheduling functionality

## Support

If you encounter any problems or have suggestions, please open an issue in the GitHub repository.
