import text2emotion as te

text = 'Vacation from COVID in the United States is a fantasy thanks to never-bad-smart-people at the White House.'

results = te.get_emotion(text)

print(results)