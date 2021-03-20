from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .models import *
from .forms import *
from PIL import Image
from django.views import View

def genData(data): 
          
        # list of binary codes 
        # of given data 
        newd = []  
          
        for i in data: 
            newd.append(format(ord(i), '08b')) 
        return newd 
          
# Pixels are modified according to the 
# 8-bit binary data and finally returned 
def modPix(pix, data): 
      
    datalist = genData(data) 
    lendata = len(datalist) 
    imdata = iter(pix) 
  
    for i in range(lendata): 
          
        # Extracting 3 pixels at a time 
        pix = [value for value in imdata.__next__()[:3] +
                                  imdata.__next__()[:3] +
                                  imdata.__next__()[:3]] 
                               
        # Pixel value should be made  
        # odd for 1 and even for 0 
        for j in range(0, 8): 
            if (datalist[i][j]=='0') and (pix[j]% 2 != 0): 
                  
                if (pix[j]% 2 != 0): 
                    pix[j] -= 1
                      
            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0): 
                pix[j] -= 1
                  
        # Eigh^th pixel of every set tells  
        # whether to stop ot read further. 
        # 0 means keep reading; 1 means the 
        # message is over. 
        if (i == lendata - 1): 
            if (pix[-1] % 2 == 0): 
                pix[-1] -= 1
        else: 
            if (pix[-1] % 2 != 0): 
                pix[-1] -= 1
  
        pix = tuple(pix) 
        yield pix[0:3] 
        yield pix[3:6] 
        yield pix[6:9] 
  
def encode_enc(newimg, data): 
    w = newimg.size[0] 
    (x, y) = (0, 0) 
      
    for pixel in modPix(newimg.getdata(), data): 
          
        # Putting modified pixels in the new image 
        newimg.putpixel((x, y), pixel) 
        if (x == w - 1): 
            x = 0
            y += 1
        else: 
            x += 1
 
