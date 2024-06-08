import pymupdf
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(os.environ['GOOGLE_API_Key'])

def generateData(extractedText):
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    messages = [SystemMessage(
        content="Generate a title for this data, classify the data into sections as you see fit (and if the subject matter is really complex, into sub-sections) with summaries for the bottom level section/subsection. For ex:\n## Title: <Title>\n**Section: <Section Name>**\n Summary: <Section Summary>.\n**Section: <Section Name>**\nSummary: <Section Summary>\nSub-Section: <Subsection Name> \nSummary: <Subsection Summary> \n Sub-Section: <Subsection Name> \nSummary: <Subsection Summary> \n**Section: <Section Name>**\nSummary: <Section Summary>\n"),
        HumanMessage(content=extractedText)
    ]
    result = model.invoke(messages)
    parser = StrOutputParser()
    return parser.invoke(result)

def returnText(fileName):
    pdfDocument = pymupdf.open(fileName)
    extractedText = []
    for pageNum in range(pdfDocument.page_count):
        page = pdfDocument.load_page(pageNum)
        text = page.get_text()
        extractedText.append(text)
    extractedText.remove("")
    fullText = "\n".join(extractedText)
    return generateData(fullText)


if __name__ == '__main__':
    print(os.environ['GOOGLE_API_key'])
    responseText = returnText("Placeholder.pdf")
    print(responseText)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
