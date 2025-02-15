# amper-trawers-translator

Sample integration between AMPER <-> TRAWERS

## Prerequisites

Before you start, make sure you set necessary environment variables

- **AMPER_USERNAME** - AMPER user 
- **AMPER_PASS** - AMPER password
- **AMPER_WS_URL** - url of AMPER webservice
- **TRAWERS_SOA_URL** - url od TRAWERS SOA service

```
AMPER_USERNAME=
AMPER_PASS=
AMPER_WS_URL=
TRAWERS_SOA_URL=
```

## Running program

There are two type of jobs
- **import** _-i_ - jobs responsible for fetching changes from TRAWERS and sending it to AMPER
- **export** _-e_ - jobs responsible for sending documents, orders etc from AMPER to TRAWERS
 
Example

``
python runner.py -i products
``