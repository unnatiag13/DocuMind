from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load https://huggingface.co/sentence-transformers/all-mpnet-base-v2
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode([
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
])
# similarities = cosine_similarity(embeddings, embeddings)
# similarities = model.similarity(embeddings, embeddings)
# print(embeddings)
print(type(model.encode("hello")))














# import fitz 
# pdf_document = fitz.open('uploads/24035c19-d1e3-4fb7-87dc-7f95231d33a0_UnnatiAgarwal_.pdf')
# # Number of pages
# num_pages = pdf_document.page_count
# print(f'The document has {num_pages} pages.')

# # Metadata
# metadata = pdf_document.metadata
# print('Metadata:', metadata)

# page_number = 0
# page = pdf_document.load_page(page_number)

# # Extract text
# text = page.get_text("blocks")
# print(len(text))

# abc ="Hello i am unnati" 
# print(len(abc))
