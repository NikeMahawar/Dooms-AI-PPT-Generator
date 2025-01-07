import os
from flask import Flask, render_template, send_from_directory, abort, request, url_for
from dotenv import load_dotenv
from utils.generate_route import generate as gpt4_generate
from gutils.gemini_generate_route import generate as gemini_generate
from jutils.jamba_generate_route import generate as jamba_generate
from flask import after_this_request

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

temp_dir = '/tmp'


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/generator', methods=['GET', 'POST'])
def generator_route():
    if request.method == 'POST':
        model_choice = request.form.get('model_choice')
        filename = 'generated_presentation.pptx'
        file_path = os.path.join(temp_dir, filename)

        os.makedirs(temp_dir, exist_ok=True)

        if model_choice == 'gpt4':
            gpt4_generate(file_path)
        elif model_choice == 'gemini':
            gemini_generate(file_path)
        elif model_choice == 'jamba':
            jamba_generate(file_path)
        else:
            abort(400, description="Invalid model choice")

        download_link = url_for('download_file', filename=filename)
        return render_template('generator.html', title='Generate', download_link=download_link)

    return render_template('generator.html', title='Generate')


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(temp_dir, filename)

    try:
        @after_this_request
        def remove_file(response):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file: {e}")
            return response

        return send_from_directory(temp_dir, filename, as_attachment=True)

    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
