from tracker.database import init_db
from tracker.logger import get_logger
import uvicorn

logger = get_logger(__name__)

init_db()
logger.info("APIサーバーを起動します")
uvicorn.run("tracker.api.main:app", reload=True)