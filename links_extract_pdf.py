import pikepdf 
import PyPDF2
import re
pdf_file = open("C:/Users/mavram/Downloads/Power BI Training Instruction_Edited.pdf", 'rb')
import PyPDF2

import PyPDF2
import requests
from tabulate import tabulate

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

# Function to check the validity of a URL by making a GET request
def is_url_valid(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

# Initialize a list to store the results
results = []

# Loop through each page in the PDF
for page_num in range(pdf_reader.getNumPages()):
    page = pdf_reader.getPage(page_num)
    page_links = extract_links(page)
    
    if page_links:
        for link in page_links:
            print(f'Page {page_num + 1}: {link}')
            if is_url_valid(link):
                print('  This link is valid and exists on the internet.')
            else:
                print('  This link is invalid or does not exist on the internet.')

            link_status = "Valid" if is_url_valid(link) else "Invalid"
            results.append([f'Page {page_num + 1}', link, link_status])

# Close the PDF file
pdf_file.close()

# Display the results as a table
table_headers = ["Page Number", "Link", "Status"]
print(tabulate(results, headers=table_headers, tablefmt="pretty"))
