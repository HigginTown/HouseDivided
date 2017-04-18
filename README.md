# HouseDivided
This repo contains the data, scripts, notebooks, and images used for a project exploring voting behavior in the 114th United States Senate.

There is a [blog](http://www.adammassachi.com/senate-114/) with analysis and commentary on the results. 

First, I explore the roll call data. The `all_bills.csv` dataset describes the 502 roll call votes, the total for both sessions. Missing votes by the senators are explored and dicussed [here](http://www.adammassachi.com/missing-votes/) 

Next, I apply PCA to create a synthetic vote space and agglomerative clustering methods to reveal some of the underlying structure of senators' voting patters. The [clusters](http://www.adammassachi.com/clusters/) match exactly the natural party divide. 

The [dendrogram](http://www.adammassachi.com/clusters/dendrogram.png) offers more insight into the clustering algorithm. Notably, Cruz (R-TX), Rubio (R-FL), Graham (R-SC), Kirk (R-IL), and Sanders (I-VT) are very dissimilar to other Senators because all missed many votes in election season. All except Kirk ran for president -- and Kirk lost reelection in tough IL Senate race to then Rep. Tammy Duckworth. 

I show that we can predict party affiliation with 100% accuracy using any subset of 20 senators as a training sample. This helps to confirm intuitions about the distance between Republican and Democratic voting records offered by the clustering analysis. 

Next, I introduce a distance metric derived from the measure of Mutual Information and entropy in information theory. The inspiration for this metric can be found in the `.pdf` in the repo. 

We take mutual information between the senator's voting record and the outcome to be 'influence', and rank the senators by how infleuntial they are. The metricized version of mutual information allows us to  calculate distances between each pair of senators. 