import itertools
import os
import sys

def hide(textFile, imageFile):
    header, data = readImageFile(imageFile)
    secret = readText(textFile)
    lastbits = bitGenerator(secret)

    buffer = []
    buffer.append(header)

    for byte in data:
        try:
            #http://stackoverflow.com/questions/6059454/replace-least-significant-bit-with-bitwise-operations
            buffer.append(chr((ord(byte) & ~1) | lastbits.next()))
        except StopIteration:
            buffer.append(byte)

    writeBytes('%s.ste' % imageFile, buffer)

def bitGenerator(message):
    return itertools.chain(
        (int(bit) for bit in byteToString(len(list(stringToBits(message)))).zfill(64)),
        stringToBits(message),
        )

def stringToBits(byteBuffer):
    for byte in map(ord, byteBuffer):
        for bit in byteToString(byte).zfill(8):
            yield int(bit)

def byteToString(byteBuffer):
    return str(byteBuffer) if byteBuffer <= 1 else byteToString(byteBuffer >> 1) + str(byteBuffer & 1)

def readText(fileName):
    file = open(fileName, 'rb')
    text = file.read()
    file.close()
    return text.strip()

def readImageFile(fileName):
    image = open(fileName, 'rb')
    header = image.read(55)
    data = image.read()
    image.close()
    return (header,data)

def writeBytes(fileName, bytes):
    file = open(fileName, 'wb')
    file.write(''.join(bytes))
    file.close()

def main():
    if len(sys.argv) != 3:
        print 'Usage: %s <text-file> <bmp-file>' % __file__
        sys.exit(1)

    textFile = os.path.abspath(sys.argv[1])
    imageFile = os.path.abspath(sys.argv[2])

    hide(textFile,imageFile)

if __name__ == "__main__":
    main()
