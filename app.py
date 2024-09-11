import pdfplumber
import os
from PIL import Image
from io import BytesIO

def get_cropped_image(page, bbox, dpi):
    cropped_page = page.within_bbox(bbox).to_image(resolution=dpi)
    return cropped_page.original

def save_image(image, output_path, quality):
    img_bytes = BytesIO()
    image.save(img_bytes, format='PNG', quality=quality)
    img_bytes.seek(0)
    pil_image = Image.open(img_bytes)
    pil_image.save(output_path, quality=quality)
    print(f"Saved {output_path}")

def extract_images_from_pdf(pdf_path, output_dir, dpi=500, quality=98):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_output_dir = os.path.join(output_dir, pdf_name)
    os.makedirs(pdf_output_dir, exist_ok=True)

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            images = page.images
            for img_index, img in enumerate(images, start=1):
                bbox = (img['x0'], img['top'], img['x1'], img['bottom'])
                try:
                    image = get_cropped_image(page, bbox, dpi)
                    image_filename = f"page_{page_number}_image_{img_index}.jpg"
                    image_filepath = os.path.join(pdf_output_dir, image_filename)
                    save_image(image, image_filepath, quality)
                except Exception as e:
                    pass

if __name__ == "__main__":
    pdf_file = "test.pdf"
    output_directory = "extract2"
    extract_images_from_pdf(pdf_file, output_directory)
