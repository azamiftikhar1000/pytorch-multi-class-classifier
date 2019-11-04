from PIL import Image
import os, sys

path = "img/"
path2="img2/"
dirs = os.listdir( path )

def resize():
    count=0
    for item in dirs:
      dirs2= os.listdir( path+item )
      for item2 in dirs2:
        if os.path.isfile(path+item+'/' + item2 ):
            im = Image.open(path+item+'/'+item2 )
            f, e = os.path.splitext(path+item+'/'+item2)
            
            # Create target Directory if don't exist
            try:
                 
                imResize = im.resize((224,224), Image.ANTIALIAS)
                count=count+1
                imResize.save(path2+f +'.jpg', quality=100)
                print(count)
            except:
              print("error error")
              continue
            
resize()
