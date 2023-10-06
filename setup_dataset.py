import re
import json
from datasets import load_dataset

# Function to parse input and output from a line
def parse_line(line):
    match = re.match(r'Input: "(.*?)"; Output: "(.*?)"', line)
    if match:
        input_text = match.group(1)
        output_text = match.group(2)
        return {"input": input_text, "output": output_text}
    else:
        return None

def text2json(path):
    # Read the text file
    # path example: '/content/SearchQuery2FuncCall/Dataset.txt'
    with open(path, 'r') as file: 
        lines = file.readlines()

    # Parse the lines into input-output pairs
    data = [parse_line(line) for line in lines]
    # Filter out any None entries (lines that couldn't be parsed)
    data = [entry for entry in data if entry is not None]

    # Save the data as a JSON file
    with open('q2f_dataset.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)
    print(f"Saved {len(data)} examples to 'q2f_dataset.json'.")


    ## Initialize two empty lists for the separate datasets
    search_examples = []
    non_search_examples = []

    # Iterate through the dataset and separate examples
    for example in data:
        if example['output'] == "Search()":
            example['Search']=1
            search_examples.append(example)
        else:
            example['Search']=0
            non_search_examples.append(example)

    # Save the separated datasets as JSON files
    with open('search_examples.json', 'w') as json_file:
        json.dump(search_examples, json_file, indent=2)

    with open('non_search_examples.json', 'w') as json_file:
        json.dump(non_search_examples, json_file, indent=2)

    print(f"Separated {len(search_examples)} Search() examples to 'search_examples.json'.")
    print(f"Separated {len(non_search_examples)} non-Search() examples to 'non_search_examples.json'.")
    return


def load_n_process_data(path):
    dataset = load_dataset('json', data_files=path) #e.g. path = '/content/non_search_examples.json' or '/content/q2f_dataset.json'
    q2f_datasets=dataset.shuffle(seed=42)

    datasets_train_test = q2f_datasets["train"].train_test_split(test_size=80)
    datasets_train_validation = datasets_train_test["train"].train_test_split(test_size=50)

    q2f_datasets["train"] = datasets_train_validation["train"]
    q2f_datasets["validation"] = datasets_train_validation["test"]
    q2f_datasets["test"] = datasets_train_test["test"]
    return q2f_datasets