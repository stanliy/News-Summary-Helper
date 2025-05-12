import torch
from transformers import PreTrainedTokenizerFast                  # 한국어 제목
from transformers import BartForConditionalGeneration             # 한국어 제목
from transformers import T5ForConditionalGeneration, T5Tokenizer  # 영어 제목


def generate_title(text, lang):
    if text == "error1" or "error2":  # 요약 실패
        headline = None

    if lang == 'en':                  # 감지된 언어 영어 -> 영어 제목 생성
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model = T5ForConditionalGeneration.from_pretrained("Michau/t5-base-en-generate-headline")
        tokenizer = T5Tokenizer.from_pretrained("Michau/t5-base-en-generate-headline")
        model = model.to(device)

        article = "headline: " + text

        encoding = tokenizer.encode_plus(article, return_tensors="pt")
        input_ids = encoding["input_ids"].to(device)
        attention_masks = encoding["attention_mask"].to(device)

        headline_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_masks,
            max_length=64,
            num_beams=3,
            early_stopping=True,
        )
        headline = tokenizer.decode(headline_ids[0], skip_special_tokens=True)
    elif lang == 'ko':                # 감지된 언어 한국어 -> 한국어 제목 생성
        headline_model = BartForConditionalGeneration.from_pretrained('yebini/kobart-headline-gen')
        headline_tokenizer = PreTrainedTokenizerFast.from_pretrained('yebini/kobart-headline-gen')

        inputs = headline_tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        headline_ids = headline_model.generate(
            inputs.input_ids,
            max_length=64,
            num_beams=5,
            repetition_penalty=1.2,
            length_penalty=0.8,
            early_stopping=True)

        headline = headline_tokenizer.decode(headline_ids[0], skip_special_tokens=True)

    return headline
