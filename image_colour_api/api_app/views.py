from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import io
from colorthief import ColorThief
from urllib.request import urlopen
from PIL import Image
import requests

# Create your views here.

@api_view(['GET'])
def index(request):
    if request.method=='GET':
        url = request.GET['src']
        fd = urlopen(url)
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        dominant_border_color = border_color(f)
        dominant_color_hex = rgb_to_hex(color_thief.get_color(quality=1))
        return Response({'dominant_border_color': dominant_border_color, 'dominant_color':dominant_color_hex},status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def border_color(f):
    img = Image.open(f)
    width, height = img.size
    max_fre = 0
    res = 0
    lst = []
    for i in range(0,width):
        colors = img.getpixel((i,0))
        colors1 = img.getpixel((i,height-1))
        if len(colors) == 4:
            clr = (colors[1],colors[2],colors[3])
            lst.append(clr)
            clrs = (colors1[1],colors1[2],colors1[3])
            lst.append(clrs)
        else: 
            lst.append(colors)
            lst.append(colors1)


    for i in range(0,height):
        colors = img.getpixel((0, i))
        colors1 = img.getpixel((width-1, i))
        if len(colors) == 4:
            clr = (colors[1],colors[2],colors[3])
            lst.append(clr)
            clrs = (colors1[1],colors1[2],colors1[3])
            lst.append(clrs)
        else: 
            lst.append(colors)
            lst.append(colors1)


    for i in lst:
        freq = lst.count(i)
        if freq > max_fre:
            max_fre = freq
            res = i

    return rgb_to_hex(res)
