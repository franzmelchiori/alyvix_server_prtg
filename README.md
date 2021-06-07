# PRTG custom sensor for Alyvix Server

This PRTG custom sensor performs the monitoring of ongoing Alyvix test
cases, that run thanks to Alyvix Server, extending your standard sensor
set.

This Python sensor requests the RESTful web API of Alyvix Server and
returns JSON to map results to channels.

Deployment:
1. install `sensor_alyvix_server.py` in the folder
   `C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python`
   on the PRTG probe, i.e., the Alyvix Server Windows machine
2. add a "Python Script Advanced" PRTG sensor for that PRTG probe,
   inserting, in particular, the Alyvix test case alias in the
   "Additional Parameters", e.g., `visittrentino`
