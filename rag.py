import vector_search
import mongo_conn
from transformers import AutoTokenizer, AutoModelForCausalLM

# Conduct query with retrieval of sources
query = "What is the best romantic movie to watch and why?"
source_information = vector_search.get_search_result(query, mongo_conn.get_mongo_coll())
combined_information = f"Query: {query}\nContinue to answer the query by using the Search Results:\n{source_information}."
print(combined_information)


tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")  # to add hf token
# CPU Enabled uncomment below 👇🏽
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it")
# GPU Enabled use below 👇🏽
# model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it", device_map="auto")
input_ids = tokenizer(
    combined_information, return_tensors="pt"
)  # .to("cuda") #cuda to be used with gpu support
response = model.generate(**input_ids, max_new_tokens=500)
print(tokenizer.decode(response[0]))
