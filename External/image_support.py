
from External.image import create_text_extraction_pipeline

def extract_image_text(image_path):
    image_pipeline = create_text_extraction_pipeline(image_path)
    image_output = image_pipeline.run()
    image_context = image_output[0]['task_output']
    image_context = image_context.choices[0].message.content

    return image_context
