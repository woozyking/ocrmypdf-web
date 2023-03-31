from datetime import datetime
from io import BytesIO
import os
from tempfile import NamedTemporaryFile

from flask import Flask, request, send_file
import ocrmypdf


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return '''
        <!doctype html>
        <html>
            <body>
                <form action='/ocrmypdf' method='post' enctype='multipart/form-data'>
                <input type='file' name='file' accept='.pdf' required>
                <p>Select OCR options:</p>
                <input type='radio' name='ocr_options' value='default' checked>Default<br>
                <input type='radio' name='ocr_options' value='skip_text'>Skip Text<br>
                <input type='radio' name='ocr_options' value='force_ocr'>Force OCR<br>
                <input type='radio' name='ocr_options' value='redo_ocr'>Redo OCR<br>
                <br>
                <input type='submit' value='OCR PDF'>
                </form>
            </body>
        </html>
    '''


@app.route("/ocrmypdf", methods=["POST"])
def ocrmypdf_api():
    if "file" not in request.files:
        return "No file uploaded", 400

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return "No file selected", 400

    if uploaded_file.mimetype != "application/pdf":
        return "Invalid file type, please upload a PDF file", 400

    filename_parts = os.path.splitext(uploaded_file.filename)
    ocr_options = request.form.get("ocr_options")

    # Read the PDF file and perform OCR on it
    with NamedTemporaryFile(suffix=filename_parts[1]) as output_file, BytesIO(
        uploaded_file.read()
    ) as input_buffer:
        try:
            ocrmypdf.ocr(
                input_buffer,
                output_file.name,
                force_ocr=(ocr_options == "force_ocr"),
                skip_text=(ocr_options == "skip_text"),
                redo_ocr=(ocr_options == "redo_ocr"),
            )
        except ocrmypdf.exceptions.PriorOcrFoundError:
            return (
                "This file already has OCR. Go back to try a different file or OCR option",
                400,
            )
        except:
            return (
                "Unknown error, file might not be supported. Go back to try a different file or OCR option",
                500,
            )

        # Set the name of the resulting OCR'ed file
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        download_name = f"{filename_parts[0]}_{timestamp}_OCR{filename_parts[1]}"

        # Send the resulting file back to the user
        return send_file(
            output_file.name,
            as_attachment=True,
            download_name=download_name,
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
