# -*- coding: utf-8 -*-
import json
import os

from .bucket import Bucket


class Buckets:
    API_Buckets = {}
    saveFile = os.path.dirname(__file__) + "/bucketSave.json"

    @classmethod
    def Get_Buckets(cls, Name, rates):
        if len(rates) == 0:
            return
        cls.deserialize()
        if Name in cls.API_Buckets:
            return cls.API_Buckets[Name]
        cls.API_Buckets[Name] = [Bucket(rate.tokens, rate.getTime()) for rate in rates]
        return cls.API_Buckets[Name]

    @classmethod
    def reduce(cls, Name, TokenAmount=1):
        if Name not in cls.API_Buckets:
            return True

        def reduceAll(bucket, check=True):
            return bucket.reduce(TokenAmount, check)

        ReduceImpossible = False in list(
            [reduceAll(buck) for buck in cls.API_Buckets[Name]],
        )
        if not ReduceImpossible:
            list([reduceAll(buck, False) for buck in cls.API_Buckets[Name]])
        cls.serialize() if not ReduceImpossible else None
        return not ReduceImpossible

    @classmethod
    def nextRefill(cls, Name):
        refill_time = 0
        assert (
            Name in cls.API_Buckets
        ), f"{Name} doesn't exist, create it with Get_Buckets"
        for bucket in cls.API_Buckets[Name]:
            if bucket.get() == 0:
                refill_time = max(refill_time, bucket.next_refill())
        return refill_time

    @classmethod
    def deserialize(cls):
        if not os.path.isfile(cls.saveFile) or bool(cls.API_Buckets):
            return
        with open(cls.saveFile) as f:
            extracted = json.loads(str(f.read()))
        for key in extracted:
            cls.API_Buckets[key] = [Bucket(data) for data in extracted[key]]
        return False

    @classmethod
    def serialize(cls):
        serializedDict = {}
        for name, bcks in cls.API_Buckets.items():
            serializedDict[name] = [bck.serialize() for bck in bcks]

        with open(cls.saveFile, "w+") as f:
            f.write(json.dumps(serializedDict))
