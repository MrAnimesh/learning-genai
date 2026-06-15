from pypdf import PdfReader

# Text extraction from PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)

    text = []
    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)
    
    return "\n".join(text)

# print(extract_text_from_pdf("../uploads/solo_leveling.pdf"))
def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - chunk_overlap
        # print(chunks)
        # print()
    
    return chunks

# text = extract_text_from_pdf("../uploads/solo_leveling.pdf")