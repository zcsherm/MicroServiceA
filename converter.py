from PIL import Image, ImageFont, ImageDraw
import os
import smallBasicFont

def run_conversion(text, size, font, threshold, dest=None):
    """
    Converts a given text into a chart
    :param text: The text to convert
    :param size: The size of the text
    :param font: the font
    :param threshold: The color threshold to register as black. Set to higher values for stronger bias towards back
    :param dest: The location of the font
    :return: the chart
    """
    dest = os.getcwd()+'/' + dest

    # If the user specified the basic font
    if font.lower() == 'basic':
        output = convert_to_basic(text, size.lower())

    # Otherwise, we run the normal algo
    else:
        size = int(size)
        output = convert_sentence_to_pattern(text,size,font,dest,threshold)
    return output

def convert_sentence_to_pattern(text,size,font,dest,threshold):
    """
    Converts a sentence into a patter
    :param text:
    :param size:
    :param font:
    :param dest:
    :param threshold:
    :return:
    """
    # Get the font files in our directory
    fonts = os.listdir(dest)
    font_file = None
    possible_fonts = []

    # Search for possible matches or absolute matches
    for file in fonts:
        if file[0:-4].lower() == font.lower():
            font_file = file
            break
        if font.lower() in file.lower():
            possible_fonts.append(file)

    # If we didn't find an absolute match, we'll just pick the shortest named best fit
    if not font_file and len(possible_fonts) >0:
        chosen =possible_fonts[0]
        for file in possible_fonts:
            if len(file) < len(chosen):
                chosen = file
        font_file = chosen

    # If we didn't find a file, then uh oh
    elif not font_file:
        return 'error'

    # Load the font, find the size of the text in that font and make a new image
    font = ImageFont.truetype(f"fonts/{font_file}",size)
    dimensions = (font.getbbox(text)[2],font.getbbox(text)[3])
    new_image = Image.new('RGB', dimensions, (255, 255, 255))

    # Write the font onto the image, then change it into a 1bpp type image with a bias towards 0 of threshold
    ImageDraw.Draw(new_image).multiline_text((0,0),text=text,fill=(0,0,0),font=font)
    thresh = threshold
    fn = lambda x: 255 if x > thresh else 0
    new_image = new_image.convert('L').point(fn, mode='1')

    # Convert this image into a matrix
    matrix=convert_to_matrix(new_image)
    return matrix

def convert_to_matrix(image=Image.Image):
    """
    Converts a 1bpp image into a matrix where 0's represent white, 1's represent black
    Note: This could be greatly simplified by inverting the image and dividing by 255
    :param image: The image to convert
    :return: A matrix representing that image
    """

    matrix = []
    height=image.height
    width= image.width

    # Create an empty row
    blank_row = [0 for i in range(width)]

    # Iterate through pixel by pixel, update our matrix
    started = False
    for y in range(0,image.height):
        row = []
        for x in range(0, image.width):
            pixel = image.getpixel((x,y))
            if pixel ==255:
                row.append(0)
            else:
                row.append(1)

        # Some fonts have considerable white space above the characters, this removes them
        if not started:
            if row == blank_row:
                continue
            else:
                started = True
        matrix.append(row)

    # If there's whitespace below the text, get rid of those rows
    while True:
        if matrix[-1] == blank_row:
            matrix.pop()
        else:
            break
    return matrix

def convert_to_basic(message, size):
    """
    Converts a message to the basic knitting font form
    :param message: The message to convert
    :param size: enum: small, medium or large
    :return: The chart for the message
    """
    characters = []
    ratio = 1
    for character in message.upper():
        # Get each individual character, and scale it up based on size:
        if size =='medium':
            characters.append(scale_up(smallBasicFont.smallBasicFontData[character],2))
            ratio = 2
        elif size == 'large':
            characters.append(scale_up(smallBasicFont.smallBasicFontData[character],3))
            ratio = 3
        else:
            characters.append(smallBasicFont.smallBasicFontData[character])
            ratio =1
    # Stich each character together
    message = [[] for _ in range(ratio*5)]
    for character in characters:
        for i in range(len(character)):
            # Stich row by row and add space between characters
            message[i] += character[i] + [0 for _ in range(ratio)]
    # Get rid of excess white space
    for row in message:
        row.pop()
    return message

def scale_up(character, ratio):
    """
    Scales up the basic font based on a ratio
    :param character: The character in the basic font
    :param ratio: The amount to scale it up
    :return: The scaled up chart
    """
    # Build an empty array of the scaled up size
    new_character = [[0 for _ in range(len(character[0])*ratio)] for _ in range(len(character)*ratio)]

    # Each pixel goes from a 1x1 space to a ratio x ratio space
    for row in range(len(character)):
        for col in range(len(character[row])):
            for i in range(ratio):
                for q in range(ratio):
                    new_character[row*ratio+i][col*ratio+q]= character[row][col]

    return new_character
