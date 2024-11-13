NOTES - IMPORTANT

STRUCTURE:

MicrosoftDefenderTI/
└── bin/
    ├── scripts.py [mdti's get and list, gen and graph] + config.ini
    └──lib/   # Python Libraries
           

# App is using Pyhton version 3.9 - all dependecies should be compatible with this version, further updates must be complient with this version
# bin/lib - asyncio folder has been removed from the MicrosoftDefenderTI/bin/lib
          - change has been done because Splunk's Pyhton is using it's own asyncio within /opt/splunk/lib compatible with this version
# graph_client_setup.py - dependant for all script calls
# config.ini - dependant for all script calls, Proxies and Azure app must be configured


Updates: 
urlib3 v.1.26.15 - added to MicrosoftDefenderTI/bin/lib as it's using an SSL protocol compatible with Splunk Enterprise (dependecy used for msgraph-sdk)



SPLUNK COMMANDS: 

FILES                                                  COMMANDS
========================================================================================================
genreputation                   | makeresults | eval host="www.example.com" | genreputation
mdtireputation                  | makeresults | eval my_host="www.example.com" | mdtireputation fieldname=my_host
mdtigetarticle                  | makeresults | eval article="EXAMPLE" | mdtigetarticle
mdtigetindicator                | makeresults | eval indicator="EXAMPLE" | mdtigetindicator
mdtiwhois                       | makeresults | eval host="www.example.com" | mdtiwhois
mdtilistarticles                | makeresults | mdtilistarticles
mdtilistindicator               | makeresults | eval article_id="EXAMPLE" | mdtilistindicators fieldname=article_id
