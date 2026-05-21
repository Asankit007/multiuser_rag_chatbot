# from transformers import AutoTokenizer
# from transformers import AutoModelForSeq2SeqLM
# from transformers import pipeline

# from langchain_community.llms import HuggingFacePipeline

# model_name = "google/flan-t5-small"

# tokenizer = AutoTokenizer.from_pretrained(model_name)

# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# pipe = pipeline(
#     "text2text-generation",
#     model=model,
#     tokenizer=tokenizer, 
#     max_new_tokens=50,
# temperature=0.1
# )

# llm = HuggingFacePipeline(pipeline=pipe)


from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.1,
    max_tokens=100
)