import random

def GenerateLowerTriangularMatrix(size):
    LTMatrix = [] #ma tran tam giac duoi

    for i in range(0, size):
        vector = []
        for j in range(0, size):
            if (j == i): #a[i][j] = 1 neu j = i
                vector.append(1)
            elif (j > i): #a[i][j] = 0 neu j > i
                vector.append(0)
            else: #a[i][j] = 0 hoac = 1 neu j <= i
                vector.append(random.choice([0, 1]))

        LTMatrix.append(vector)
    return LTMatrix

def GenerateUpperTriangularMatrix(size):
    UTMatrix = [] #ma tran tam giac tren

    for i in range(0, size):
        vector = []
        for j in range(0, size):
            if (j == i): #a[i][j] = 1 neu j = i
                vector.append(1)
            elif (j < i): #a[i][j] = 0 neu j < i
                vector.append(0)
            else: #a[i][j] = 0 hoac = 1 neu j > i
                vector.append(random.choice([0, 1]))

        UTMatrix.append(vector)
    return UTMatrix


def GenerateIvertibleMatrix(size): #tinh ma tran kha nghich bang cach lay ma tran tam giac tren nhan ma tran tam giac duoi
    LTMatrix = GenerateLowerTriangularMatrix(size)
    UTMatrix = GenerateUpperTriangularMatrix(size)
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


def FindInverseMatrix(LTMatrix, UTMatrix):
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

def Encrypt(m, key):
    C = []
    size = len(key)

    temp = len(m) % size
    if temp != 0:
        for i in range (temp, size): #them so 0 vao sau cung
            m.append(0)

    i = 0
    while (i < len(m)): #vong lap ma hoa list, ma hoa tung cum size phan tu
        for j in range(0, size):
            temp = 0
            for k in range(0, size):
                temp += key[j][k] * m[i + k]
            C.append(temp % 256)
        i += size
    return C

def Decrypt(c, Ikey):
    M = []
    i = 0
    size = len(Ikey)

    while (i < len(c)):
        for j in range(0, size):
            temp = 0
            for k in range(0, size):
                temp += Ikey[j][k] * c[i + k]
            M.append(temp % 256)
        i += size
    return M


#Python program to read


#importing PIL
from PIL import Image

# Read image
img = Image.open('RSA.jpg')

pixels = img.load()

#for i in range(img.size[0]):
#    for j in range(img.size[1]):
#        r, b, g, t = pixels[i,j]
#        avg = int(round((r + b + g) / 3))
#        pixels_new[i,j] = (avg, avg, avg, t)
#new_img.show()

lists = []

for i in range(img.size[0]):
    elem = []
    for j in range(img.size[1]):
        r, b, g = pixels[i,j]
        elem += [r, b, g]
    lists.append(elem)

key, L, U = GenerateIvertibleMatrix(4)

Ikey = FindInverseMatrix(L, U)

def img_encrypt(img_file):
    img = Image.open(img_file)
    new_img = Image.new(img.mode, img.size)
    pixels = new_img.load()

    for i in range(img.size[0]):
        c = Encrypt(lists[i], key)
        for j in range(img.size[1]):
            pixels[i,j] = (c[j*3], c[j*3+1], c[j*3+2])
    return new_img

new_img = img_encrypt('RSA.jpg')
new_img.show()
