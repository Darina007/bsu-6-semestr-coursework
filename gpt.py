from datetime import datetime

import numpy as np
import torch
from transformers import (GPT2LMHeadModel, GPT2Tokenizer)

import config
import historyUtils
import utils


device = torch.device("cuda" if torch.cuda.is_available() and not config.no_cuda else "cpu")
model_type = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(config.model)
model = GPT2LMHeadModel.from_pretrained(config.model)
model.to(device)


def set_seed(seed=datetime.now().microsecond):
    np.random.seed(seed)
    torch.manual_seed(seed)
    print("random seed is " + str(seed))
    if not config.no_cuda and torch.cuda.device_count() > 0:
        torch.cuda.manual_seed_all(seed)


set_seed(config.seed if hasattr(config, 'seed') else set_seed.__defaults__[0])


def create_chat_answer(prompt_text):
    prepared_text = historyUtils.user_based_dialog_former(prompt_text)
    print(prepared_text)
    encoded_prompt = tokenizer.encode(prepared_text,
                                      add_special_tokens=False,
                                      return_tensors="pt")
    encoded_prompt = encoded_prompt.to(device)
    output_sequences = model.generate(
        input_ids=encoded_prompt,
        max_length=config.length + len(encoded_prompt[0]),
        temperature=config.temperature,
        top_k=config.kvalue,
        top_p=config.pvalue,
        repetition_penalty=config.repetition_penalty,
        do_sample=True,
        num_return_sequences=1,
    )
    if len(output_sequences.shape) > 2:
        output_sequences.squeeze_()
    for generated_sequence_idx, generated_sequence in enumerate(
            output_sequences):
        generated_sequence = generated_sequence.tolist()
        text = tokenizer.decode(generated_sequence,
                                clean_up_tokenization_spaces=True)
        text = text[:text.find(config.stop_token) if config.stop_token else None]
        total_sequence = (
            text[len(
                tokenizer.decode(encoded_prompt[0],
                                 clean_up_tokenization_spaces=True)):].rsplit(' ', 1)[0])
        total_sequence = utils.cut_extra_stuff(total_sequence)
        result_text = historyUtils.historic_response_parser(
            total_sequence,
            prompt_text.chat.id)
        print("GPT: " + result_text)
        return result_text


def fill_sentence(message):
    input_ids = tokenizer.encode(message, return_tensors="pt").to(device)
    out = model.generate(input_ids, do_sample=False)
    return list(map(tokenizer.decode, out))[0]
