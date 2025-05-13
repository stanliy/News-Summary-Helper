import torch

from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

from transformers import pipeline
from transformers import T5ForConditionalGeneration,T5Tokenizer

def load_kobart_summarizer():
    tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-summarization')
    model = BartForConditionalGeneration.from_pretrained('gogamza/kobart-summarization')
    return tokenizer, model

from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

def load_kobart_headline_gen():
    tokenizer2 = PreTrainedTokenizerFast.from_pretrained(
        'gogamza/kobart-base-v2',
        bos_token='</s>',
        eos_token='</s>',
        unk_token='<unk>',
        pad_token='<pad>',
        mask_token='<mask>'
    )
    model2 = BartForConditionalGeneration.from_pretrained('yebini/kobart-headline-gen')
    return tokenizer2, model2

def load_bart_large_cnn():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return summarizer

def load_t5_headline_gen():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model3 = T5ForConditionalGeneration.from_pretrained("Michau/t5-base-en-generate-headline").to(device)
    tokenizer3 = T5Tokenizer.from_pretrained("Michau/t5-base-en-generate-headline")
    model3 = model3.to(device)
    return tokenizer3, model3, device
