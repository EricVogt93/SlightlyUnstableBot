# SlightlyUnstableBot

A Discord bot for managing a World of Warcraft guild. Handles player management, flask taxation, vacation tracking, raid signups, and trial member management.

## Features

- **Player Management**: Add/remove players, track Discord IDs
- **Flask Taxation**: Date-based tracking system with configurable tax rate, unlimited credit accumulation, automatic reminders
- **Vacation Tracking**: Record vacation periods, query who's currently away
- **Trial System**: Manage trial members, promote or kick with reasons
- **Raid Signups**: Send embed messages with role reactions (Tank/Heal/DD)
- **Fun Commands**: Guild-specific entertainment commands
- **Music**: Play YouTube audio in voice channels

## Requirements

- Python 3.9+
- MySQL 5.7+ or MariaDB 10.3+
- Discord Bot Token

## Setup

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd SlightlyUnstableBot
pip install -r requirement.txt
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
DISCORD_TOKEN=your_discord_bot_token
DB_HOST=localhost
DB_PORT=3306
DB_NAME=subot
DB_USER=root
DB_PASSWORD=your_password
FLASK_TAX_PER_WEEK=18
```

### 3. Setup Database

Import the database schema:

```bash
mysql -u root -p subot < res/mysql_db.sql
```

### 4. Run the Bot

```bash
python main.py
```

## Project Structure

```
SlightlyUnstableBot/
├── main.py                     # Entry point
├── BotModel.py                 # Bot initialization (Singleton)
├── cogs/
│   ├── CommandRegisterService.py
│   ├── commands/               # Slash command handlers
│   │   ├── PlayerCommands.py   # Player management
│   │   ├── TrialCommands.py    # Trial member management
│   │   ├── ReminderCommands.py # Automated reminders
│   │   ├── MessageCommands.py  # Info & messaging
│   │   ├── FunCommands.py      # Entertainment
│   │   ├── ReactionCommands.py # Raid signups
│   │   └── MusicCommands.py    # Voice channel audio
│   └── events/                 # Event handlers
├── logic/
│   ├── classes/                # Core utilities
│   │   ├── DatabaseConnector.py
│   │   ├── ConfigHandler.py
│   │   └── OutputHandler.py
│   ├── models/                 # Data models
│   └── helper/                 # Utility functions
├── res/                        # Configuration files
│   ├── bot_config.ini          # Bot settings
│   └── mysql_db.sql            # Database schema
└── tests/                      # Unit tests
```

## Commands

### Player Management (Officer only)
| Command | Description |
|---------|-------------|
| `/add_gamer` | Add a player to the database |
| `/delete_gamer` | Remove a player |
| `/add_vacation` | Set vacation dates for a player |
| `/end_vacation` | End a player's vacation |
| `/add_flask` | Record flask payment |
| `/fetch_all` | List all players with flask status |

### Trial Management (Officer only)
| Command | Description |
|---------|-------------|
| `/show_trials` | List all trial members |
| `/make_trial` | Mark a member as trial |
| `/kick_trial` | Kick a trial member |

### Information
| Command | Description |
|---------|-------------|
| `/flask` | Check flask status for a player |
| `/gildentab` | Get guild spreadsheet link |
| `/wowaudit` | Get WoW Audit link |
| `/progress` | Get progress tracking link |
| `/help` | Show all commands |

### Reminders (Officer only)
| Command | Description |
|---------|-------------|
| `/start_flask_reminder` | Start daily flask payment reminder |
| `/stop_flask_reminder` | Stop flask payment reminder |

## Flask Taxation System

The bot tracks flask/potion payments using a **date-based system** that handles year boundaries correctly:

- **Tax Rate**: Configurable via `FLASK_TAX_PER_WEEK` environment variable
- **Tracking**: Stores "paid until" date instead of raw flask counts
- **Credit**: Players can pay ahead and accumulate unlimited credit
- **Reminders**: Automatic daily reminders for overdue players

### How it works

1. New players start with `paid_until = today` (no debt)
2. When flasks are added: `paid_until += (flasks / tax_rate) weeks`
3. Status check: `weeks_ahead = (paid_until - today) / 7`
4. If `weeks_ahead < 0`: player is behind and owes flasks

### Migration from old schema

If upgrading from the old `FLASK_SPEND` + `ID_JOINED` system, run the migration SQL in `res/mysql_db.sql`.

## Running Tests

```bash
pytest tests/ -v
```

## Configuration

The bot uses `res/bot_config.ini` for non-sensitive configuration like URLs, error messages, and fun command responses. Sensitive credentials (tokens, passwords) are loaded from environment variables.

## License

Private project - All rights reserved.
