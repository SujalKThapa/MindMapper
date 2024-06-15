import azure.functions as func
import logging
import json
from werkzeug.utils import secure_filename
import os
from main import processPDF  # Import the processPDF function

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

TEMP_DIR = "/tmp"  # Define a temporary directory within the container

@app.route(route="http_trigger", methods=["POST"])
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if req.method == 'POST':
        try:
            # Parse the multipart form data
            form = req.form
            file = req.files.get('file')  # Expecting 'file' field in the form-data
            name = form.get('name')
            
            if file and file.filename:
                if file.content_type != 'application/pdf':
                    return func.HttpResponse("Only PDF files are allowed.", status_code=400)
                
                # Secure the filename and create a file path within the container
                filename = secure_filename(file.filename)
                file_path = os.path.join(TEMP_DIR, filename)
                
                with open(file_path, 'wb') as f:
                    f.write(file.read())
                
                logging.info(f"File saved to: {file_path}")

                try:
                    image_base64 = processPDF(file_path)
                    response_body = {
                        "image_html": f"<img src='data:image/png;base64,{image_base64}' alt='Generated Image' />"
                    }
                    return func.HttpResponse(json.dumps(response_body), mimetype='application/json', status_code=200)
                except Exception as e:
                    logging.error(f"Error processing PDF: {e}")
                    return func.HttpResponse("An error occurred while processing the PDF.", status_code=500)
                finally:
                    try:
                        os.remove(file_path)
                        logging.info(f"Temporary file {file_path} deleted successfully.")
                    except Exception as cleanup_error:
                        logging.error(f"Error deleting temporary file {file_path}: {cleanup_error}")
                
            else:
                return func.HttpResponse("No file uploaded.", status_code=400)
        
        except Exception as e:
            logging.error(f"Error processing the file upload: {e}")
            return func.HttpResponse("An error occurred while processing the file upload.", status_code=500)
    
    return func.HttpResponse(
        "This HTTP triggered function executed successfully. Pass a PDF file in the form-data.",
        status_code=200
    )
