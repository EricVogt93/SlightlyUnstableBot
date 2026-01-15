# SlightlyUnstableBot

A Discord bot template for managing World of Warcraft guilds. Handles player management, weekly taxation, vacation tracking, raid signups, and trial member management.

**This project is designed as a template** - fork it and customize it for your own guild!

## Features

- **Player Management**: Add/remove players, track Discord IDs
- **Tax System**: Configurable weekly tax (flasks, gold, materials - whatever your guild needs)
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

# Tax configuration
TAX_PER_WEEK=18
TAX_NAME=flasks
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

## Customization

### Tax System

The tax system is fully configurable:

- `TAX_PER_WEEK`: Amount owed per week (e.g., 18 flasks, 500 gold)
- `TAX_NAME`: What to call the tax in messages (e.g., "flasks", "gold", "materials")

Examples:
```env
# For flask tax
TAX_PER_WEEK=18
TAX_NAME=flasks

# For gold tax
TAX_PER_WEEK=500
TAX_NAME=gold

# For material tax
TAX_PER_WEEK=50
TAX_NAME=enchanting materials
```

### Guild-Specific Configuration

Edit `res/bot_config.ini` to customize:
- Error messages
- Fun command responses
- URLs (WoW Audit, guild spreadsheet, progress tracking)

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
│   ├── services/               # Business logic
│   │   └── TaxService.py       # Tax calculation
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
| `/add_tax` | Record tax payment |
| `/fetch_all` | List all players with tax status |

### Trial Management (Officer only)
| Command | Description |
|---------|-------------|
| `/show_trials` | List all trial members |
| `/make_trial` | Mark a member as trial |
| `/kick_trial` | Kick a trial member |

### Information
| Command | Description |
|---------|-------------|
| `/tax` | Check tax status for a player |
| `/gildentab` | Get guild spreadsheet link |
| `/wowaudit` | Get WoW Audit link |
| `/progress` | Get progress tracking link |
| `/help` | Show all commands |

### Reminders (Officer only)
| Command | Description |
|---------|-------------|
| `/start_tax_reminder` | Start daily tax payment reminder |
| `/stop_tax_reminder` | Stop tax payment reminder |

### Music
| Command | Description |
|---------|-------------|
| `/join` | Join your voice channel |
| `/leave` | Leave voice channel |
| `/play` | Play audio from URL |
| `/skip` | Skip current track |
| `/queue` | Show music queue |

## Tax System

The bot tracks payments using a **date-based system** that handles year boundaries correctly:

- **Tax Rate**: Configurable via `TAX_PER_WEEK` environment variable
- **Tracking**: Stores "paid until" date instead of raw counts
- **Credit**: Players can pay ahead and accumulate unlimited credit
- **Reminders**: Automatic daily reminders for overdue players

### How it works

1. New players start with `paid_until = today` (no debt)
2. When payment is added: `paid_until += (amount / tax_rate) weeks`
3. Status check: `weeks_ahead = (paid_until - today) / 7`
4. If `weeks_ahead < 0`: player is behind and owes tax

## Running Tests

```bash
pytest tests/ -v
```

## License

MIT License - Feel free to use this as a template for your own guild bot!
