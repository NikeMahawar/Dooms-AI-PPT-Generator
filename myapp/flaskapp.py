import os
from flask import Flask, render_template, send_from_directory, abort, request
from dotenv import load_dotenv
from myapp.utils.generate_route import generate as gpt4_generate
from myapp.gutils.gemini_generate_route import generate as gemini_generate
from myapp.jutils.jamba_generate_route import generate as jamba_generate

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/generator', methods=['GET', 'POST'])
def generator_route():
    if request.method == 'POST':
        model_choice = request.form.get('model_choice')
        file_path = os.path.join('/tmp', 'generated_presentation.pptx')  # Save to temp dir

        if model_choice == 'gpt4':
            gpt4_generate(file_path)  # Pass the temp file path
        elif model_choice == 'gemini':
            gemini_generate(file_path)
        elif model_choice == 'jamba':
            jamba_generate(file_path)
        else:
            abort(400, description="Invalid model choice")

        return render_template('generator.html', title='Generate',
                               download_link=f"/download/generated_presentation.pptx")

    return render_template('generator.html', title='Generate')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    temp_dir = '/tmp'  # Temporary storage directory
    try:
        response = send_from_directory(temp_dir, filename, as_attachment=True)
        os.remove(os.path.join(temp_dir, filename))  # Clean up after serving
        return response
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
