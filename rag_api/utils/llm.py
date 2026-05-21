from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM
from transformers import pipeline

from langchain_community.llms import HuggingFacePipeline

model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=50,
temperature=0.1
)

llm = HuggingFacePipeline(pipeline=pipe)