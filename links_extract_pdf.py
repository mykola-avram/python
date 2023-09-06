import pikepdf 
import PyPDF2
import re
pdf_file = open("file.pdf", 'rb')
import PyPDF2

import PyPDF2
import requests
from selenium import webdriver

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

# Function to check the validity of a URL using Selenium
def is_url_valid_with_selenium(url):
    try:
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        
        driver.get(url)
        
        # Check if the page loaded successfully (you can modify this check as needed)
        if "Amazon.com" in driver.title:
            return True
        
        return False
    except Exception as e:
        print(e)
        return False
    finally:
        driver.quit()

# Create a PDF reader object
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Loop through each page in the PDF
for page_num in range(pdf_reader.getNumPages()):
    page = pdf_reader.getPage(page_num)
    page_links = extract_links(page)
    
    if page_links:
        for link in page_links:
            print(f'Page {page_num + 1}: {link}')
            if "amazon.com" in link.lower():
                is_valid = is_url_valid_with_selenium(link)
                if is_valid:
                    print('  This link is valid and exists on the internet.')
                else:
                    print('  This link is invalid or does not exist on the internet (Amazon page).')
            else:
                if requests.get(link).status_code == 200:
                    print('  This link is valid and exists on the internet.')
                else:
                    print('  This link is invalid or does not exist on the internet.')

# Close the PDF file
pdf_file.close()

