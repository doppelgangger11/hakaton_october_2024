import torch
from transformers import GPT2Tokenizer, T5ForConditionalGeneration 
tokenizer = GPT2Tokenizer.from_pretrained('RussianNLP/FRED-T5-Summarizer',eos_token='</s>')
model = T5ForConditionalGeneration.from_pretrained('RussianNLP/FRED-T5-Summarizer')
device='cuda'
model.to(device)

input_text='<LM> Сократи текст.\n В деревне, затерянной среди зелёных холмов, жил старик по имени Иван. Его жизнь протекала медленно и размеренно. Каждое утро Иван выходил на поля, чтобы заботиться о своём скромном участке земли. Он выращивал картофель и морковь, которые были его главным источником пищи. Вечера старик проводил у камина, читая книги и вспоминая молодость. Жизнь в деревне была тяжёлая, но Иван находил в ней простые радости.'
input_ids=torch.tensor([tokenizer.encode(input_text)]).to(device)
outputs=model.generate(input_ids,eos_token_id=tokenizer.eos_token_id,
                    num_beams=5,
                    min_new_tokens=17,
                    max_new_tokens=200,
                    do_sample=True,
                    no_repeat_ngram_size=4,
                    top_p=0.9)
print(tokenizer.decode(outputs[0][1:]))