# HouseDivided
This repo contains the data, scripts, notebooks, and images used for a project exploring voting behavior in the 114th United States Senate.

There is a [blog](http://www.adammassachi.com/senate-114/) with analysis and commentary on the preliminary results. Some of the inspiration for this project came from a [paper](http://www.stat.columbia.edu/~jakulin/Politics/) on the 2003 Senate. I have incldued their code in this project's repo, in the folder `senate-mining`, though I don't make use of any of it. 

The data is comprised of three major components. 
 - `votes.csv` includes 502 rows, each a particualr rolll call vote in the Senate. There are 101 columns, one for each senator and one for the final outcome. 
 - `cleaned_votes.csv` is numerical representation of `votes.csv`
 - `all_bills.csv` contains information on each vote and issue, such as the result, title, question type, etc. 
 - `senators114.csv` contains information on each senator, such as their seniority, number of missed votes, etc
 - `member_masterlist.pkl` is a pickle of a dictionary containing information on several US Senate Classes


The primary aims of this project include:
 - Developing a mathematical model of influence in the senate to create an influence score for senators and a distance metric for the voting records (which are vectors like `Schumer = [0, 1, 1, 0, 1, 0, ...]`). I borrow many ideas and techniques from information thoery, inlcuding entropy, mutual information, and informaiton gain. 
 - Performing hierarchical clustering analysis with this metric to explore underlying groups of senators and influence. 
 - Predicting the party of a given senator given the voting record using decision trees to identify which issues are most important to party identity. 
 - Testing a thought experiment. 

 The thought experiment: 
 Predicting Outcomes

 





First, I explore the roll call data. The `all_bills.csv` dataset describes the 502 roll call votes, the total for both sessions. Missing votes by the senators are explored and dicussed [here](http://www.adammassachi.com/missing-votes/) 

Next, I apply PCA to create a synthetic vote space and agglomerative clustering methods to reveal some of the underlying structure of senators' voting patterns. The [clusters](http://www.adammassachi.com/clusters/) match exactly the natural party divide. 

The [dendrogram](http://www.adammassachi.com/clusters/dendrogram.png) offers more insight into the clustering algorithm. Notably, Cruz (R-TX), Rubio (R-FL), Graham (R-SC), Kirk (R-IL), and Sanders (I-VT) are very dissimilar to other Senators because all missed many votes in election season. All except Kirk ran for president -- and Kirk lost reelection in a tough IL Senate race to then Rep. Tammy Duckworth. 

We represent each senator as a vector with 502 binary elements, something like this `Schumer = [0, 1, 1, 0, ...]`. 

I show that we can correctly classify party affiliation with 100% accuracy using any subset of 20 senators as a training sample. This helps to confirm intuitions about the distance between Republican and Democratic voting records offered by the clustering analysis. 

Next, I introduce a distance metric derived from the measure of Mutual Information and entropy in information theory. The inspiration for this metric can be found in the `senate-mining` folder. 

We take mutual information between the senator's voting record and the outcome to be 'influence', and rank the senators by how infleuntial they are. The metricized version of mutual information allows us to  calculate distances between each pair of senators. 