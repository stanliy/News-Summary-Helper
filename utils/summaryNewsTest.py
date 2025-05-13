import torch
from transformers import pipeline    # 영어 기사 요약
from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast  # 한국어 기사 요약


def summary_news(text, lang, len_min, len_max):

    if lang == 'en':    # 감지된 언어 영어 -> 영어 요약문 생성
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary_eng = summarizer(text, max_length=len_max, min_length=len_min, do_sample=False)
        summary = summary_eng[0]['summary_text']

    elif lang == 'ko':  # 감지된 언어 한국어 -> 한국어 요약문 생성
        sum_tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-summarization')
        sum_model = BartForConditionalGeneration.from_pretrained('gogamza/kobart-summarization')

        raw_input_ids = sum_tokenizer.encode(text)
        input_ids = [sum_tokenizer.bos_token_id] + raw_input_ids + [sum_tokenizer.eos_token_id]

        summary_ids = sum_model.generate(
            torch.tensor([input_ids]),
            max_length=len_max,
            min_length=len_min,
            num_beams=5,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
            early_stopping=True
        )
        summary_ko = sum_tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)
        summary = summary_ko.replace('\n', ' ').strip()
    elif not lang:      # 언어 감지에 실패한 경우
        summary = "error1"
    else:               # 감지된 언어가 영어나 한국어가 아닐 경우 (ex. 일본어, 중국어 등)
        summary = "error2"

    return summary


def decide_summary_len(lang, length_type):
    length_range_ko = {        # 한국어 요약문 길이 범위 제한
        'short': {'min': 64, 'max': 160},
        'medium': {'min': 128, 'max': 256},
        'long': {'min': 256, 'max': 320},
    }

    length_range_en = {        # 영어 요약문 길이 범위 제한
        'short': {'min': 32, 'max': 48},
        'medium': {'min': 48, 'max': 64},
        'long': {'min': 64, 'max': 96},
    }

    if lang == 'ko':
        return length_range_ko.get(length_type)
    else:
        return length_range_en.get(length_type)
