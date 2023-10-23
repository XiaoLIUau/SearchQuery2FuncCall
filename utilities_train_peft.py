from datasets import DatasetDict
# Package name SearchQuery2FuncCall needed for import in colab
from SearchQuery2FuncCall.utilities_main import print_number_of_trainable_model_parameters

##########################
### Setup for Training ###
##########################

### Prepare for training dataset
def create_prompt_training(input,output):
    input_prompt = 'Input:'
    output_prompt = ', Output:'
    start_prompt = '<s>[INST] '
    end_prompt = '[/INST]'
    instruction = f"""Instruction: Given a search query, then route to different backend components based on the search intent.
1. If the search is about unit conversion, return API function UnitConvert(SourceUnit, TargetUnit, SourceValue).
2. If the search is about calculation, return API function Calculate(Equation).
3. If the search is about other search intent, return API function Search().
* For unit conversion: common unit conversion in length, mass, time, area, speed, temperature, volume should be covered. And it should be consistent for the same unit throughout. E.g. it should always be “foot”, it cannot be “feet” or “ft” in API calls.
* For calculation: common operation such as +, -, *, /, pow, log, ln, exp, tan(h), sin(h), cos(h), factorial should be covered. And it should be consistent for the same operation throughout. E.g. it should always be “ * ”, it cannot be “x” or “X” in API calls.
Handle input queries in different language styles. Cover common unit conversion and calculation operations.

"""

    prompt = start_prompt + instruction + input_prompt + f'“{input}”' + output_prompt + f'“{output}”' + end_prompt
    return prompt

# Examples:
# {input_prompt}“ft to cm”{output_prompt}“UnitConvert(SourceUnit:foot, TargetUnit:centimeter,
# SourceValue:1)”
# {input_prompt}“how many ounces in 5.8 kilograms”{output_prompt}“UnitConvert(SourceUnit:kilogram,
# TargetUnit:ounce, SourceValue:5.8)”
# {input_prompt}“two to the power of 10”{output_prompt}“Calculate(2^10)”
# {input_prompt}“2001-1989” {output_prompt}“Calculate(2001-1989)”
# {input_prompt}“what is chatgpt”{output_prompt}“Search()”
# {input_prompt}“primary year 1 maths calculation checklist”{output_prompt}“Search()”
# {input_prompt}“what are different length units”{output_prompt}“Search()”
# {input_prompt}“Natural logarithm of -3/18”{output_prompt}“Calculate(ln(-3/18))”
# {input_prompt}“what is tan of 3/4”{output_prompt}“Calculate(tan(3/4))”


### Tokenize the datasets for Trainer
def tokenize_datasets(datasets,tokenizer):
  def tokenize_function(example):
      prompt = [create_prompt_training(input) for input in example["input"]]
      example['input_ids'] = tokenizer(prompt, padding="max_length", truncation=True, return_tensors="pt").input_ids
      example['labels'] = tokenizer(example["output"], padding="max_length", truncation=True, return_tensors="pt").input_ids
      return example
  # The dataset actually contains 3 diff splits: train, validation, test.
  # The tokenize_function code is handling all data across all splits in batches.
  tokenized_datasets = datasets.shuffle().map(tokenize_function, batched=True)
  tokenized_datasets = tokenized_datasets.remove_columns(['input', 'output'])
  return tokenized_datasets


### Add text variable to datasets for SFTTrainer
def create_text_datasets(example):
    # Define your custom processing logic here
    prompt_text = create_prompt_training(example['input'], example['output'])
    return {"text": prompt_text}
def process_dataset_dict(dataset_dict, processing_function):
    processed_dict = DatasetDict()
    for split_key, split_data in dataset_dict.items():
        processed_data = split_data.map(processing_function)
        processed_dict[split_key] = processed_data
    return processed_dict


# Iterate over your training set and calculate the length of each sequence.
# For example, you can use the following code:
def get_max_seq_length(dataset):
    max_seq_length = 0
    for sequence in dataset['train']:
        text_len = len(sequence['text'])
        if text_len > max_seq_length:
            max_seq_length = text_len
    return max_seq_length+100


### Prepare model for training
# Freeze all parameters
def freeze_all_parameters(model):
    for param in model.parameters():
        param.requires_grad = False
    print('\n### After freeze all parameters: ###')
    print(print_number_of_trainable_model_parameters(model))
    return
