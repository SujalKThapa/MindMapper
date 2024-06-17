import pymupdf
import graphviz
import os
import base64
from io import BytesIO
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
import tempfile
import logging

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(os.environ['GOOGLE_API_Key'])

def generateData(extractedText):
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    messages = [SystemMessage(
        content="Generate a title for this data, classify the data into sections as you see fit (and if the subject matter is really complex, into sub-sections) with summaries for the bottom level section/subsection. (Note: Always try to maximize the number of sub-sections and prefer summaries with a greater weight placed on the number of sub-sections rather than the number of sections) MUST FOLLOW THE FORMAT:\n## Title: <Title>\n**Section: <Section Name>**\n Summary: <Section Summary>.\n**Section: <Section Name>**\nSummary: <Section Summary>\nSub-Section: <Subsection Name> \nSummary: <Subsection Summary> \n Sub-Section: <Subsection Name> \nSummary: <Subsection Summary> \n**Section: <Section Name>**\nSummary: <Section Summary>\n"),
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
    if "" in extractedText:
        extractedText.remove("")

    if not extractedText:
        logging.warning("No text extracted from the PDF.")
        return ""
    
    fullText = "\n".join(extractedText)
    return generateData(fullText)

def replace_every_fourth_space(input_string):
    space_count = 0
    output_string = ""
    charCount = 0
    for char in input_string:
        charCount += 1
        if char == ' ':
            space_count += 1
            if charCount > 35:
                output_string += '&#92;n'
                charCount = 0
            else:
                output_string += char
        else:
            output_string += char
    output_string += '&#92;n&#92;n'
    return output_string


def processPDF(filepath):
    responseText = returnText(filepath)
    dot = graphviz.Digraph(format='png')
    dot.attr(ranksep='1.0')
    allResponses = responseText.split('\n')
    allResponses[0] = allResponses[0].replace("## Title: ","")
    nodeAttr = {
        "style": "filled",
        "color": "brown1",
        "fontcolor": "white",
        "fontname": "Arial"
    }
    dot.node('Title', label=allResponses[0], shape="record",_attributes=nodeAttr)
    for i in range(1, len(allResponses)):
        if("**Section: " in allResponses[i]):
            allResponses[i] = allResponses[i].removeprefix("**Section: ")
            allResponses[i] = allResponses[i].removesuffix("**")
            lastSectionName = allResponses[i]
            if("Summary: " in allResponses[i+1]):
                allResponses[i+1] = allResponses[i+1].removeprefix("Summary: ")
                allResponses[i+1] = replace_every_fourth_space(allResponses[i+1])
            nodeAttr = {
                "style":"filled",
                "color":"slateblue4",
                "fontcolor": "white",
                "fontname": "Arial"
            }
            dot.node(allResponses[i], label=f"{allResponses[i]}&#92;n&#92;n{allResponses[i+1]}", shape="record", _attributes=nodeAttr)
            edgeAttr = {
                "tailport":'s'
            }
            dot.edge('Title', allResponses[i], _attributes=edgeAttr)
        elif("**Sub-Section: " in allResponses[i]):
            allResponses[i] = allResponses[i].removeprefix("**Sub-Section: ")
            allResponses[i] = allResponses[i].removesuffix("**")
            if ("Summary: " in allResponses[i + 1]):
                allResponses[i + 1] = allResponses[i + 1].removeprefix("Summary: ")
                allResponses[i + 1] = replace_every_fourth_space(allResponses[i + 1])
            nodeAttr = {
                "style": "filled",
                "color": "darkslategray",
                "fontcolor": "white",
                "fontname": "Arial"
            }
            dot.node(allResponses[i], label=f"{allResponses[i]}&#92;n&#92;n{allResponses[i + 1]}", shape="record", _attributes=nodeAttr)
            dot.edge(lastSectionName, allResponses[i], _attributes=edgeAttr)
    dot.attr(size="25,25!")
    output_filepath = f"{filepath}_output"
        
    dot.render(output_filepath, format='png', cleanup=True)
    logging.info(f"Graph rendered to file: {output_filepath}.png")
        
    with open(f"{output_filepath}.png", 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    # Cleanup the generated output file
    os.remove(f"{output_filepath}.png")
    return img_base64

    # Example of a Graph made using GraphViz.
    # dot.node('A', 'Node 1')
    # dot.node('B', 'Node 2')
    # dot.node('C', 'Node 3')
    # dot.edge('A', 'B')
    # dot.edge('A', 'C')
    # dot.render('file1', format='png', cleanup=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
