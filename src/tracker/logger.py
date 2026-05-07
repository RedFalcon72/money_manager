import logging
from pathlib import Path

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # コンソール出力
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # ファイル出力
    file = logging.FileHandler(Path("logs/tracker.log"), encoding="utf-8")
    file.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    console.setFormatter(formatter)
    file.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file)

    return logger