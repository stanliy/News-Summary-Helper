import torch
from . import model_loader

tokenizer, model = model_loader.load_kobart_summarizer()
tokenizer2, model2 = model_loader.load_kobart_headline_gen()

def summarize_korean(text: str) -> str:
    # 입력 토큰 변환
    input_ids = [tokenizer.bos_token_id] + tokenizer.encode(text) + [tokenizer.eos_token_id]
    input_len = len(input_ids)

    # 사전 정의된 최대 입력 길이 (BART 기반 모델은 보통 1024)
    MAX_INPUT_LEN = 1024

    # 예외 처리: 입력이 너무 짧은 경우 요약 생략
    if input_len < 30:
        return text.strip()

    # 긴 입력 잘라내기
    if input_len > MAX_INPUT_LEN:
        input_ids = input_ids[:MAX_INPUT_LEN]
        input_len = MAX_INPUT_LEN

    # 비율 기반 max_length 설정: 20~25% 비율 (클수록 요약 결과가 풍부함)
    raw_output_len = int(input_len * 0.5)

    # 최소·최대 길이 범위 지정
    max_output_len = max(48, min(raw_output_len, 200))
    min_output_len = int(max_output_len * 0.6) 

    # 요약 생성
    summary_ids = model.generate(
        torch.tensor([input_ids]),
        max_length=max_output_len,
        min_length = min_output_len,  # 요약 결과가 너무 짧지 않게 보장
        num_beams=4, #더 다양한 후보 문장 비교
        early_stopping=False, #필요 이상으로 길게 생성되지 않도록 중단
        no_repeat_ngram_size=3,#반복 방지
        length_penalty=1.2 #너무 짧은 요약 방지
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def generate_korean_headline(summary_text: str) -> str:
    """
    요약문을 입력받아 자연스러운 뉴스 제목을 생성하는 함수
    """
    # 입력 텍스트를 토큰화
    inputs = tokenizer2(summary_text, return_tensors="pt", padding=True, truncation=True,max_length=128)

    # 모델로 제목 생성
    summary_ids = model2.generate(
        inputs.input_ids,
        max_length=25,
        min_length=8,
        num_beams=4,
        repetition_penalty=1.2,
        length_penalty=1.1,
        early_stopping=True,
        
        )
    return tokenizer2.decode(summary_ids[0], skip_special_tokens=True)
