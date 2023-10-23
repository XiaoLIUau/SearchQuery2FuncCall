########################
### Import libraries ###
########################
import os
import gc
import time
import pandas as pd
import torch
import evaluate
import tqdm

from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer, BitsAndBytesConfig, GenerationConfig, TrainingArguments, Trainer
from peft import PeftModel, LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
# Package name SearchQuery2FuncCall needed for import in colab
from SearchQuery2FuncCall.setup_dataset import text2json, load_n_process_data
from datasets import DatasetDict, Dataset
from trl import SFTTrainer



########################################
### Setup for Check Model Parameters ###
########################################
### Funciton to print number of trainable mode parameters
def print_number_of_trainable_model_parameters(model):
  trainable_model_params = 0
  all_model_params = 0
  for _, param in model.named_parameters():
      all_model_params += param.numel()
      if param.requires_grad:
          trainable_model_params += param.numel()
  return f"trainable model parameters: {trainable_model_params}\nall model parameters: {all_model_params}\npercentage of trainable model parameters: {100 * trainable_model_params / all_model_params:.2f}%"



##################################
### Setup for Model Generation ###
##################################
# define prompt format
def create_prompt(input):
  input_prompt = 'Input:'
  output_prompt = ', Output:'
  instruction = f"""Instruction: Given a search query, then route to different backend components based on the search intent.
1. If the search is about unit conversion, return API function UnitConvert(SourceUnit, TargetUnit, SourceValue).
2. If the search is about calculation, return API function Calculate(Equation).
3. If the search is about other search intent, return API function Search().
* For unit conversion: common unit conversion in length, mass, time, area, speed, temperature, volume should be covered. And it should be consistent for the same unit throughout. E.g. it should always be “foot”, it cannot be “feet” or “ft” in API calls.
* For calculation: common operation such as +, -, *, /, pow, log, ln, exp, tan(h), sin(h), cos(h), factorial should be covered. And it should be consistent for the same operation throughout. E.g. it should always be “ * ”, it cannot be “x” or “X” in API calls.
Handle input queries in different language styles. Cover common unit conversion and calculation operations.

"""
  prompt = instruction + input_prompt + f'“{input}”' + output_prompt
  return prompt

# Generate response in tokens with given model and tokenized input
def model_generate(input,model,tokenizer):
  generation_config = model.generation_config
  generation_config.max_new_tokens = 100
  generation_config.temperature = 0.00000000000001
  generation_config.top_p = 0.9
  generation_config.num_return_sequences = 1
  generation_config.pad_token_id = tokenizer.eos_token_id
  generation_config.eos_token_id = tokenizer.eos_token_id
  return model.generate(
          input_ids = input.input_ids,
          attention_mask = input.attention_mask,
          generation_config = generation_config,
          )

# Generate Text with selected model and input text
def generated_text(input,model,tokenizer):
  prompt = create_prompt(input)
  inputs = tokenizer(prompt, return_tensors='pt')
  generated = tokenizer.decode(
      model_generate(inputs,model,tokenizer)[0],
      skip_special_tokens=True
  )
  return generated

# Post generation string processing
def extractOutputString(input_string,output_string):
  import re
  # Use regular expressions to find the matching output for the input query
  output_match = re.search(rf'Input:\s*“{re.escape(input_string)}”\s*,\s*Output:\s*(.*?)(\[\/|$)', output_string, flags=re.MULTILINE)

  # Extract and print the output
  if output_match:
      output_string = output_match.group(1)

  # Remove quotation marks
  prefixes = ['“', '”', "'", '"', '[', '.', ']']
  if output_string.startswith(tuple(prefixes)):
      output_string = output_string[1:]
  while output_string.endswith(tuple(prefixes)):
      output_string = output_string[:-1]
  # Remove all space in output
  output_string = "".join(output_string.split())
  return output_string



############################
### Setup for Model Test ###
############################
## Test model output and dataset evaluation using ROUGE and BLEU scores
def generate_samples(example_indices,dataset,model,tokenizer):
    dash_line = '-'.join('' for x in range(100))

    for i, index in enumerate(example_indices):
        input = dataset['test'][index]['input']
        output = dataset['test'][index]['output']

        generated = generated_text(input,model,tokenizer)
        generated = extractOutputString(input,generated)

        print(dash_line)
        print('Example ', i + 1)
        print(dash_line)
        print(f'INPUT:\n{input}')
        print(dash_line)
        print(f'BASELINE OUTPUT:\n{output}')
        print(dash_line)
        print(f'PEFT MODEL GENERATION - OUTPUT:\n{generated}\n')
    return


def generate_dataset(start_index,dataset,model,tokenizer):
    end_index=start_index+len(dataset['test'])
    inputs = dataset['test'][start_index:end_index]['input']
    outputs = dataset['test'][start_index:end_index]['output']

    outputs_gen = []

    for idx, input in enumerate(inputs):
        if idx%10==0:
            print(idx)
        output_gen = generated_text(input,model,tokenizer)
        output_gen = extractOutputString(input,output_gen)
        outputs_gen.append(output_gen)

    zipped_summaries = list(zip(inputs, outputs, outputs_gen))
    df = pd.DataFrame(zipped_summaries, columns = ['Inputs', 'Outputs', 'Outputs_generated'])
    return df


def evaluate_generations(outputs_ref,outputs_gen):
    # Rouge
    rouge = evaluate.load('rouge')
    model_results = rouge.compute(
        predictions=outputs_gen,
        references=outputs_ref,
        use_aggregator=True,
        use_stemmer=True,
    )

    print('MODEL ROUGE SCORES:')
    print(model_results)

    # bleu
    bleu = evaluate.load('bleu')
    model_results = bleu.compute(
        predictions=outputs_gen,
        references=outputs_ref,
    )

    print('MODEL BLEU SCORES:')
    print(model_results)
    return
