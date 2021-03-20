
from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .models import *
from .forms import *
from PIL import Image
from django.views import View
from django.contrib.auth.models import User,auth
from django.contrib import messages

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

def check_pin(request):
    if request.method == "POST": 
        if request.user.is_authenticated:
            final_data=""
            dec=""
            pin=request.POST['pin']
            image_name='encoded/'+decode.dec_image
            decoded=Document.objects.raw("SELECT id,message,pin,encoded_img from upload_document where pin = %s AND encoded_img = %s ",[pin,image_name])
            decoded_img=img_steg_enc.objects.raw("SELECT id,main_img FROM upload_img_steg_enc WHERE pin_img = %s AND enc_img_steg = %s ",[pin,image_name])
            if decoded:
                for data in decoded:
                    final_data=data.message
                final_data=final_data.replace("__sec_pin__"," ")
                return render(request, 'dec_print.html', {'msg_sec' : final_data})
            if decoded_img:
                for data in decoded_img:
                    dec=data.main_img
                #dec='mainimg/'+str(c)
                return render(request, 'prindec.html', {'content' : str(dec)})

            else:
                messages.warning(request,'Invalid Seecure pin !!! ')
                return render(request,"sec_pin.html")    
        else:
            messages.warning(request,'You must be logged In !!')
            return redirect('/Login')
    else:
        return redirect('/main')

