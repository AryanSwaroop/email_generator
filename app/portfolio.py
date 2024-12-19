import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):

        self.file_path = file_path  # Save the path to the portfolio CSV file
        self.data = pd.read_csv(file_path)  # Load the portfolio data from the CSV file into a pandas DataFrame
        self.chroma_client = chromadb.PersistentClient('vectorstore')  # Initialize a persistent ChromaDB client
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")  # Create or fetch a collection named "portfolio"

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
