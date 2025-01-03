from flask import request, render_template
from myapp.jutils.jamba_generate import chat_development
from myapp.jutils.text_pp import parse_response, create_ppt

def generate():
    if request.method == 'POST':
        number_of_slide = request.form.get('number_of_slide')
        user_text = request.form.get('user_text')
        template_choice = request.form.get('template_choice')
        presentation_title = request.form.get('presentation_title')
        presenter_name = request.form.get('presenter_name')
        insert_image = 'insert_image' in request.form

        # Formulate the user query
        user_message = (
            f"I want you to come up with the idea for the PowerPoint. The number of slides is {number_of_slide}. "
            f"The content is: {user_text}. The title of content for each slide must be unique, "
            f"and extract the most important keyword within two words for each slide."
        )

        # Generate the response using AI21
        assistant_response = chat_development(user_message)

        # Debug response
        print(f"Assistant Response:\n{assistant_response}")

        # Parse and create the presentation
        slides_content = parse_response(assistant_response)
        create_ppt(slides_content, template_choice, presentation_title, presenter_name, insert_image)

    return render_template('generator.html', title='Generate')
