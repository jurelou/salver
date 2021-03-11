import time


class Bucket:
    def __init__(self, *args):
        if isinstance(args[0], list):
            args = list(args)[0]
        self.rate = str(args[0]) + "/" + str(args[1])
        self.MaxToken, self.resetTime = args[:2]
        if len(args) > 2 and time.time() < args[2]:
            self.amount, self.lastUpdate = args[3:]
            return
        self.reset()

    def __str__(self):
        return "Rate: {}, amount {}, Maxtoken: {}, nextRefill: {}".format(
            self.rate, self.amount, self.MaxToken, self.next_refill(),
        )

    def serialize(self):
        diffTime = time.time() + self.next_refill()
        return (
            self.MaxToken,
            self.resetTime,
            diffTime,
            self.get(),
            self.lastUpdate,
        )

    def reset(self):
        self.amount = self.MaxToken
        self.lastUpdate = time.time()

    def _refill_count(self):
        return int((time.time() - self.lastUpdate) / self.resetTime)

    def get(self):
        return min(self.MaxToken, self.amount + self._refill_count() * self.MaxToken)

    def next_refill(self):
        return self.resetTime + self.lastUpdate - time.time()

    def reduce(self, tokens, check):
        refill_count = self._refill_count()
        if check:
            amount = self.amount
            amount += refill_count * self.MaxToken
            return False if tokens > amount else True

        self.amount += refill_count * self.MaxToken
        self.lastUpdate += refill_count * self.resetTime

        if self.amount >= self.MaxToken:
            self.reset()
        if tokens > self.amount:
            return False

        self.amount -= tokens
        return True
