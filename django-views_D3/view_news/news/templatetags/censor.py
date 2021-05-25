from django import template
 
register = template.Library()

mats = ["хуй", "хуе", "хуё", "пизд", "ёб", "ебать", "блять"]

 
@register.filter(name='censor')
def censor(value, arg):
    #for mat in mats:
    #    value = value.replace(mat, '*')
    words = value.split();
    for word in words:
        for mat in mats:
            if word.find(mat) != -1:
                value = value.replace(word, "*")			
    return value
