from salver.engine.scans import Scan
from salver.engine.scans.single_collector import SingleCollectorStrategy
from salver.engine.scans.full_scan import FullScanStrategy

from salver.common.facts import Email, Username, Company, Domain

scan = Scan(strategy=SingleCollectorStrategy(collector_name="little-brother"))
#scan = Scan(strategy=FullScanStrategy())

scan.run(facts=[
    Company(name="wavely"),
    Username(name="jurelou"),
    Domain(fqdn="wavely.fr")
])