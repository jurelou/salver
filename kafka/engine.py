import faust
from faust.cli import argument, option

class Scan(faust.Record, validation=True):
    name: str

class Collector(faust.Record, validation=True):
    name: str


app = faust.App(
    'test_app',
    broker='kafka://broker:9092',
)

schema = faust.Schema(
    value_type = Scan,
)
scan_topic = app.topic("scan", schema=schema)

user_withdrawals = app.Table('user_withdrawals', default=int, partitions=50)

# other_topic = app.topic("other",value_type=Fact)

# @app.agent(scan_topic)
# async def execute_scan(scans):
#     async for fact in scans.events():
#         print("JE SCAN {}")
#         yield "salut"
        
#     print("STOP scan agent")


def done_scan(value):
    print("!!! G scan")

@app.agent(scan_topic, sink=[done_scan])
async def agent_scan(scans):
    async for scan in scans:
        print()
        yield f"SCANNED {scan.name}"
        
    print("STOP scan agent")


# Call totofun every 3 sec
@app.command(
)
async def produce_cmd():
        for i in range(0, 100):
            r = await agent_scan.ask(Scan(name=i))
            print(r)

@app.task
async def on_started():
    print('APP STARTED')

if __name__ == '__main__':
    app.main()

#ok