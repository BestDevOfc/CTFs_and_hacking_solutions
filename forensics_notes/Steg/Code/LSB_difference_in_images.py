# https://nisaruj.medium.com/spot-the-difference-secplayground-christmas-ctf-2023-writeup-bf7bdb9ef40c
# knitting gir
from PIL import Image

im = Image.open('flowers.png', 'r')

pix_val = list(im.getdata())

im2 = Image.open('dylans_flowers.png', 'r')

pix_val2 = list(im2.getdata())
flag = ''
for i in range(len(pix_val)):
    one = pix_val[i]
    two = pix_val2[i]
    
    # bcs in the "SUB" mode of stegsolve's "combine images" we see a small line of different colored pixels,
    # she just stopped it at 35 from logically looking at the image.
    if i <= 35:
        print(i)
        
        # iterating every channel (if it's in RGBA mode)
        for j in range(4):
            print(bin(one[j]), bin(two[j]))
            # getting the least significant bit (last digit in the binary string hence the [-1] ):
            flag += bin(two[j])[-1]
         
print(flag)
