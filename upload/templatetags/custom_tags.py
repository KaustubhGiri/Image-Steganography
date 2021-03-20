from django import template
register = template.Library()

@register.simple_tag()
def extract_imgname(encoded_img):
    img=str(encoded_img)
    image_name=img.split('/')
    return str(image_name[1])

@register.simple_tag()
def extract_msg(encoded_msg):
    sec_pin="__sec_pin__"
    if encoded_msg.endswith(sec_pin):
        encoded_msg=encoded_msg.replace("__sec_pin__"," ")
        return str(encoded_msg)
    else:
        return str(encoded_msg)

@register.simple_tag()
def count_no(sr_no):
    for no in sr_no:
        return no


    