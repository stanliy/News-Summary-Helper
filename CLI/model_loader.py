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

def insert_summary_to_mysql(category, url, title_summary, body_summary, article_date):
    import pymysql
    import os
    conn = pymysql.connect(
        host=os.getenv("ODB_HOST"),
        user=os.getenv("DB_NAME"),
        password=os.getenv("ODB_PASSWORD"),
        database=os.getenv("DB_NAME"),

        charset='utf8mb4',
        autocommit=True
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_summary (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(50),
            url TEXT,
            title_summary TEXT,
            body_summary TEXT,
            article_date DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    sql = """
        INSERT INTO news_summary (category, url, title_summary, body_summary, article_date)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (category, url, title_summary, body_summary, article_date))

    cursor.close()
    conn.close()