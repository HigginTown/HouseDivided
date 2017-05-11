# House Divided
This repo contains the notebooks, images, and data for my project modeling voting behavior in the 114th United States Senate. Initially, I was motivated by a thought experiment I detail below, but this grew to include other analyses as well. I hope you enjoy the interesting results! 

![influence](https://github.com/HigginTown/HouseDivided/blob/master/gallery/influence_predictions/influence_map.png)


### The primary aims of this project include
- Developing a mathematical model of influence in the Senate to create an "influence score" for senators; creating a distance metric for the voting records (represented as vectors like `Schumer = [0, 1, 1, 0, 1, 0, ...]`). I borrow many ideas and techniques from information theory, inlcuding entropy, mutual information, and information gain. The distance metric is a transformation of mutual information so that it is non-negative, obeys the triangle inequality, etc. 

- Performing hierarchical clustering analysis with this metric to explore underlying groups of senators and influence. 
- Predicting the party of a given senator given the voting record, using decision trees to identify which issues are most important to party identity. 
- Testing a thought experiment. 


### The thought experiment

Imagine that you are standing outside of the Senate Chamber, attempting to discover the outcome of a roll call vote. The vote has just taken place. You walk into the chamber and find that all 100 senators have just voted. 

You are allowed to ask 1 senator of your choice how they voted, and they will respond truthfully. 
Then, you must guess the outcome of the vote -- passed or rejected. 

**So, who should you ask?**

The game can be altered to include any number `n` senators up to 100. Working backwards, it's obvious that if you could ask all 100 senators how they've voted, you could guess with 100% accuracy the result of the vote. But, with `n < 100`, you must make decisions about whom to include. 

I show that a rank-ordered list of senators by the "influence score" is the best way to select `n` senators, e.g. If you can ask `n` senators, then selecting the first `n` senators on the ordered list outperforms all other choices. See [predictions_information.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/influence_predictions/predictions_information_reverse.png) in the gallery. 


In this model, senators can either influence one another or influence the final outcome of a vote. I model influence as an answer to one of the following two questions:
 - For two senators Alice and Bob, how much does the voting behavior of Alice tell me about the voting behavior of Bob? This is the influence Alice has on Bob. 
 - Senators can also be influential on the outcome. How much does knowing the vote of Alice tell me about the final outcome of the vote? The more influential the senator, the more information we gain about the final vote outcome. 

Other motivating questions for the project include
 - Can we find a minimal subset of senators such that knowledge of their votes results in 0 uncertainty about the outcome of the total votes? 
 - Can we find a minimal subset of senators such that knowledge of their party label and voting behavior allows us to predict with 100% accuracy the party label of an unknown senator with a given voting record? 



### The strategy

![the_issues](https://github.com/HigginTown/HouseDivided/blob/master/gallery/roll_call_bills/bills_mapped.png)

![popular days](https://github.com/HigginTown/HouseDivided/blob/master/gallery/roll_call_bills/popular_days.png)

 - First, we need to get the data. Go to the `scripts` folder, and find `data_collection`. I use the [ProPublica Congress API](https://propublica.github.io/congress-api-docs/#congress-api-documentation) to get data on the senators, and I scrape the roll call votes on the [Congress website](https://www.congress.gov/roll-call-votes). 

 - Second, I do some exploratory analysis on the roll call data and senators. Importantly, there are many [missing votes](http://www.adammassachi.com/missing-votes/) because a given senator does not vote in every roll call. The `eda_prelim` notebook incldues this material. 

 - Third, in the `pca_votes_clustering` notebook, I make some preliminary [clusters](http://www.adammassachi.com/clusters/). Using PCA with two components, I create a synthetic vote space and plot the coordinates of each senator. I compare the results of a simple KMeans clustering algorithm with `k=2` with the true party labels. The results are nearly identical, except that both Independent senators are misclassified as democrats. 

 - Fourth, I fit a [decision tree](https://github.com/HigginTown/HouseDivided/blob/master/gallery/cluster_correlation/dtc.png) on the voting records and party labels, detailed below. Find this in the `predicting_outcomes` notebook section "Decision Tree". 

 - Fifth, we move to more math and modeling. In the `similarity_metric` notebook, I cover entropy, mutual information, and the distance metric. In our case, the mutual information metric is congruent to the Jaccard distance. In this notebook, I use agglomerative clustering with a distance matrix calculated using this metric. You can visualize the hierarchies in the [dendrogram.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/cluster_correlation/dendrogram.png). I model "influence" as the mutual information between the senator and the outcome. This makes intuitive sense in terms of our motivating thought experiment -- we want to learn a ranking of senators such that information about the \# 1 ranked senator reduces uncertainty about the outcome the most compared to all other senators, and so on for each senator. 

  - Sixth, go to `predicting_outcomes`. In this notebook, you can find [influence_rank.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/influence_predictions/influence_rank.png) shows the normalized influence of each senator by their rank; and [influence_cumsum.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/influence_predictions/influence_cumsum.png) compares the growth in mutual information observed in the senate (`observed`) with hypothetical uniformally distributed influence scores. 

  - Now that we have an influence ranking, we can finally begin to simulate the thought experiment. [predictions_information.png](https://github.com/HigginTown/HouseDivided/blob/master/gallery/influence_predictions/predictions_information.png) compares the strategies in the thought experiment detailed above. The strategy is a straightforward, iterative process. 

  Consider the following: 

  We will compare two strategies (plans) for simulating the thought experiment. 

  In order to justify that that the rank-ordered list by our influence score is the best way to select senators, we need, at least, Plan 1 to perform better than Plan 2:

  For both plans, we will fit a model using a subset of senators of size `n`, starting with `n = 1`, as the features, and the final outcome as the target. Then we plot the accuracy given the number of senators included for `n` in the interval `[1,100]`. The different plans describe the order in which we add senators to the model features. My hypothesis is that the influence score rank order is optimal. 

  Plan 1: Start with the senator in position 1 of the rank order list, and proceed by iteratively adding senators in the order that they appear on this list. 

  Plan 2: Choose senators at random

  It turns out that the influence score ranking **is** the best way to select `n` senators. This is an experimental result, but I am confident that we can construct a rigorous, mathematical proof of this hypothesis. The proof is left as an exercise to the reader. 


 ### Additional about this repo

There is a [blog](http://www.adammassachi.com/senate-114/) with analysis and commentary on the preliminary results. 

The data are comprised of a few major components. 
 - `votes.csv` includes 502 rows, each a particualr roll call vote in the Senate. There are 101 columns, one for each senator and one for the final outcome. 
 - `cleaned_votes.csv` is numerical representation of `votes.csv`
 - `all_bills.csv` contains information on each vote and issue, such as the result, title, question type, etc. 
 - `senators114.csv` contains information on each senator, such as their seniority, number of missed votes, etc
 - `member_masterlist.pkl` is a pickle of a dictionary containing information on several US Senate Classes




Some of the inspiration for this project came from a [paper](http://www.stat.columbia.edu/~jakulin/Politics/) on the 2003 Senate. I have incldued their code in this project's repo, in the folder `senate-mining`, though I don't make use of any of it. 

