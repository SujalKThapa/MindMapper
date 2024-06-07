import logging
import azure.functions as func
from PyPDF2 import PdfFileReader
import io

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get the file from the request
        pdf_file = req.files['file']
        pdf_reader = PdfFileReader(io.BytesIO(pdf_file.read()))

        # Example: Extract number of pages
        num_pages = pdf_reader.getNumPages()
        response_message = f"The PDF file has {num_pages} pages."

        return func.HttpResponse(response_message, status_code=200)
    except Exception as e:
        logging.error(f"Error processing PDF file: {e}")
        return func.HttpResponse("Failed to process PDF file.", status_code=400)
