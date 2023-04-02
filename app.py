from datetime import datetime
import os
from tempfile import NamedTemporaryFile

from flask import Flask, request, send_file
import ocrmypdf
from PIL import Image
import tempfile

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return """
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
                <button type='reset'>Reset</button>
                </form>
            </body>
        </html>
    """

@app.route("/ocrmypdf", methods=["POST"])
def ocrmypdf_api():
    if "file" not in request.files:
        return "No file uploaded", 400

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return "No file selected", 400

    allowed_extensions = {".pdf", ".jpg", ".jpeg", ".png"}
    file_extension = os.path.splitext(uploaded_file.filename)[1]

    if file_extension not in allowed_extensions:
        return "Invalid file type, please upload a PDF or image file", 400

    if file_extension in {".jpg", ".jpeg", ".png"}:
    # convert the image to PDF
        with Image.open(uploaded_file) as img:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                img.convert("RGB").save(temp_file, "PDF")
            pdf_file = open(temp_file.name, 'rb').read()
    else:
        pdf_file = uploaded_file.read() 

    ocr_options = request.form.get("ocr_options")

    # Read the PDF file and perform OCR on it
    with NamedTemporaryFile(suffix=".pdf") as pdf_output_file, NamedTemporaryFile(suffix=".pdf") as output_file:
        pdf_output_file.write(pdf_file)
        pdf_output_file.seek(0)

        try:
            ocrmypdf.ocr(
                pdf_output_file.name,
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
        download_name = f"{os.path.splitext(uploaded_file.filename)[0]}_{timestamp}_OCR.pdf"

        # Send the resulting file back to the user
        return send_file(
            output_file.name,
            as_attachment=True,
            download_name=download_name,
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
