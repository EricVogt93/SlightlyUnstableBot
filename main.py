"""
SlightlyUnstableBot - Discord bot for WoW guild management.

Entry point for the bot application.
"""
import logging
import sys

from BotModel import BotModel


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('bot.log', encoding='utf-8')
        ]
    )
    # Reduce noise from discord library
    logging.getLogger('nextcord').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)


def main() -> None:
    """Main entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting SlightlyUnstableBot...")

    try:
        bot = BotModel()
        bot.start_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.exception(f"Bot crashed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
