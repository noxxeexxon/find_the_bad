## What is this?
This repository contains a simple exercise for using Kibana to look at log files and try to find something malicious.  Log loading is handled for you, so all you should need to is use docker compose and then access the Kibana interface.  The data is based on logs gathered from a Windows desktop.

## Getting started
This should be as simple as doing:
- docker-compose build
- docker-compose up

## What just happened?
The docker-compose file sets up Elasticsearch, Kibana and loads up some example sysmon data.  Once the loader is done you should see a message like:
```
loader_1            | Loading logs into ES
loader_1            | Done
find_the_bad_loader_1 exited with code 0
```

## Now what?
Open your browser and go to localhost:5601 to access Kibana.  I've also provided a prebuilt dashboard to use. To load it:
- Click management in the left menu panel
- Selected "Saved Objects"
- Select Import, and pick the export.json file from the "kibana_dashes" folder.  Import it.
- After succesfully importing the dashboards, select "Dashboard" in the left menu panel
- Select the "SysmonSummaryXMLImport" dashboard
- Data exists in the time range of November 25th, 2018 to January 3rd, 2019

## Your Challenge
In this example data of roughly 64k events there is something bad.  You must find that bad.  In order to be successful you need to answer:
- What is the full path and name of the malicious image?
- What is the hash of the malicous image?
- Did it make network communications?  If so, what was the destination IP and port?
- What APT group has this image been linked to?
