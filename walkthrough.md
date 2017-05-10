# House Divided

A thought experiment and prediction game motivated this project. 

## The thought experiment

Imagine that you are trying to predict the outcome of recent vote in the senate. 
You walk into The Senate Chamber and find that all 100 senators have just voted. 

The rules are simple:
You ask one senator of your choice how they have just voted. They will truthfully respond. 
Then, you must guess whether the bill was passed or rejected. 

** Who should you ask?**

This game can be altered to allow for any number $n$ senators with $n \leq 100$. 

 Working backwards, it's obvious that if you could ask all 100 senators how they've voted, you could guess with 100% accuracy the result of the vote. But, with $n < 100$, you must make decisions about whom to include. 


Intuitively, the senators which we consider most "influential" would be the best to ask -- in this model, the most influential senators are those senators whose votes most agree with the outcome. We'll define what agreement means and how we meausre it later. 

In this project, I'll introduce a mathematical model of influence to help answer this question. Along the way, we'll investigate the voting behavior of the senators and states, explore the issues and bills brought before The Senate, and find an answer to our question. 

## The data
Two sources provide the data.
 - Congress keeps records of the roll call votes for each session. Those are avaiable on their website. This is where I get information on the voting records and the bills and issues. 
 - ProPublica makes an API availble with a lot of information about the US Congress. This is where I gather information about each senator. 


### First contact
There is a problem with missing data. Only about 12% of bills saw all 100 senators vote. 
