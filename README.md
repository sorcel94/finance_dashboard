# finance_dashboard
dashboard to show financial data, developed with flask on the BE and nodejs in FE.

the worklow is the following:

-get data from a data source (websocket or REST API)
-pipe the data to a flask application, where we can analize the data and prepare them (BE)
-show the data in a dashboard via flask templates or nodejs, using maybe bootstrap as a framework

shortcomings:

-flask might be not the best framework for the application, maybe is better to use PHP(?)
-at the moment the data are stored in a CSV file, this will be changed in a DB in the future

PER FAR RUNNARE L'APP:

- entrare nel virtual environment
- nel terminal python3 test_app.py

