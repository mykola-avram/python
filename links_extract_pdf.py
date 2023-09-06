import pikepdf 
import PyPDF2
import re
pdf_file = open("C:/Users/mavram/Downloads/Power BI Training Instruction_Edited.pdf", 'rb')
import PyPDF2

def extract_links(page):
    links = []
    if '/Annots' in page:
        annotations = page['/Annots']
        for annotation in annotations:
            annotation_object = annotation.getObject()
            if annotation_object.get('/Subtype') == '/Link':
                uri = annotation_object['/A']['/URI']
                links.append(uri)
    return links

# Create a PDF reader object
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Loop through each page in the PDF
for page_num in range(pdf_reader.getNumPages()):
    page = pdf_reader.getPage(page_num)
    page_links = extract_links(page)
    
    if page_links:
        for link in page_links:
            print(f'Page {page_num + 1}: {link}')

# Close the PDF file
pdf_file.close()
