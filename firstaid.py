from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader ,TextLoader
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
import os 
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from ai71 import AI71
import json


AI71_API_KEY = os.getenv('AI71_API_KEY')



class HRChatBot:
    def __init__(self, directory='doc', embeddings_model="sentence-transformers/all-mpnet-base-v2", persist_directory="chroma_db"):
        self.directory = directory
        self.embeddings = HuggingFaceBgeEmbeddings(
                        model_name=embeddings_model,  # alternatively use "sentence-transformers/all-MiniLM-l6-v2" for a light and faster experience.
                        model_kwargs={'device':'cpu'}, 
                        encode_kwargs={'normalize_embeddings': True}
                            )
        self.persist_directory = persist_directory
        self.vectordb = None

    def load_docs(self):
        loader = DirectoryLoader(self.directory)
        documents = loader.load()
        return documents

    def split_docs(self, documents, chunk_size=500, chunk_overlap=20):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents(documents)
        return docs

    def process_docs(self):
        documents = self.load_docs()
        docs = self.split_docs(documents)
        self.vectordb = Chroma.from_documents(documents=docs, embedding=self.embeddings, persist_directory=self.persist_directory)
        print("Database created.")

    def load_database(self):
        self.vectordb = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)

    def update_database(self, text_file):
        if self.vectordb is None:
            self.load_database()
        loader = TextLoader(text_file)
        documents = loader.load()
        self.vectordb.add_texts(texts=documents, embedding=self.embeddings)
        self.vectordb.persist()
        print("Database updated.")


def check_folder_exists(parent_folder):
    folder_name = "chroma_db" #chroma_db
    folder_path = os.path.join(parent_folder, folder_name)
    # print("Checking folder path:", folder_path)  # Add this line for debugging
    return os.path.exists(folder_path) and os.path.isdir(folder_path)


def qna_bot(query):
    current_folder = os.getcwd()
    if check_folder_exists(current_folder):
        print("Vector Database Folder found")
        Tut_bot = HRChatBot()
        Tut_bot.load_database()
        retrieve = Tut_bot.vectordb.similarity_search(query)
        # print(Tut_bot.vectordb.similarity_search(query))
        # print()
        # print(len(retrieve))
        ans =[]
        for i in range(len(retrieve)):
            ans.append(retrieve[i].page_content)
        # print()
        print(ans)
        return  json.dumps(ans)
    else:
        print("I got a cut in my hand ")
        Tut_bot = HRChatBot()
        Tut_bot.process_docs()
        retrieve = Tut_bot.vectordb.similarity_search(query)
        # print(Tut_bot.vectordb.similarity_search(query))
        # print()
        # print(len(retrieve))
        ans =[]
        for i in range(len(retrieve)):
            ans.append(retrieve[i].page_content)
        # print()
        # print(ans)
        return  json.dumps(ans)


# print(qna_bot("My friend is feeling faintish "))