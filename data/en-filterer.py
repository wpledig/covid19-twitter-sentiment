import csv
import linecache

input_dataset = "2021-02-15_clean-dataset.tsv"
output_dataset = "2021-02-15_clean-dataset-filtered.tsv"

filtered_tw = list()
current_line = 1
with open(input_dataset) as tsvfile:
  tsvreader = csv.reader(tsvfile, delimiter="\t")

  if current_line == 1:
    filtered_tw.append(linecache.getline(input_dataset, current_line))

    for line in tsvreader:
      if line[3] == "en" and line[4] == "US":
        filtered_tw.append(linecache.getline(input_dataset, current_line))
      current_line += 1

print('\033[1mShowing first 5 tweets from the filtered dataset\033[0m')
print(filtered_tw[1:(6 if len(filtered_tw) > 6 else len(filtered_tw))])

with open(output_dataset, 'w') as f_output:
    for item in filtered_tw:
        f_output.write(item)