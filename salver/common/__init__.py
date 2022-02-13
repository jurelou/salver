# -*- coding: utf-8 -*-
import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<level>{level: <6}</level> | <cyan>{name}:{line}</cyan> - <level>{message}</level>",
)
