import logging
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Generate timestamped filename for every run
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"logs/agent_{timestamp}.log"

logger = logging.getLogger("hospital_agent")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler = logging.FileHandler(
    log_filename,
    encoding="utf-8",
)

file_handler.setFormatter(formatter)

logger.handlers.clear()

logger.addHandler(file_handler)