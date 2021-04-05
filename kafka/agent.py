import faust

class Scan(faust.Record, validation=True):
    name: str

app = faust.App(
    'test_app',
    broker='kafka://broker:9092',
)

schema = faust.Schema(
    value_type = Scan,
)
scan_topic = app.topic("agent_scan", schema=schema)


def done_scan(value):
    print(f"!!! G scan {value}")

@app.agent(scan_topic, sink=[done_scan])
async def agent_scan(scans):
    async for scan in scans:
        yield f"SCANNED {scan.name}"
        
    print("STOP scan agent")


@app.task
async def on_started():
    print('APP STARTED')

if __name__ == '__main__':
    app.main()

#ok