# -*- coding: utf-8 -*-
import uuid

from pydantic import BaseModel


class UUIDResponse(BaseModel):
    id: uuid.UUID
