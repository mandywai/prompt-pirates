from pypdf import PdfReader

def pdf_reader(pdf_file_path):
  pdf_file_path=r'/content/Nelson-Physics-11.pdf'
  # Create a PdfReader object
  reader = PdfReader(pdf_file_path)

  # You can now access PDF properties and content
  num_pages = len(reader.pages)
  print(f"Number of pages: {num_pages}")

  # To extract text from a specific page (e.g., the first page):
  # first_page = reader.pages[0]
  # page_text = first_page.extract_text()
  num_pages = 2
  documents = []
  for ind in range(num_pages):
    page = reader.pages[ind]
    text = page.extract_text()
    if text:
      documents.append(text)
  return documents