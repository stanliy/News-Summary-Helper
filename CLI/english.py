from . import model_loader

summarizer = model_loader.load_bart_large_cnn()
tokenizer3, model3, device = model_loader.load_t5_headline_gen()

def summarize_bart_pipeline(text: str) -> str:
    result = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return result[0]['summary_text']

def generate_english_headline(summary_text: str) -> str:
    input_text = "headline: " + summary_text.strip()
    inputs = tokenizer3.encode(
        input_text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(device)

    output_ids = model3.generate(
        inputs,
        max_length=32,
        num_beams=5,
        repetition_penalty=1.2,
        length_penalty=0.9,
        early_stopping=True
    )
    return tokenizer3.decode(output_ids[0], skip_special_tokens=True)
