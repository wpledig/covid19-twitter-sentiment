# `modeling`

## Description

These files contain the code to create, train, and test several different types of models for predicting COVID=19 test
positivity rate based on the sentiment/emotion data generated elsewhere in this project.

## Usage
The code in this section can be run in any order. Running any of the files in the `src` folder will generate one type of 
model and output a graph of its generated predictions as well as the mean squared error of those predictions for testing 
and training data (if applicable). The available models are as follows: LSTM (`src/lstm.py`), NARX (`src/narx.py`), and 
ARIMA (`src/arima.py`).