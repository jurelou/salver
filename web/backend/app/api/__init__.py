# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .toto import router as toto_router


router = APIRouter()

router.include_router(prefix="/toto", router=toto_router, tags=["Toto"])
