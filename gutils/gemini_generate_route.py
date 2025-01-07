from flask import request, render_template
from gutils.gem_generate import chat_development
from gutils.text_pp import parse_response, create_ppt

def generate(file_path):
    if request.method == 'POST':
        number_of_slide = request.form.get('number_of_slide')
        user_text = request.form.get('user_text')
        template_choice = request.form.get('template_choice')
        presentation_title = request.form.get('presentation_title')
        presenter_name = request.form.get('presenter_name')
        insert_image = 'insert_image' in request.form

        user_message = f"I want you to create PowerPoint slides with the following requirements: " \
                       f"The number of slides is {number_of_slide}. Each slide should contain a 'Content' section with approximately 100–120 words. " \
                       f"The content is: {user_text}. Ensure the title of each slide is unique and extract the most important keyword (two words) for each slide."

        assistant_response = chat_development(user_message)
        print("=== Raw Response ===")
        print(assistant_response)
        print("=== End Raw Response ===")

        slides_content = parse_response(assistant_response)
        print("=== Parsed Slides ===")
        for slide in slides_content:
            print(f"Title: {slide['title']}")
            print(f"Content length: {len(slide['content'])}")
            print(f"Keywords: {slide['keywords']}")
            print("---")
        print("=== End Parsed Slides ===")
        create_ppt(slides_content, template_choice, presentation_title, presenter_name, insert_image, file_path)

    return render_template('generator.html', title='Generate')
