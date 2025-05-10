from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast


def summaryNews(text):

    model = BartForConditionalGeneration.from_pretrained('gogamza/kobart-summarization')
    tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-summarization')

    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(
        inputs['input_ids'],
        max_length=128,
        min_length=30,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    print("요약:", summary)
    return summary

