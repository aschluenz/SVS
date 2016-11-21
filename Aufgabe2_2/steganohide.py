from PIL import Image
from xtea import *
import binascii,sys,hashlib,hmac

def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)

def hex2rgb(hexcode):
    return tuple(map(ord, hexcode[1:].decode('hex')))

def str2bin(message):
    binary = bin(int(binascii.hexlify(message), 16))
    return binary[2:]

def bin2str(binary):
    message = binascii.unhexlify('%x' % (int('0b' + binary,2)))

def readTextFile(fileName):
    message = open(fileName,'r').read()
    return message

def encode(hexcode, number):
    if hexcode[-1] in ('0','1','2','3','4','5'):
        hexcode = hexcode[:-1] + number
        return hexcode
    else:
        return None

def decode(hexcode):
    if hexcode[-1] in ('0','1'):
        return hexcode[-1]
    else:
        return None

def hide(imagefile, message):
    img = Image.open(imagefile)
    #end of message
    binary = str2bin(message) + '1111111111111110'
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        data = img.getdata()

        newData = []
        number = 0
        temp = ''
        for item in data:
            if(number < len(binary)):
                new_pixel = encode(rgb2hex(item[0],item[1],item[2]), binary[number])
                if new_pixel == None:
                    newData.append(item)
                else:
                    r,g,b = hex2rgb(new_pixel)
                    newData.append((r,g,b,255))
                    number += 1
            else:
                newData.append(item)
        img.putdata(newData)
        img.save(imagefile + '.ste', "BMP")
        return "Done!"
    return "Wrong Image Mode, couldn't Hide"

def show(imagefile):
    img = Image.open(imagefile)
    binary = ''

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        data = img.getdata()

        for item in data:
            number = decode(rgb2hex(item[0],item[1],item[2]))
            if number == None:
                pass
            else:
                binary = binary + number
                if (binary[-16] == '1111111111111110'):
                    print ("Success")
                    return bin2str(binary[:-16])

        return bin2str(binary)
    return "Wrong Image Mode, Couldn't Show Text"

def hashSHA256(message):
    hash_object = hashlib.sha256()
    hash_object.update(message)
    return hash_object.hexdigest()

def xteaEncrypt(message, key):
    print('keylength:', len(key))
    text = message*8
    x = new(key,mode=MODE_CFB, IV='12345678')
    c = x.encrypt(text)
    return c

def xteaDecrypt(message,key):
    x = new(key,mode=MODE_CFB, IV='12345678')
    message = x.decrypt(message)
    return message

def main(argv):
    parameter_len = len(argv)
    #macpassword = '123456fdgkdfjhkgskkjlshjksdf'
    #key = 'what ever'
    #textfile = 'text.txt'

    print(len(argv))
    #encrypt
    if parameter_len == 7:
        if(argv[0] == '-e' and argv[1] == '-m' and argv[2] != '' and argv[3] == '-k' and argv[4] != '' and argv[5] != '' and argv[6] != ''):
            mac_pw = argv[2]
            key = argv[4]
            text = readTextFile(argv[5])
            imgfile = argv[6]

            hashedMac = hashSHA256(mac_pw)
            lengthMac = len(hashedMac)
            # SHA256pw + text string
            new_message = hashedMac + text
            print(hashedMac)
            print(text)
            print(new_message)
            #SHA256 from key
            hashedkey = hashSHA256(key)

            encryptedText = xteaEncrypt(new_message,hashedkey[:16])
            #hide text in the image
            hide(imagefile,encryptedText)

            print (argv)
        else:
            print('usage to encrypt: ', 'aesteganohide.py -e -m macpassword -k password text.txt bild.bmp')
    #decrypt
    elif parameter_len == 6:
        if(argv[0] == '-d' and argv[1] == '-m' and argv[2] != '' and argv[3] == '-k' and argv[4] != '' and argv[5] != ''):
            #get text from image
            text = show(argv[5])
            #hash mac pw
            hashedMac = hashSHA256(argv[2])

            hashedkey = hashSHA256(argv[4])

            decrypted_message = xteaDecrypt(text)
            #check Mac
            if(decrypted_message[0:16] == hashedMac):
                print ("Message: ", decrypted_message[16:])
                sys.exit(0)
            else:
                print('WRONG MACPASSWORD')
                sys.exit(1)

        else:
            print('usage to decript: ', 'aesteganohide.py -d -m macpassword -k password bild.bmp.sae')

    else:
        print('usage to decript: ', 'aesteganohide.py -d -m macpassword -k password bild.bmp.sae')
        print('usage to encrypt: ', 'aesteganohide.py -e -m macpassword -k password text.txt bild.bmp')

if __name__ == "__main__":
    main(sys.argv[1:])
