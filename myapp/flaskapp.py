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
        if model_choice == 'gpt4':
            return gpt4_generate()
        elif model_choice == 'gemini':
            return gemini_generate()
        elif model_choice == 'jamba':
            return jamba_generate()
        else:
            abort(400, description="Invalid model choice")
    return render_template('generator.html', title='Generate')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory('generated', filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
