import random
from PIL import Image
import base64
import io
from cipher.RSA import RSA

class Matrix:
    @staticmethod
    def Generate_LMatrix(size):
        LTMatrix = [] #ma tran tam giac duoi

        for i in range(0, size):
            vector = []
            for j in range(0, size):
                if (j == i): #a[i][j] = 1 neu j = i
                    vector.append(1)
                elif (j > i): #a[i][j] = 0 neu j > i
                    vector.append(0)
                else: #a[i][j] = 0 hoac = 1 neu j <= i
                    vector.append(random.choice([1, 2]))

            LTMatrix.append(vector)
        return LTMatrix

    @staticmethod
    def Generate_UMatrix(size):
        UTMatrix = [] #ma tran tam giac tren

        for i in range(0, size):
            vector = []
            for j in range(0, size):
                if (j == i): #a[i][j] = 1 neu j = i
                    vector.append(1)
                elif (j < i): #a[i][j] = 0 neu j < i
                    vector.append(0)
                else: #a[i][j] = 0 hoac = 1 neu j > i
                    vector.append(random.choice([1, 2]))

            UTMatrix.append(vector)
        return UTMatrix

    @staticmethod
    def Generate_IMatrix(size): #tinh ma tran kha nghich bang cach lay ma tran tam giac tren nhan ma tran tam giac duoi
        LTMatrix = Matrix.Generate_LMatrix(size)
        UTMatrix = Matrix.Generate_UMatrix(size)
        size = len(LTMatrix)
        Imatrix = []

        for i in range(0, size):
            vector = []
            for j in range(0, size):

                element = 0
                for k in range(0, size): #vong lap de tinh phan tu thu i, j cua ma tran kha nghich
                    element += LTMatrix[i][k] * UTMatrix[k][j]

                vector.append(element % 256)
            Imatrix.append(vector)
        return Imatrix, LTMatrix, UTMatrix

    @staticmethod
    def Find_IMatrix(LTMatrix, UTMatrix):
        size = len(LTMatrix)

        Y = [] #LTMatrix * Y^T = I
        X = [] #UTMatrix * X = Y
        for i in range(0, size):
            X.append([])

        for i in range(0, size): #tinh ma tran Y theo cong thuc
            vector = []
            if (i == 0):
               vector.append(1)
            else:
                vector.append(0)
            for j in range(1, size):
                temp = 0
                for k in range(0, j):
                    temp += vector[k] * LTMatrix[j][k]
                if j == i:
                    vector.append((1 - temp) % 256)
                else:
                    vector.append((0 - temp) % 256)
            Y.append(vector)

        for i in range(0, size): #tinh ma tran X theo cong thuc
            vector = []
            vector.append(Y[i][size - 1])
            for j in reversed(range(0, size - 1)):
                temp = 0
                for k in reversed(range(j + 1, size)):
                    temp += vector[size - 1 - k] * UTMatrix[j][k]

                vector.append((Y[i][j] - temp) % 256)
            for j in range(0, size):
                X[size - 1 - j].append(vector[j])

        return X

    @staticmethod
    def matrix2string(key):
        Ikeystring=""
        for i in key:
            row=""
            for j in i:
                row+=str(j)
                row+=";"
            Ikeystring+=row
        return(Ikeystring[:-1])

    @staticmethod
    def string2matrix(string):
        Ikeymatrix=[]
        row=[]
        index=""
        string.replace('[|]', '')
        for i in range(len(string)):
            if string[i]==";":
                row.append(int(index))
                index=""
            else:
                index+=string[i]
            if len(row)==20:
                Ikeymatrix.append(row)
                row=[]
            if i==len(string)-1:
                row.append(int(string[i]))
                Ikeymatrix.append(row)
                break
        return Ikeymatrix



class AESCipher:

    def __init__(self):
        pass
        # self.key = key
        # self.Ikey = Ikey
        
    def Encrypt(self, m, key): #ma hoa 1 mang
        C = []
        size = len(key)

        i = 0
        while (i < len(m)): #vong lap ma hoa list, ma hoa tung cum size phan tu
            if i + size > len(m):
                for j in range(i, len(m)):
                    C.append(m[j])
                break
            for j in range(0, size):
                temp = 0
                for k in range(0, size):
                    temp += key[j][k] * m[i + k]
                C.append(temp % 256)
            i += size
        return C

    def Decrypt(self, c, Ikey): #giai ma 1 mang
        M = []
        size = len(Ikey)

        i = 0
        while (i < len(c)):
            if i + size > len(c):
                for j in range(i, len(c)):
                    M.append(c[j])
                break
                
            for j in range(0, size):
                temp = 0
                for k in range(0, size):
                    temp += Ikey[j][k] * c[i + k]
                M.append(temp % 256)
            i += size
        return M

    def img_encrypt(self, img_file, key): #ma hoa anh
        img = Image.open(img_file)
        pixels = img.load()

        lists = [] #chuyen doi pixel tung dong thanh r,b,g
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                r = pixels[i,j][0]
                b = pixels[i,j][1]
                g = pixels[i,j][2]
                lists += [r, b, g]
        
        c = self.Encrypt(lists, key)
        count = 0
        for i in range(img.size[0]): #ma hoa
            for j in range(img.size[1]):
                pixels[i,j] = (c[count*3], c[count*3+1], c[count*3+2])
                count += 1
                
        img_file.seek(0)
        img.save(img_file, 'PNG')
        img_file.seek(0)

    def img_decrypt(self, img_file, Ikey): #giai ma anh
        img = Image.open(img_file)
        pixels = img.load()

        lists = [] #chuyen doi pixel tung dong thanh r,b,g
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                r = pixels[i,j][0]
                b = pixels[i,j][1]
                g = pixels[i,j][2]
                lists += [r, b, g]
        
        m = self.Decrypt(lists, Ikey)
        count = 0
        for i in range(img.size[0]): #giai ma
            for j in range(img.size[1]):
                pixels[i,j] = (m[count*3], m[count*3+1], m[count*3+2])
                count += 1
                
        return img


def DecryptImg(photo, D):
    Ikey = Matrix.string2matrix(photo.key)
    N = photo.submitter.userkey.N
    RSA_cipher = RSA()
    Ikey = RSA_cipher.decrypt(Ikey, D, N)
    cipher = AESCipher()
    img_data = cipher.img_decrypt(photo.image.path, Ikey)
    #img_data = Image.open(self.get_photo().image.path)
    data = io.BytesIO()
    img_data.save(data, "PNG")
    encoded_img = base64.b64encode(data.getvalue())
    decoded_img = encoded_img.decode('utf-8')
    return decoded_img