import azure.functions as func
import logging
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import tempfile
from main import processPDF  # Import the processPDF function

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

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
                
                # Secure the filename and create a temporary file
                filename = secure_filename(file.filename)
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    temp_path = tmp_file.name
                    tmp_file.write(file.read())

                # Process the file using the processPDF function
                logging.info(f"File saved to temporary location: {temp_path}")
                try:
                    image_base64 = processPDF(temp_path)
                    response_body = f"<img src='data:image/png;base64,{image_base64}' alt='Generated Image' />"
                    return func.HttpResponse(response_body, mimetype='text/html', status_code=200)
                except Exception as e:
                    logging.error(f"Error processing PDF: {e}")
                    return func.HttpResponse("An error occurred while processing the PDF.", status_code=500)
                
            else:
                return func.HttpResponse("No file uploaded.", status_code=400)
        
        except Exception as e:
            logging.error(f"Error processing the file upload: {e}")
            return func.HttpResponse("An error occurred while processing the file upload.", status_code=500)
    
    return func.HttpResponse(
        "This HTTP triggered function executed successfully. Pass a PDF file in the form-data.",
        status_code=200
    )
