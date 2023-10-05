import os
from flask import Flask, request, render_template
from generate_answer import GenerateAnswer
import warnings

warnings.filterwarnings("ignore")
app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Function to check if a file has an allowed extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("upload.html", result=None)


@app.route("/upload", methods=["POST"])
def upload_file():
    # Check if the post request has the file part and text input
    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]
    input_text = request.form["text_input"]

    # If the user does not select a file, browser also
    # submit an empty part without filename
    if file.filename == "":
        return "No selected file"

    if file and allowed_file(file.filename):
        try:
            # Save the PDF file
            filename = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filename)

            # Process the PDF to extract text
            generate = GenerateAnswer(file=filename)
            ans = generate.answer(input_text)
            print("result :", ans["result"])
            text = ans["result"]
            # Combine the extracted text and input text
            result = f"Input Text: {input_text}\n\nExtracted Text:\n{text}"

            return render_template("upload.html", input_text=input_text, result=text)
        except Exception as e:
            return str(e)

    return "Invalid file type"


if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True)
