from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_name_or_path = "sberbank-ai/rugpt3large_based_on_gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
model = GPT2LMHeadModel.from_pretrained(model_name_or_path).to(DEVICE)

while True:
    inputText = input("Input: ")
    if inputText == "0":
        break
    else:
        input_ids = tokenizer.encode(inputText, return_tensors="pt").to(DEVICE)
        out = model.generate(input_ids, do_sample=False)
        generated_text = list(map(tokenizer.decode, out))[0]
        print("Output: ", generated_text)
