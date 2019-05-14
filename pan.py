from PIL import Image
import sys

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
# The tools are returned in the recommended order of usage
tool = tools[0]

langs = tool.get_available_languages()
lang = langs[0]
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use
txt = tool.image_to_string(
    Image.open('/home/caratred/copy/passport/AILEEN_MAUNAHAN_438.jpeg'),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)
print(txt)

word_boxes = tool.image_to_string(
    Image.open('/home/caratred/copy/passport/AILEEN_MAUNAHAN_438.jpeg'),
    lang="eng",
    builder=pyocr.builders.WordBoxBuilder()
)
print (word_boxes[33].__dict__)
for x in word_boxes:

    print(x.__dict__)
