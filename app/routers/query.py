from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from langchain.document_loaders import JSONLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from app.models.query_model import QueryModel
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import json

env = json.load(open("env.json"))
route = APIRouter()

@route.post("/process")
async def process(body: QueryModel):
  loader = JSONLoader(
    file_path="app/data/example.json",
    jq_schema=".QA[]",
    text_content=False
  )
  data = loader.load()
  embeddings = OpenAIEmbeddings(openai_api_key=env["OPENAI_API_KEY"])
  db = FAISS.from_documents(data, embeddings)
  docs = db.similarity_search(body.query)
  chain = load_qa_chain(OpenAI(temperature=0.7, openai_api_key=env["OPENAI_API_KEY"]), chain_type="stuff")
  res = chain.run(input_documents=docs, question=body.query)
  return {"result": res.strip()}
