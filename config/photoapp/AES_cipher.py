import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding
from PIL import Image
from six import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class AESCipher(object):
    def __init__(self, key):
       self.key = (hashlib.md5(key.encode('utf-8')).hexdigest()).encode('utf-8')

    def encrypt(self, img_file):
       iv = Random.new().read(AES.block_size)
       cipher = AES.new(self.key, AES.MODE_CBC, iv)

       # Opens image and converts it to RGB format for PIL 
       img = Image.open(img_file)
       data = img.convert("RGB").tobytes() 
       original = len(data)
       data_enc = cipher.encrypt(Padding.pad(data, AES.block_size, 'pkcs7'))
       img_enc = convert_to_RGB(data_enc[:original])  
       im2 = Image.new(img.mode, img.size)
       im2.putdata(img_enc) 
       img_file.seek(0)
       im2.save(img_file)
       img_file.seek(0)

    def decrypt(self, enc):
      #  enc = base64.b64decode(enc.encode('utf-8'))
       iv = enc[:AES.block_size]
       cipher = AES.new(self.key, AES.MODE_CBC, iv)
       data = cipher.decrypt(Padding.unpad(enc[AES.block_size:], AES.block_size, 'pkcs7'))
       return data

# Maps the RGB  
def convert_to_RGB(data): 
    r, g, b = tuple(map(lambda d: [data[i] for i in range(0,len(data)) if i % 3 == d], [0, 1, 2])) 
    pixels = tuple(zip(r,g,b)) 
    return pixels 