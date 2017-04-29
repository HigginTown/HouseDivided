# House Divided
This repo contains the notebooks, images, and data for my project modelling voting behavior in the 114th United States Senate. Intially, I was motivated by a thought experiment I detail below, but this grew to include other analyses as well. I hope you enjoy the interesting results! 


### The primary aims of this project include
- Developing a mathematical model of influence in the Senate to create an "influence score" for senators; creating a distance metric for the voting records (represented as vectors like `Schumer = [0, 1, 1, 0, 1, 0, ...]`). I borrow many ideas and techniques from information theory, inlcuding entropy, mutual information, and informaiton gain. The distance metric is a transformation of mutual information so that it is non negative, obeys the triangle inequality, etc. 

- Performing hierarchical clustering analysis with this metric to explore underlying groups of senators and influence. 
- Predicting the party of a given senator given the voting record, using decision trees to identify which issues are most important to party identity. 
- Testing a thought experiment. 


### The thought experiment

Imagine that you are standing outside of the Senate Chamber, attempting to discover the outcome of a roll call vote. The vote has just taken place. You walk into the chamber and find that all 100 senators have just voted. 

You are allowed to ask 1 senator of your choice how they voted, and they will respond truthfully. 
Then, you must guess the outcome of the vote -- passed or rejected. 

**So, who should you ask?**

The game can be altered to include any number `n` senators up to 100. Working backwards, it's obvious that if you could ask all 100 senators how they've voted, you could guess with 100% accuarcy the result of the vote. But, with `n < 100`, you must make decisions about whom to include. 

I show that a rank-ordered list of senators by the "influence score" is the best way to select `n` senators, e.g. If you can ask `n` senators, then selecting the first `n` senators on the ordered list outperforms all other choices. See [predictions_information.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/influence_predictions/predictions_information.png) in the gallery. 


In this model, senators can either influence one another or influence the final outcome of a vote. I model influence as an answer to one of the folllowing two questions:
 - For two senators Alice and Bob, how much does the voting behavior of Alice tell me about the voting behavior of Bob? This is the infleunce Alice has on Bob. 
 - Senators can also be influential on the outcome. How much does knowing the vote of Alice tell me about the final outcome of the vote? The more influential the senator, the more information we gain about the final vote outcome. 


 ### About this repo

There is a [blog](http://www.adammassachi.com/senate-114/) with analysis and commentary on the preliminary results. 

The data are comprised of a few major components. 
 - `votes.csv` includes 502 rows, each a particualr roll call vote in the Senate. There are 101 columns, one for each senator and one for the final outcome. 
 - `cleaned_votes.csv` is numerical representation of `votes.csv`
 - `all_bills.csv` contains information on each vote and issue, such as the result, title, question type, etc. 
 - `senators114.csv` contains information on each senator, such as their seniority, number of missed votes, etc
 - `member_masterlist.pkl` is a pickle of a dictionary containing information on several US Senate Classes

The `gallery` folder includes many of the images generated during this project. Some particular points of interest are:
 - [The clusters](http://www.adammassachi.com/clusters/senate_divided.html) of senators in a synthetic vote space constructed with PCA, on two axes. This matches the natural party divide seen in [these clusters](http://www.adammassachi.com/clusters/senate_divided_2.html). 
 - [dtc.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/cluster_correlation/dtc.png) represents a surpsringly simple decision tree fit on the roll call vote data with party label as the target variable. The tree requires just two splits to correctly map every senator to a party. The first split, `S. Con. Res 11` is a budget issue, where all Republicans voted differently from Independents and Democrats. Next the Independents differ from Democrats on `H.R. 1735`, a National Defense Authorization Act. 
 - [influence_rank.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/influence_predictions/influence_rank.png) shows the normailzed influence of each senator by their rank. 
 - [dendrogram.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/cluster_correlation/dendrogram.png) offers insight into the agglomerative clustering process. 
 - [predictions_information.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/influence_predictions/predictions_information.png) compares the strategies in the thought experiment detailed above. 
 - [influence_cumsum.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/influence_predictions/influence_cumsum.png) compares the growth in mutual informaion observed in the senate (`observed`) with hypothetical uniformally distributed influence scores.

Check out the README in the gallery folder for a complete list of image descriptions. 



### The strategy


First, we need to get the data. Go to the `scripts` folder, and find `data_collection`. I use the [ProPublica Congress API](https://propublica.github.io/congress-api-docs/#congress-api-documentation) to get data on the senators, and I scrape the roll call votes on the[Congress website](https://www.congress.gov/roll-call-votes). 

Second, I do some exploratory analysis on the roll call data and senators. Importantly, there are many [missing votes](http://www.adammassachi.com/missing-votes/) because a given senator does not vote on in every roll call. The `eda_prelim` notebook incldues this material. 

Third, in the `pca_votes_clustering` notebook, I make some preliminary [clusters](http://www.adammassachi.com/clusters/). Using PCA with two components, I create a synthetic vote space and plot the coordinates of each senator. I compare the results of a simple KMeans clustering algorithm with `k=2` with the true party labels. The results are nearly identical, except that both Independent senators are missclassifed as democrats. 




Some of the inspiration for this project came from a [paper](http://www.stat.columbia.edu/~jakulin/Politics/) on the 2003 Senate. I have incldued their code in this project's repo, in the folder `senate-mining`, though I don't make use of any of it. 