# Create your views here.
def encode_msg(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        data = request.POST['message']
        
        if form.is_valid():
            form.save()
            im=request.FILES['image_path']
            ima=str(im).split(".")
            if ima[1]=="png":
                image = Image.open(im, "r")       
                newimg = image.convert('RGB')
                newimg.save(ima[0]+'.jpg')
                image = Image.open(ima[0]+'.jpg', "r")
            else:
                image = Image.open(im, "r")       
            newimg = image.copy() 
            encode_enc(newimg,data) 
            enc_img='enc'+str(im)
            enc_img1=enc_img.split(".")
            newimg.save('media/encoded/'+enc_img1[0]+'.png')
            content = 'encoded/'+enc_img1[0]+'.png'
            return render(request, "encode.html", {'context':content})
            return HttpResponse("succesfully")
            
           
            
    else:
        form = DocumentForm()
        return render(request, 'content.html', {'form' : form}) 

def index(request):
    return render(request, 'content.html')

'''
def decode_msg(dec_img):
            #dec_img=request.FILES['dec_img']
            image = Image.open(dec_img, 'r') 
        
            data = '' 
            imgdata = iter(image.getdata()) 
            
            while (True): 
                pixels = [value for value in imgdata.__next__()[:3] +
                                        imgdata.__next__()[:3] +
                                        imgdata.__next__()[:3]] 
                # string of binary data 
                binstr = '' 
                
                for i in pixels[:8]: 
                    if (i % 2 == 0): 
                        binstr += '0'
                    else: 
                        binstr += '1'
                        
                data += chr(int(binstr, 2)) 
                if (pixels[-1] % 2 != 0): 
                    return render(request, 'dec_print.html', {'msg' : data})
 '''  
    
def int_to_bin(rgb):
    """Convert an integer tuple to a binary (string) tuple.
        :param rgb: An integer tuple (e.g. (220, 110, 96))
        :return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
    """
    r, g, b = rgb
    return ('{0:08b}'.format(r),
            '{0:08b}'.format(g),
            '{0:08b}'.format(b))

def bin_to_int(rgb):
    """Convert a binary (string) tuple to an integer tuple.
        :param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :return: Return an int tuple (e.g. (220, 110, 96))
    """
    r, g, b = rgb
    return (int(r, 2),
            int(g, 2),
            int(b, 2))

def merge_rgb(rgb1, rgb2):
        """Merge two RGB tuples.
        :param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :param rgb2: Another string tuple
        (e.g. ("00101010", "11101011", "00010110"))
        :return: An integer tuple with the two RGB values merged.
        """
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb

def merge(request):
        """Merge two images. The second one will be merged into the first one.
            :param img1: First image
            :param img2: Second image
            :return: A new merged image.
        """
        if request.method == 'POST': 
            form = forms_imgenc(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                '''
                rgb=(220, 110, 96)
                k=int_to_bin(rgb)
                return render(request, 'prin.html', {'king' : k})

                '''
                m_i=request.FILES['main_img']
                c_i=request.FILES['cover_img']
                m=str(m_i).split(".")
                c=str(c_i).split(".")
                if m[1]=="png" and c[1]=="jpg" or m[1]=="PNG":
                    image = Image.open(m_i, "r")       
                    newimg = image.convert('RGB')
                    newimg.save(m[0]+'.jpg') 
                    img1 = Image.open(c_i, 'r') # cover image 
                    img2 = Image.open(m[0]+'.jpg','r') # hidden image
                
                if c[1]=="png" and m[1]=="jpg" or c[1]=="PNG":
                    image = Image.open(c_i, "r")       
                    newimg = image.convert('RGB')
                    newimg.save(c[0]+'.jpg')
                    img1 = Image.open(c[0]+'.jpg', 'r') # cover image 
                    img2 = Image.open(m_i,'r') # hidden image
                
                if m[1]=="png" or m[1]=="PNG" and c[1]=="png" or c[1]=="PNG":
                    image = Image.open(c_i, "r")       
                    newimg = image.convert('RGB')
                    newimg.save(c[0]+'.jpg')
                    img1 = Image.open(c[0]+'.jpg', 'r') 
                    
                    image = Image.open(m_i, "r")       
                    newimg = image.convert('RGB')
                    newimg.save(m[0]+'.jpg') 
                    img2 = Image.open(m[0]+'.jpg','r') 

                if m[1]=="jpg" and c[1]=="jpg":
                    img1 = Image.open(c_i, 'r') # cover image 
                    img2 = Image.open(m_i,'r') # hidden image
                
            #Check the images dimensions
            # Get the pixel map of the two images
                pixel_map1 = img1.load()
                pixel_map2 = img2.load()

            # Create a new image that will be outputted
                new_image = Image.new(img1.mode, img1.size)
                pixels_new = new_image.load()
                enc_img='encoded_'+str(c_i)
                enc_img1=enc_img.split(".")
                
                for i in range(img1.size[0]):
                    for j in range(img1.size[1]):
                        rgb1 = int_to_bin(pixel_map1[i, j])
                        #return render(request, 'prin.html', {'king' : pixel_map1[i, j]})
                        
                            # Use a black pixel as default
                        rgb2 = int_to_bin((0, 0, 0))

                            # Check if the pixel map position is valid for the second image
                        if i < img2.size[0] and j < img2.size[1]:
                            rgb2 = int_to_bin(pixel_map2[i, j])
                            #return render(request, 'prin.html', {'king' : pixel_map2[i, j]})
                            
                            # Merge the two pixels and convert it to a integer tuple
                        rgb = merge_rgb(rgb1, rgb2)

                        pixels_new[i, j] = bin_to_int(rgb)
                #k=enc_img1[0]+'.png'
                new_image.save('media/encoded/'+enc_img1[0]+'.png')
                val='encoded/'+enc_img1[0]+'.png'
                return render(request, 'encoded_img.html', {'key' : val})
                #return HttpResponse("Successfully encoded")           
                
        else:
            form = forms_imgenc()
            return render(request, 'content.html', {'form' : form})
'''
def unmerge(im):
        """Unmerge an image.
        :param img: The input image.
        :return: The unmerged/extracted image.
            if request.method == 'POST': 
            form = forms_imgdec(request.POST,request.FILES)
            if form.is_valid():
                im=request.FILES['main_img_dec']
      
        dec_img=str(im)
        dec_img1=dec_img.split("_")
        img=Image.open(im, "r")
                # Load the pixel map
        pixel_map = img.load()
                # Create the new image and load the pixel map
        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()

                # Tuple used to store the image original size
        original_size = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                        # Get the RGB (as a string tuple) from the current pixel
                r, g, b = int_to_bin(pixel_map[i, j])

                        # Extract the last 4 bits (corresponding to the hidden image)
                        # Concatenate 4 zero bits because we are working with 8 bit
                rgb = (r[4:] + '0000',
                    g[4:] + '0000',
                    b[4:] + '0000')

                        # Convert it to an integer tuple
                pixels_new[i, j] = bin_to_int(rgb)

                        # If this is a 'valid' position, store it
                        # as the last valid position
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

                # Crop the image based on the 'valid' pixels
        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))
        dec_img=str(im)
        dec_img1=dec_img.split("_")
        new_image.save('media/decoded/'+'decode'+dec_img1[1])
        dec='decoded/'+'decode'+dec_img1[1]
        return render(request, 'prindec.html', {'content' : dec})
 '''       
def decode(request):
    if request.method=='POST':
        dec_imag=request.FILES['dec_img']
        val=request.POST['value']
        #dec_img=str(dec_imag)
        if val=="1":
            #return render(request,'encode.html',{'de': dec_img })

            image = Image.open(dec_imag, 'r') 
        
            data = '' 
            imgdata = iter(image.getdata()) 
            
            while (True): 
                pixels = [value for value in imgdata.__next__()[:3] +
                                        imgdata.__next__()[:3] +
                                        imgdata.__next__()[:3]] 
                # string of binary data 
                binstr = '' 
                
                for i in pixels[:8]: 
                    if (i % 2 == 0): 
                        binstr += '0'
                    else: 
                        binstr += '1'
                        
                data += chr(int(binstr, 2)) 
                if (pixels[-1] % 2 != 0): 
                    #return render(request, 'msgalert.js', {'msg':data},content_type="application/x-javascript")
                    return render(request, 'dec_print.html', {'msg' : data})
            #return render(request,'encode.html')
            #decode_msg(k)
        elif val=="2":
            #dec_img=str(im)
            dec_img1=str(dec_imag).split("_")
            img=Image.open(dec_imag, "r")
                    # Load the pixel map
            pixel_map = img.load()
                    # Create the new image and load the pixel map
            new_image = Image.new(img.mode, img.size)
            pixels_new = new_image.load()

                    # Tuple used to store the image original size
            original_size = img.size

            for i in range(img.size[0]):
                for j in range(img.size[1]):
                            # Get the RGB (as a string tuple) from the current pixel
                    r, g, b = int_to_bin(pixel_map[i, j])

                            # Extract the last 4 bits (corresponding to the hidden image)
                            # Concatenate 4 zero bits because we are working with 8 bit
                    rgb = (r[4:] + '0000',
                        g[4:] + '0000',
                        b[4:] + '0000')

                            # Convert it to an integer tuple
                    pixels_new[i, j] = bin_to_int(rgb)

                            # If this is a 'valid' position, store it
                            # as the last valid position
                    if pixels_new[i, j] != (0, 0, 0):
                        original_size = (i + 1, j + 1)

                    # Crop the image based on the 'valid' pixels
            new_image = new_image.crop((0, 0, original_size[0], original_size[1]))
            #dec_img=str(im)
            #dec_img1=dec_img.split("_")
            new_image.save('media/decoded/'+'decode'+dec_img1[1])
            dec='decoded/'+'decode'+dec_img1[1]
            return render(request, 'prindec.html', {'content' : dec})

                