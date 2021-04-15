import text2emotion as te

# Test tweet simply to help show how text2emotion is used
text = 'Vacation from COVID in the United States is a fantasy thanks to never-bad-smart-people at the White House.'

# results will be a dictionary containing values for Angry, Fear, Happy, Sad, Surprise. The emotion with the highest values are the detected emotions within the tweet 
results = te.get_emotion(text)

print(results)