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
        e = find_boundry(text, end)
        temp = False
        if (end - e )!= 0:
            temp = True
        chunk = text[start:abs(e)]
        chunks.append(chunk)
        to_minus = 0
        if temp == True:
            to_minus = end - e
        start += (chunk_size + to_minus) - chunk_overlap
        # print(chunks)
        # print()
        temp = False
    
    return chunks

def find_boundry(text: str, end: int):
    if end > len(text):
        return end
    if end < len(text) and text[end] in ['?','.','!']:
        return end
    
    i = 100
    e = end
    while i >= 0:
        if text[e] == '?' or text[e] == '.' or text[e] == '!':
            return e
        i -= 1
        e -= 1
    
    i = 100
    e = end
    while i >= 0:
        if text[e] == '?' or text[e] == '.' or text[e] == '!':
            return e
        i -= 1
        e += 1
    
    return end




text = extract_text_from_pdf("../uploads/solo_leveling.pdf")
print(chunk_text(text))