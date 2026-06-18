import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
        ]
    )

logger = logging.getLogger(__name__)
logging.getLogger("watchfiles").setLevel(logging.WARNING)