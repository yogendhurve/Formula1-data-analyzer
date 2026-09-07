import sys
import os

# Force reload .env file with override
from dotenv import load_dotenv
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'

print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")

load_dotenv(dotenv_path=env_path, override=True)

# Verify what was loaded
print(f"API_BASE_URL loaded: {os.getenv('API_BASE_URL')}")
print(f"API_FALLBACK_URL loaded: {os.getenv('API_FALLBACK_URL')}")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from f1_pipeline.config.settings import get_config
from f1_pipeline.ingestion.orchestrator import F1DataIngester

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    """Main execution function."""
    config = get_config()

    # Use api_base_url from config
    api_url = config["api_base_url"]
    logger.info(f"Using API URL: {api_url}")

    ingester = F1DataIngester(
        api_base_url=api_url,
        db_config=config["database"]
    )

    seasons = [2023]
    max_laps = 25

    ingester.ingest_and_load(seasons, max_laps)


if __name__ == "__main__":
    main()