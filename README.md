# Predicting COVID-19 Infection Rates Using Twitter Sentiment

## Project Description
Through this project, we investigated how sentiments expressed about the COVID-19 pandemic on social media interact with public health outcomes, and whether they are an effective predictor of future outcomes.

Our objectives in the project included:

- Sentiment analysis of a large dataset of Twitter posts, ranging across time and space

- Analysis of how sentiments interact with public health outcomes over time and space, identifying which sentiments correlate with positive outcomes and which sentiments correlate with negative outcomes

- A model which, given sentiment over a time and space, predicts COVID-19 infection and mortality rates

## Usage
All of the code in this project uses Python 3.

The code for this project is separated into different folders based on function, and should be run in a designated order. Please see below for their descriptions.

### Folders
1. `data-collection`
    <p>
    All of the code needed to load / clean the dataset, as well as the files containing the data itself.
    </p>
2. `exploration`
    <p>
    Code to aggregate different features of the raw dataset, and the files representing the results of those.
    </p>
3. `sentiment-tagging`
    <p>
    Code to tag tweets with sentiment/emotion values and compute the daily averages of such values.
    </p>
4. `visualization`
    <p>
    Code to create visualizations/graphs of the data (and the image files for those visualizations).
    </p>
5. `modeling`
    <p>
    Code to create and run models that predict the positivity rate of COVID-19 tests in the US based on Twitter emotion 
    and sentiment.
    </p>    

