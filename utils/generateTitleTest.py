import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration


def generateTitle(text):

    model = BartForConditionalGeneration.from_pretrained('yebini/kobart-headline-gen')
    tokenizer = PreTrainedTokenizerFast.from_pretrained('yebini/kobart-headline-gen')

    # text =  '서울 중부경찰서는 마약을 투약한 상태로 운전을 하다 교통사고를 내고 도주한 혐의로 40대 남성에 대해 구속영장을 신청했습니다. 이 남성은 지난 5일 오전 6시 15분쯤 서울 중구 광희동의 한 도로에서 마약을 투약한 상태로 고급 외제차를 몰다 신호 대기 중인 차량 2대를 들이받은 뒤 도주한 혐의를 받고 있습니다. 이 남성은 사고 직후 2백 미터가량 달아났다 다시 현장으로 돌아와 경찰에 자수했으며, 마약 간이 시약 검사에선 대마 양성 반응이 나온 걸로 파악됐습니다. 남성이 들이받은 차량에 타고 있던 운전자들은 크게 다치지는 않은 걸로 전해졌으며, 경찰은 남성의 소변과 모발을 국립과학수사연구원에 보내 정밀 감정을 의뢰하고 자세한 경위를 조사하고 있습니다.'

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    summary_ids = model.generate(inputs.input_ids, max_length=64, num_beams=5, repetition_penalty=1.2, length_penalty=0.8, early_stopping=True)

    title = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    print("제목:", title)
    return title

