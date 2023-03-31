# ocrmypdf-web

ocrmypdf-web is a web-based front end for [OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF), a free and open-source tool that converts scanned documents to searchable PDFs.

This project is inspired by [sseemayer/OCRmyPDF-web](https://github.com/sseemayer/OCRmyPDF-web) with the following key differences:

* Flask-based web server (instead of Hug)
* Grossly blank web UI; the advantage being no JS required
  ![image](https://user-images.githubusercontent.com/2837532/229243759-4b56d973-02b3-4b6b-aa91-34da6fa4499f.png)
* Uses `OCRmyPDF`'s Python API directly (instead of invoking the CLI `ocrmypdf` using a subprocess)

Otherwise, it's conceptually the same and I encourage you to pick what suits you.

## Requirements

* Docker (with `docker-compose`)

## Getting Started

To run ocrmypdf-web locally, follow these steps:

1.  Clone this repository to your local machine.
2.  Navigate to the root directory of the cloned repository.
3.  Build the Docker image: `docker-compose build`.
4.  Start the Docker container: `docker-compose up`.
5.  Open your web browser and navigate to `http://localhost:8080`.

## Usage

ocrmypdf-web provides a simple web interface for uploading PDF files and running OCRmyPDF on them. To use ocrmypdf-web:

1.  Navigate to `http://localhost:8080` in a web browser.
2.  Click the "Browse..." button and select a PDF file to upload.
3.  Optionally select OCR options.
4.  Click the "OCR PDF" button.
5.  Once the conversion is complete, the resulting PDF will be downloaded (or opened) by your browser.

## Troubleshooting

If something goes wrong, you'll generally be led to the `/ocrmypdf` path in your browser with some error message to help you understand what went wrong.

Go back to the index page (where the PDF upload and OCR buttons are). To reset the form on the page, click the "Reset" button.

## Contributing

Issues and pull requests are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
