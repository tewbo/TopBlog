from PIL import ImageDraw


def get_bounds(el):
    points = el['boundingBox']['vertices']
    min_x = min(int(point.get("x", "0")) for point in points)
    max_x = max(int(point.get("x", "0")) for point in points)
    min_y = min(int(point.get("y", "0")) for point in points)
    max_y = max(int(point.get("y", "0")) for point in points)
    return ((min_x, min_y), (max_x, max_y))


def _draw_element(drw, el, style, text_color = None, font = None):
    (min_x, min_y), (max_x, max_y) = get_bounds(el)
    drw.rectangle([(min_x, min_y), (max_x, max_y)], **style)
    if "text" in el:
        drw.text((min_x, max_y), el["text"], text_color, font=font)


def draw(img, blocks, block_style, line_style, word_style, text_color, text_font):
    draw = ImageDraw.Draw(img)
    for block in blocks:
        _draw_element(draw, block, block_style, None, text_font)
        for line in block["lines"]:
            _draw_element(draw, line, line_style, None, text_font)
            for word in line["words"]:
                _draw_element(draw, word, word_style, text_color, text_font)
    # img.show()


def draw_boxes(img, boxes, box_style, text_color, text_font):
    draw = ImageDraw.Draw(img)
    for box in boxes:
        _draw_element(draw, box, box_style, text_color, text_font)
    # img.show()


def resize(img, min_width, min_height, max_width, max_height):
    width, height = img.size
    lower_k = min(max_width / width, max_height / height)
    higher_k = max(min_width / width, min_height / height)
    k = min(max(1, lower_k), higher_k)
    width = int(k * width)
    height = int(k * height)
    fmt = img.format
    img = img.resize((width, height))
    img.format = fmt
    return img
