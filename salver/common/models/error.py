# -*- coding: utf-8 -*-
from pydantic import BaseModel

<<<<<<< HEAD

=======
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
class Error(BaseModel):
    context: str
    error: str

    class Config:
        extra = 'allow'

    @staticmethod
    def to_dict(obj, _):
        return obj.dict()

    @staticmethod
    def from_dict(obj, _):
<<<<<<< HEAD
        return Error(**obj)

    @classmethod
    def elastic_mapping(cls):
        return {
            'mappings': {
                'properties': {
                    'context': {'type': 'keyword'},
                    'error': {'type': 'text'},
                },
            },
        }
=======
        return Error(**obj)
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
