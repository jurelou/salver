========================
Usage of Token Bucket
========================


You have to add a field "_rate_limit_" in your collector

this field should take a list of "TimeLimit", here is the possible Time limit:

 * MinuteLimit
 * HourlyLimit
 * DailyLimit
 * MonthlyLimit

TimeLimit's constructors take one required parameter (token) and a optional amount of time

Here is some examples:
   
::

   _rate_limit_ = [MinuteLimit(4)] # one TimeLimit of 4 tokens and 1 min  
   _rate_limit_ = [HourlyLimit(2, 3)] # one TimeLimit of 2 tokens and 3 h  
   _rate_limit_ = [MonthlyLimit(4), DailyLimit(1)] # two TimeLimit of 4 tokens and 1 month, 1 token and 1 day

by adding this field in your collector, the run function will create an object bucket (or not if it already exist) for every TimeLimit you provided. Next, it will try to get a token. If it fails, it will raise a "Rate Limited" error and return the next refill time (in seconds).

If you need, you can get this value in your collector using his name :

::

   Buckets.nextRefill(self._name_)