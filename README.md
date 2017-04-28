# House Divided
This repo contains the relevant files exploring voting behavior in the 114th United States Senate.

There is a [blog](http://www.adammassachi.com/senate-114/) with analysis and commentary on the preliminary results. 

The data are comprised of a few major components. 
 - `votes.csv` includes 502 rows, each a particualr roll call vote in the Senate. There are 101 columns, one for each senator and one for the final outcome. 
 - `cleaned_votes.csv` is numerical representation of `votes.csv`
 - `all_bills.csv` contains information on each vote and issue, such as the result, title, question type, etc. 
 - `senators114.csv` contains information on each senator, such as their seniority, number of missed votes, etc
 - `member_masterlist.pkl` is a pickle of a dictionary containing information on several US Senate Classes

The `gallery` folder includes many of the images generated during this project. Some particular points of interest are:
 - [dtc.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/dtc.png) represents a surpsringly simple decision tree fit on the roll call vote data with party label as the target variable. The tree requires just two splits to correctly map every senator to a party. The first split, `S. Con. Res 11` is a budget issue, where all Republicans voted differently from Independents and Democrats. Next the Independents differ from Democrats on `H.R. 1735`, a National Defense Authorization Act. 
 - [influence_rank.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/influence_rank.png) shows the normailzed influence of each senator by their rank. 
 - [dendrogram.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/dendrogram.png) offers insight into the agglomerative clustering process. 
 - [predictions_information.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/predictions_information.png) compares the strategies in the thought experiment detailed below. 

Check out the README in the gallery folder for a complete list of image descriptions. 



### The primary aims of this project include:
 - Developing a mathematical model of influence in the senate to create an influence score for senators and a distance metric for the voting records (represented as vectors like `Schumer = [0, 1, 1, 0, 1, 0, ...]`). I borrow many ideas and techniques from information theory, inlcuding entropy, mutual information, and informaiton gain. 
 - Performing hierarchical clustering analysis with this metric to explore underlying groups of senators and influence. 
 - Predicting the party of a given senator given the voting record using decision trees to identify which issues are most important to party identity. 
 - Testing a thought experiment. 

### The thought experiment: 

Imagine that you are standing outside of the Senate Chamber, trying to discover the outcome of a roll call vote. The vote has just taken place. You walk into the chamber and find that all 100 senators have just voted. 

You are allowed to ask 1 senator of your choice how they voted, and they will respond truthfully. 
Then, you must guess whether the vote passed or was rejected. 

**So, who should you ask?**

The game can be altered to include any number `n` senators up to 100. Working backwards, it's obvious that if you could ask all 100 senators how they've voted, you could guess with 100% accuarcy the result of the vote. But, with `n < 100`, you must make decisions about whom to include. 

I show that a rank-ordered list of senators by our influence score is the best way to select `n` senators, e.g. If you can ask `n` senators, then selecting the first `n` senators on the ordered list outperforms all other choices. 

### The strategy


First, I explore the roll call data. Missing votes by the senators are explored and dicussed [here](http://www.adammassachi.com/missing-votes/) 

Next, I apply PCA to create a synthetic vote space and agglomerative clustering methods to reveal some of the underlying structure of senators' voting patterns. The [clusters](http://www.adammassachi.com/clusters/) match exactly the natural party divide. 

The [dendrogram](http://www.adammassachi.com/clusters/dendrogram.png) offers more insight into the clustering algorithm. Notably, Cruz (R-TX), Rubio (R-FL), Graham (R-SC), Kirk (R-IL), and Sanders (I-VT) are very dissimilar to other Senators because all missed many votes in election season. All except Kirk ran for president -- and Kirk lost reelection in a tough IL Senate race to then Rep. Tammy Duckworth. 

We represent each senator as a vector with 502 binary elements, something like this `Schumer = [0, 1, 1, 0, ...]`. 

I show that we can correctly classify party affiliation with 100% accuracy using any subset of 20 senators as a training sample. This helps to confirm intuitions about the distance between Republican and Democratic voting records offered by the clustering analysis. 

Next, I introduce a distance metric derived from the measure of Mutual Information and entropy in information theory. The inspiration for this metric can be found in the `senate-mining` folder. 

We take mutual information between the senator's voting record and the outcome to be 'influence', and rank the senators by how infleuntial they are. The metricized version of mutual information allows us to  calculate distances between each pair of senators. 


Some of the inspiration for this project came from a [paper](http://www.stat.columbia.edu/~jakulin/Politics/) on the 2003 Senate. I have incldued their code in this project's repo, in the folder `senate-mining`, though I don't make use of any of it. 