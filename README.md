# PRTG custom sensor for Alyvix Server

This PRTG custom sensor performs the monitoring of ongoing Alyvix test
cases, that run thanks to Alyvix Server, extending your standard sensor
set.

This Python sensor requests the RESTful web API of Alyvix Server and
returns JSON to map results to channels.

Deployment:
1. install this package `alyvix_server_prtg` in a folder
   `PYTHON3_PATH\Lib\site-packages\` on the probe system (the Alyvix
   Server Windows machine)
2. install the batch file `sensor_alyvix_server.bat` in the folder
   `%programfiles(x86)%\PRTG Network Monitor\Custom Sensors\EXE` on
   the probe

JSON Return Format:
{
    "prtg": {
        "result": [
            {
             "channel": "duration",
             "value": 10, (test_case_duration_ms)
             "customunit": "ms", (-)
            },
            {
             "channel": "bla01", (transaction_alias)
             "value": 10, (transaction_performance_ms)
             "customunit": "ms", (-)
             "limitmaxerror": "30", (transaction_critical_ms)
             "limitmaxwarning": "20" (transaction_warning_ms)
             "limitmode": 1
            },
            {
             "channel": "bla02", (transaction_alias)
             "value": 10, (transaction_performance_ms)
             "customunit": "ms", (-)
             "limitmaxerror": "30", (transaction_critical_ms)
             "limitmaxwarning": "20" (transaction_warning_ms)
             "limitmode": 1
            }
        ],
        "text": "bla" (test_case_execution_code)
    }
}
