from glob import glob
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import MarkdownTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
import pymupdf4llm
load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

db = Chroma(
  embedding_function=embeddings,
  persist_directory='./data/chroma_final',
  collection_metadata={"hnsw:space": "cosine"}
)

pymupdf4llm.use_layout(False)

if db._collection.count() == 0:
  print('\nChroma-ing\n')
  docs = []

  for pdf in glob('./data/docs/*.pdf'):
    pages = pymupdf4llm.to_markdown(
      pdf,
      page_chunks=True,
      write_images=True,
      image_path='./data/images',
      image_size_limit=0.2
    )
    for page in pages:
      docs.append(Document(
        page_content=page['text'],
        metadata=page['metadata']
      ))
  
  splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
  chunks = splitter.split_documents(docs)
  db.add_documents(chunks)

retriever = db.as_retriever(search_kwargs={'k': 5})

llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.2)

with open('./data/prompt.txt', 'r') as f:
  system_prompt = f.read()

prompt = ChatPromptTemplate.from_messages([
  ('system', system_prompt),
  ('human', '{input}')
])

def query(inputquery):
  chunks = retriever.invoke(inputquery)
  proper_chunks = []

  for chunk in chunks:
    src = chunk.metadata['file_path']
    file = src.split('\\')[-1]
    name = file.split('.')[0]
    chunk = f'Source: {name}\nContent: {chunk.page_content}'
    proper_chunks.append(chunk)

  context = '\n-----\n'.join(proper_chunks)
  prompted_context = prompt.invoke({'context': context, 'input': inputquery})
  answer = llm.invoke(prompted_context)
  
  return answer.content