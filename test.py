# -*- coding: utf-8 -*-
toto = """
Google is blocking your ip and the workaround, returning
Google is blocking your ip and the workaround, returning
        Searching 500 results.
[*] Searching Google.
Google is blocking your ip and the workaround, returning
        Searching 500 results.
[*] Searching Linkedin.

[*] No links found.


        Searching 500 results.
[*] Searching Linkedin.

[*] No users found.



[*] IPs found: 15
-------------------
34.76.255.180
34.77.50.203
35.205.72.185
51.210.45.104
51.254.131.100
95.217.85.181
134.209.198.40
137.74.171.97
164.132.235.17

[*] Emails found: 4
----------------------
contact@wavely.fr
marion.aubert@wavely.fr
nicolas.cote@wavely.fr
recrutement@wavely.fr

[*] Hosts found: 233
---------------------
annotator.dev.wavely.fr:137.74.171.97
annotator.wavely.fr:51.254.131.100
bc.annotation.wavely.fr:51.254.131.100
bc.input.wavely.fr:51.254.131.100
broker.dev.wavely.fr:137.74.171.97
broker.staging.wavely.fr:51.210.45.104
cerebro.dev.wavely.fr:137.74.171.97
cerebro.gcp.wavely.fr:35.205.72.185
cerebro.staging.wavely.fr:51.210.45.104
cerebro.staging.wavely.fr:35.205.72.185
cerebro.test.wavely.fr:35.205.72.185
cerebro.wavely.fr:51.254.131.100
cerebro2.wavely.fr:137.74.171.97
chronograf.wavely.fr:51.254.131.100
data1.wavely.fr:95.217.85.181
deployment.dev.wavely.fr:137.74.171.97
deployment.staging.wavely.fr:51.210.45.104
deployment.wavely.fr:51.254.131.100
dev.grafana.wavely.fr:51.254.131.100
dev.input.wavely.fr:51.254.131.100
enedis.wavely.fr:51.254.131.100
forwarder.dev.wavely.fr:51.254.131.100
forwarder.prod.wavely.fr:51.254.131.100
forwarder.wavely.fr:51.254.131.100
gitlab.wavely.fr:51.83.76.210
glitchtip.dev.wavely.fr:137.74.171.97
glitchtip.wavely.fr:51.254.131.100
grafana.wavely.fr:51.254.131.100
influxdb.cerebro.wavely.fr:51.254.131.100
input.cerebro.wavely.fr:51.254.131.100
input.wavely.fr:51.254.131.100
keycloak.dev.wavely.fr:137.74.171.97
keycloak.staging.wavely.fr:51.254.131.100
keycloak.staging.wavely.fr
keycloak.wavely.fr:51.254.131.100
loki.wavely.fr:35.205.72.185
map.wavely.fr:51.254.131.100
monitoring.predict.staging.wavely.fr:51.254.131.100
nuisalgo.dev.wavely.fr:51.210.45.104
nuisalgo.staging.wavely.fr:51.254.131.100
nuisalgo.staging.wavely.fr:51.210.45.104
nuisalgo.wavely.fr:51.254.131.100
openproject.wavely.fr:51.254.131.100
pgadmin.dev.wavely.fr:137.74.171.97
pgadmin.staging.wavely.fr:51.210.45.104
pgadmin.wavely.fr:51.254.131.100
predict.dev.wavely.fr:137.74.171.97
predict.staging.wavely.fr:51.254.131.100
predict.wavely.fr:51.254.131.100
pypi.staging.wavely.fr:35.205.72.185
pypi.wavely.fr:35.205.72.185
pypicloud.dev.wavely.fr:137.74.171.97
registry.cerebro.wavely.fr:95.217.85.181
registry.magneto.wavely.fr:95.217.85.181
sound.api.wavely.fr:95.217.85.181
soundbooth.dev.wavely.fr:137.74.171.97
soundbooth.wavely.fr:51.254.131.100
tadi.cerebro.test.wavely.fr:51.254.131.100
tadi.cerebro.wavely.fr:51.254.131.100
telegraf.cerebro.dev.wavely.fr:137.74.171.97
telegraf.cerebro.staging.wavely.fr:51.210.45.104
telegraf.cerebro.wavely.fr:51.254.131.100
www.wavely.fr:134.209.198.40
www.wavely.fr:164.132.235.17

[*] No Trello URLs found.
"""


import re

start = "[*] IPs found:"
end = "[*] Emails found:"
print(toto[toto.find(start) + len(start) : toto.rfind(end)])
