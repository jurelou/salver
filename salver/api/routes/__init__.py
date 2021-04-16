# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .cases import router as cases_router
from .scans import router as scans_router

# from .toto import router as toto_router
from .agents import router as agents_router

router = APIRouter()

router.include_router(prefix="/agents", router=agents_router, tags=["agents"])
router.include_router(prefix="/cases", router=cases_router, tags=["cases"])
router.include_router(prefix="/scans", router=scans_router, tags=["scans"])

# router.include_router(prefix="/toto", router=toto_router, tags=["Toto"])
