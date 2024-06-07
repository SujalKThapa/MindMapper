import pymupdf
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def returnText(fileName):
    pdfDocument = pymupdf.open(fileName)
    extractedText = []
    for pageNum in range(pdfDocument.page_count):
        page = pdfDocument.load_page(pageNum)
        text = page.get_text()
        extractedText.append(text)
    extractedText.remove("")
    print(extractedText)


if __name__ == '__main__':
    returnText("Placeholder.pdf")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
