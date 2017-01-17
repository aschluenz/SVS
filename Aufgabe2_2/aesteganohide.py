import itertools
import os, sys,hashlib, hmac,argparse
from xtea import *

def hideText(textfile, imagefile, args):
    header, data = readImageFile(imagefile)
    secretText = readText(textfile)
    bits = bitgenerator(secretText, args)

    Buffer = []
    Buffer.append(header)

    for byte in data:
        try:
            #http://stackoverflow.com/questions/6059454/replace-least-significant-bit-with-bitwise-operations
            Buffer.append(chr((ord(byte) & ~1) | bits.next()))
        except StopIteration:
            Buffer.append(byte)
    writeBytes('%s.sae' % imagefile, Buffer)

def showText(imagefile, args):
    image = open(imagefile, 'rb')
    header = image.read(55)
    macData = image.read(64)

    macDataLastBits = bufferGetLastBits(macData)

    macDataLen = bufferToInt(macDataLastBits)

    macDataBytes = image.read(macDataLen)

    image.close()

    macAndTextBits = bufferGetLastBits(macDataBytes)
    print('macAndTextBits', macAndTextBits)

    xteaPW = hashlib.sha256(args.password).digest()[0:16]
    print("xteaPW", xteaPW)
    macDataDecrypted = xteaCfbDecrypt(bufferToString(macAndTextBits), xteaPW)
    print("macDataDecrypted",macDataDecrypted[0:32])
    mac = macDataDecrypted[0:32]
    data = macDataDecrypted[32:]

    return(header,mac,data)

def readImageFile(fileName):
    image = open(fileName, 'rb')
    header = image.read(55)
    data = image.read()
    image.close()
    return (header,data)

def readText(fileName):
    file = open(fileName, 'rb')
    text = file.read()
    file.close()
    return text.strip()

def writeBytes(fileName, bytes):
    file = open(fileName, 'wb')
    file.write(''.join(bytes))
    file.close()

def bitgenerator(secret,args):
    secret = generateMAC(secret, args.macpassword) + secret

    xteaPW = hashlib.sha256(args.password).digest()[0:16]
    secret = xteaCfbEncrypt(secret, xteaPW)
    print xteaPW
    print secret
    return itertools.chain(
        (int(bit) for bit in byteToString(len(list(stringToBits(secret)))).zfill(64)),
        stringToBits(secret),
    )

def stringToBits(byteBuffer):
    for byte in map(ord, byteBuffer):
        for bit in byteToString(byte).zfill(8):
            yield int(bit)

def byteToString(byteBuffer):
    return str(byteBuffer) if byteBuffer <= 1 else byteToString(byteBuffer >> 1) + str(byteBuffer & 1)

def chunks(l,n):
    #Source: http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def bufferToString(byteBuffer):
    output = []
    for chunk in chunks(byteBuffer, 8):
        output.append(chr(int(''.join(map(str, chunk)), 2)))

    return (''.join(output)).strip()

def bufferToInt(byteBuffer):
    return int(''.join(map(str, byteBuffer)), 2)

def bufferGetLastBits(byteBuffer):
    lastbitsonly = []
    for byte in byteBuffer:
        lastbitsonly.append(ord(byte) & 1)
    return lastbitsonly

def generateMAC(message, password):
    return hmac.new(key=password,msg=message, digestmod=hashlib.sha256).digest()

def checkMacs(mac, data, password):
    #print mac
    #print generateMAC(data,password)
    return mac == generateMAC(data,password)


def main(args):
    imageFile = args.imagePath[0]
    print imageFile
    if args.e:
        textFile = args.textPath
        print textFile
        hideText(textFile, imageFile, args)
        print('Text is hidden in Image!')

    if args.d:

        header, mac, data = showText(imageFile, args)

        if not checkMacs(mac,data, args.macpassword):
            print ('MAC password is not correct')
            sys.exit(1)

        print('Text from image: ',data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', help='encrypt',action='store_true', dest='e')
    parser.add_argument('-d', help='decrypt',action='store_true', dest='d')
    parser.add_argument('-m', required=True, help='MAC key', dest='macpassword')
    parser.add_argument('-k', required=True,help='Crypto K', dest='password')
    parser.add_argument('textPath', nargs='?')
    parser.add_argument('imagePath', nargs=1)
    args = parser.parse_args()
    main(args)
