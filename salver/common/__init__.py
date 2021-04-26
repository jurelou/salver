# -*- coding: utf-8 -*-
from loguru import logger
import sys


logger.remove()
logger.add(
    sys.stdout,
    level='DEBUG',
    format='<level>{level: <6}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>',
)