# Create your views here.
def encode_msg(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.POST['message']
            im=request.FILES['image_path']
            if request.user.is_authenticated:
                sec_pin=0
                newimg=Image.open(im, "r") 
                newimg.save('media/documents/'+str(im))
                if request.POST['hidden_sec']=="pined":
                    sec_pin=request.POST['pin']
                    data = data+"__sec_pin__"
            
             
            ima=str(im).split(".")
            if ima[1]=="png":
                image = Image.open(im, "r")       
                newimg = image.convert('RGB')
                newimg.save('media/temporary/'+ima[0]+'.jpg')
                image = Image.open('media/temporary/'+ima[0]+'.jpg', "r")
            else:
                image = Image.open(im, "r")       
            newimg = image.copy() 
            encode_enc(newimg,data) 
            enc_img='enc'+str(im)
            enc_img1=enc_img.split(".")
            newimg.save('media/encoded/'+enc_img1[0]+'.png')
            content = 'encoded/'+enc_img1[0]+'.png'
            current_user = request.user
            if request.user.is_authenticated:
                Document(message=data,image_path=str(im),encoded_img=content,pin=str(sec_pin),user_id_id=current_user.id).save()
            return render(request, "encode.html", {'context':content})
            return HttpResponse("succesfully")
            
    else:
        form = DocumentForm()
        current_user = request.user
        cu=str(current_user.id)
        defaultpin=0
        encoded_data_msg=Document.objects.raw("Select id,message,pin,encoded_img from upload_document where user_id_id = %s ",[cu])[0:]
        encoded_data_img=Document.objects.raw("Select id,main_img,cover_img,pin_img,enc_img_steg from upload_img_steg_enc where user_id_img_id = %s ",[cu])[0:]
        return render(request, 'enc.html',{'encoded_data':encoded_data_msg,'defaultpin':defaultpin,'encoded_data_img':encoded_data_img,'form':form})
        #return render(request, 'content.html', {'form' : form}) 
'''
def index(request):
    current_user = request.user
    cu=str(current_user.id)
    defaultpin=0
    encoded_data_msg=Document.objects.raw("Select id,message,pin,encoded_img from upload_document where user_id_id = %s ",[cu])[0:]
    encoded_data_img=Document.objects.raw("Select id,main_img,cover_img,pin_img,enc_img_steg from upload_img_steg_enc where user_id_img_id = %s ",[cu])[0:]
    return render(request, 'content.html',{'encoded_data':encoded_data_msg,'defaultpin':defaultpin,'encoded_data_img':encoded_data_img})
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

def dec(request):
    return render(request,"dec.html")

def encoded_data(request):
    current_user = request.user
    cu=str(current_user.id)
    defaultpin=0
    encoded_data_msg=Document.objects.raw("Select id,message,pin,encoded_img from upload_document where user_id_id = %s ",[cu])[0:]
    encoded_data_img=Document.objects.raw("Select id,main_img,cover_img,pin_img,enc_img_steg from upload_img_steg_enc where user_id_img_id = %s ",[cu])[0:]
    return render(request,"encoded_data.html",{'encoded_data':encoded_data_msg,'defaultpin':defaultpin,'encoded_data_img':encoded_data_img})

def merge(request):
        """Merge two images. The second one will be merged into the first one.
            :param img1: First image
            :param img2: Second image
            :return: A new merged image.
        """
        if request.method == 'POST': 
            form = forms_imgenc(request.POST,request.FILES)
            data=""
            if form.is_valid():
                m_i=request.FILES['main_img']
                c_i=request.FILES['cover_img']
                img1 = Image.open(c_i, 'r') # cover image 
                img2 = Image.open(m_i,'r') # hidden image
                #form.save()
                if request.user.is_authenticated:
                    newimg=Image.open(m_i, "r") 
                    newimg.save('media/mainimg/'+str(m_i))
                    newimg=Image.open(c_i, "r")
                    newimg.save('media/coverimg/'+str(c_i))
                        
                
                m=str(m_i).split(".")
                c=str(c_i).split(".")
                if m[1]=="png" and c[1]=="jpg" or m[1]=="PNG":
                    image = Image.open(m_i, "r")       
                    newimg = image.convert('RGB')
                    newimg.save('media/temporary/'+m[0]+'.jpg') 
                    img1 = Image.open(c_i, 'r') # cover image 
                    img2 = Image.open('media/temporary/'+m[0]+'.jpg','r') # hidden image
                
                if c[1]=="png" and m[1]=="jpg" or c[1]=="PNG":
                    image = Image.open(c_i, "r")       
                    newimg = image.convert('RGB')
                    newimg.save('media/temporary/'+c[0]+'.jpg')
                    img1 = Image.open('media/temporary/'+c[0]+'.jpg', 'r') # cover image 
                    img2 = Image.open(m_i,'r') # hidden image
                
                if m[1]=="png" or m[1]=="PNG" and c[1]=="png" or c[1]=="PNG":
                    image = Image.open(c_i, "r")       
                    newimg = image.convert('RGB')
                    newimg.save('media/temporary/'+c[0]+'.jpg')
                    img1 = Image.open('media/temporary/'+c[0]+'.jpg', 'r') 
                    
                    image = Image.open(m_i, "r")       
                    newimg = image.convert('RGB')
                    newimg.save('media/temporary/'+m[0]+'.jpg') 
                    img2 = Image.open('media/temporary/'+m[0]+'.jpg','r') 

                '''
                if m[1]=="jpg" and c[1]=="jpg":
                    img1 = Image.open(c_i, 'r') # cover image 
                    img2 = Image.open(m_i,'r') # hidden image
                '''
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
                        
                            # Use a black pixel as default
                        rgb2 = int_to_bin((0, 0, 0))

                            # Check if the pixel map position is valid for the second image
                        if i < img2.size[0] and j < img2.size[1]:
                            rgb2 = int_to_bin(pixel_map2[i, j])
                            
                            # Merge the two pixels and convert it to a integer tuple
                        rgb = merge_rgb(rgb1, rgb2)

                        pixels_new[i, j] = bin_to_int(rgb)
                #k=enc_img1[0]+'.png'
                new_image.save('media/encoded/'+enc_img1[0]+'.png')
                val='encoded/'+enc_img1[0]+'.png'
                if request.user.is_authenticated:
                    sec_pin=0
                    current_user = request.user
                    if request.POST['hidden_sec']=="pined":
                        sec_pin=request.POST['pin']
                        data="__sec_pin__"
                        image = Image.open('media/encoded/'+enc_img1[0]+'.png', "r")
                        encode_enc(image,data) 
                        image.save('media/encoded/'+enc_img1[0]+'sp'+'.png')
                        val='encoded/'+enc_img1[0]+'sp'+'.png'
                    img_steg_enc(main_img='mainimg/'+str(m_i),cover_img='coverimg/'+str(c_i),pin_img=str(sec_pin),enc_img_steg=val,user_id_img_id=current_user.id).save()
                    return render(request, 'encoded_img.html', {'key' : val})

                return render(request, 'encoded_img.html', {'key' : val})
                #return HttpResponse("Successfully encoded")           
                
        else:
            form = forms_imgenc()
            current_user = request.user
            cu=str(current_user.id)
            defaultpin=0
            encoded_data_msg=Document.objects.raw("Select id,message,pin,encoded_img from upload_document where user_id_id = %s ",[cu])[0:]
            encoded_data_img=Document.objects.raw("Select id,main_img,cover_img,pin_img,enc_img_steg from upload_img_steg_enc where user_id_img_id = %s ",[cu])[0:]
            return render(request, 'enc.html',{'encoded_data':encoded_data_msg,'defaultpin':defaultpin,'encoded_data_img':encoded_data_img,'form':form})
            #return render(request, 'content.html', {'form' : form})

def decode_img(request):
    dec_img1=str(decode.dec_imag).split("_")
    img=Image.open(decode.dec_imag, "r")
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
            
    new_image.save('media/decoded/'+'decode'+str(decode.dec_imag))
                
    dec='decoded/'+'decode'+str(decode.dec_imag)
                
    return render(request, 'prindec.html', {'content' : dec})

def decode(request):
    if request.method=='POST':
        decode.dec_imag=request.FILES['dec_img']
        val=request.POST['value']
        decode.dec_image=str(decode.dec_imag)
        if val=="1":
            image = Image.open(decode.dec_imag, 'r') 
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
                sec_pin="__sec_pin__"
                if (pixels[-1] % 2 != 0): 
                    if data.endswith(sec_pin):
                        return render(request,'sec_pin.html')
                    return render(request, 'dec_print.html', {'msg' : data})
            
        elif val=="2":
            #dec_img=str(im)
            #if request.user.is_authenticated:
            image = Image.open(decode.dec_imag, 'r') 
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
                if "_" in data:
                    if request.user.is_authenticated:
                        return render(request,'sec_pin.html')
                    else:
                        return redirect('/Login') 
                else:
                    return decode_img(request)
                
    else:
        return redirect('/dec')
                
                