# -*- coding: utf-8 -*-
# image_word_to_image_tag.py

import base64

# 1 pixel = 9525 emus. Elaboro con menos emus para mejorar el ajuste visual.
pixel_a_emus = 7925

def calculate_pixels_from_emu(emu_value):
    return int(emu_value / pixel_a_emus)

def get_drawing_extent(drawing_element):
    namespaces = {'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
    return drawing_element.find('.//wp:extent', namespaces)

def extract_emu_dimensions(extent_element):
    if extent_element is not None:
        witdh_emu = int(extent_element.get('cx'))
        height_emu = int(extent_element.get('cy'))
        return witdh_emu, height_emu
    return None, None

def get_pixel_dimensions(drawing_element):
    extent_element = get_drawing_extent(drawing_element)
    width_emu, height_emu = extract_emu_dimensions(extent_element)
    
    if width_emu and height_emu:
        width = calculate_pixels_from_emu(width_emu)
        height = calculate_pixels_from_emu(height_emu)
        return width, height
    return None, None

def encode_blob_to_base64(image_blob):
    return base64.b64encode(image_blob).decode('utf-8')

def build_proportional_image_tag(content_type, base64_data, width, height):
    tag_text = f'<img src="data:{content_type};base64,{base64_data}"'
    if width and height:
        return f'{tag_text} width="{width}" height="{height}" />'
    return f'{tag_text} style="max-width: 100%; height: auto;" />'

# Función empleada de forma principal
def generate_html_image_output(doc_part, embed_id, drawing_element):
    image_part = doc_part.related_parts[embed_id]
    base64_string = encode_blob_to_base64(image_part.blob)
    width_px, height_px = get_pixel_dimensions(drawing_element)
    
    return build_proportional_image_tag(
        image_part.content_type,
        base64_string,
        width_px,
        height_px)