# What's the script?

This `scripts` folder contains scripts and notebooks which cover collecting the data, building the distance metric, clustering, prediction, and making graphs. 

`data_collection` contains two notebooks:  

  	- `api-calls` includes the API requests I made to the ProPublica API to gather information on each senate class. 
  	- `congress_scrape` incldues the XML scraping I did on the Congressional website, as well as some repackaging and cleaning of the data generally. 

 - `similarity_metric` develops the metric, calculates mutual information, does the clustering, and is generally the more mathematically focused notebook. 
