from SearchQuery2FuncCall.setup_dataset import text2json, load_n_process_data
from huggingface_hub import login

####################################
### Load Datasets and Get Access ###
####################################
text2json('/content/SearchQuery2FuncCall/Dataset.txt')
# q2f_datasets = load_n_process_data('/content/non_search_examples.json')
q2f_datasets = load_n_process_data('/content/q2f_dataset.json')
print(q2f_datasets)


# # Load Huggingface API key
# Here we use Huggingface models
# Note: Please load a text file that contains your model api key to current folder
# >Name your file in either ***'api_key_huggingface.txt'***

### Access Huggingface for loading model
""" # Get model api key """
def load_api_key_from_file(file_path):
  with open(file_path, 'r') as file:
      api_key = file.read().strip()
  return api_key
# # Setting a new environment variable
# os.environ["HUGGINGFACE_TOKEN"] = load_api_key_from_file('/content/api_key_huggingface.txt')
# !huggingface-cli login --token $HUGGINGFACE_TOKEN

HUGGINGFACE_TOKEN= load_api_key_from_file('/content/api_key_huggingface.txt')
login(token=HUGGINGFACE_TOKEN)