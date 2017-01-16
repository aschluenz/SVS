from PIL import Image
from xtea3 import *
import os,sys,hashlib,hmac,struct, binascii,itertools,argparse,random

mac_passw = ""
password = ""
text_file = ""
image_file = ""
do_xtea_encrypt = True



def args_parser():

    return vars(args)

def generateIV():
    string = 'b' + '"' + '12345678' + '"'
    return string

def get_mac(in_text, key):
    dig = hmac.new(key.encode(), digestmod=hashlib.sha256)
    dig.update(in_text.encode())
    generated_mac = str(dig.hexdigest())
    print ("Ausgabe get_mac: ", generated_mac)
    print ("key len", len(generated_mac))
    return generated_mac

def compare_macs(in_text,in_mac,mac_pw_in):
    dig = hmac.new(mac_pw_in.encode(), digestmod=hashlib.sha256)
    dig.update(in_text.encode())
    return dig.hexdigest() == in_mac

def encrypt(mac_passw,password,text_file,image_file,do_xtea_encrypt,img):
    file = open(text_file, "r")
    text = file.read()
    file.close()

    max_chars = (img.size[0])

    mac = get_mac(text, mac_passw)
    text_len = str(len(mac) + len(text)).rjust(16, '0')

    if do_xtea_encrypt:
        textWithMac = (mac + text)
        key = (password.ljust(16,'0')).encode()
        #key =  (get_mac("",password)).encode()
        
        print("key: ", len(key))
        
        #x = new(key,mode=MODE_CFB,IV=generateIV())
        x = new(key , mode=MODE_CFB, IV=b"12345678")
        encryptedText = x.encrypt(textWithMac.encode())
        encryptedText = binascii.a2b_hex(text_len) + encryptedText
        encryptedText = str(binascii.b2a_hex(encryptedText))[2:]
        encryptedText = encryptedText[:len(encryptedText)-1]

    else:
        encryptedText = text_len + mac + text

    decryptText = [ord(x) for x in encryptedText]
    bin_text_bits = [bin(x)[2:].rjust(7,'0') for x in decryptText]

    img_pixels = [(x >> 1) << 1 for x in list(img.getdata())]

    bin_text = [int(x) for x in list(itertools.chain(*list(bin_text_bits)))]

    new_image_list = []

    for i in range (0, len(bin_text)):
        new_image_list.append(img_pixels[i] | bin_text[i])

    for i in range(len(bin_text), len(img_pixels)):
        new_image_list.append(img_pixels[i] | random.randint(0,1))

    new_image = Image.new('L', (img.size[0], img.size[1]))
    new_image.frombytes(bytes(new_image_list))
    new_image.save("bild.bmp.sae")
    new_image.show()

def decrypt(mac_passw,password,text_file,image_file,do_xtea_encrypt):

    bin_text_list = [x & 1 for x in list(img.getdata())]
    ascii_bit_len = 7
    bin_text_bits = [bin_text_list[i:i+ascii_bit_len] for i in range (0, len(bin_text_list), ascii_bit_len)]
    bin_text = ["".join(map(str,x)) for x in bin_text_bits]
    text_decrypt = [int(i,2) for i in bin_text]
    encryptedText = [chr(x) for x in text_decrypt]

    text_len = ""
    for x in encryptedText[:16]:
        text_len += x
    text_len = int(text_len)
    encryptedText = encryptedText[16:(16+ text_len*2)]

    if do_xtea_encrypt:
        encryptedText = "".join(map(str, encryptedText))
        key = (password.ljust(16,'0')).encode()
        x = new(key,MODE_CFB, IV=generateIV())
        plainText = x.decrypt(binascii.a2b_hex(encryptedText))
        mac = plainText[:64]
        mac = [chr(x) for x in mac]
        mac = "".join(map(str,mac))

        plainText = plainText[64:64+text_len]
        plainText = [chr(x) for x in plainText]
        plainText = "".join(map(str, plainText))

    else:
        plainText = encryptedText
        mac = ""
        for x in plainText[:64]:
            mac += x
        plainText = plainText[16+64:16+64+text_len]

    textDecrypted = ""

    for x in plainText:
        textDecrypted += x
    if not(compare_macs(textDecrypted, mac,mac_pw)):
        print("mac comparison failed, text has been modified!")
    else:
        print("text has been authenticated")
    print(textDecrypted)
    pass

def test():
    print mac_passw
    print password
    print text_file
    print image_file



def main(args):
    mac_passw = args.get('m')
    password = args.get('k')
    text_file = args.get('txt')
    image_file = args.get('img')
    test()
    img = Image.open(image_file)
    img_channels = len(img.split())

    if img_channels > 1:
        img = img.split()[0]
    if args.get('encrypt'):
        encrypt(mac_passw,password,text_file,image_file,do_xtea_encrypt,img)
    elif args.get('decrypt'):
        decrypt(mac_passw,password,text_file,image_file,do_xtea_encrypt)
    else:
        print("either '-e' or '-d' must be present in arguments, exiting")
        exit(0)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers')
    parser.add_argument('-encrypt', '-e', action='store_true')
    parser.add_argument('-decrypt', '-d', action='store_true')
    parser.add_argument('-m', metavar='MAC_PASSW', help='password for mac-verification')
    parser.add_argument('-k', metavar='PASSWORD',help='password for text en-/decryption')
    parser.add_argument('-txt', default='text.txt',help='plain text, which will be embedded in image')
    parser.add_argument('-img', default='bild.bmp',help='target image')
    args = parser.parse_args()
    main(vars(args))
