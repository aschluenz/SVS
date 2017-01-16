from PIL import Image
import hashlib, hmac, argparse
import xtea

def stringToBits(string):
    bits = []
    for char in string:
        bin_t = bin(ord(char))[2:] #remove b0
        bits.append(bin_t.zfill(8))
    return "".join(bits)

def bitsToString(bits):
    chars = []
    for i in range(0,len(bits), 8):
        char = chr(int(b[i:i +8], 2))
        chars.append(char)
    return "".join(chars).rstrip(char(0))

def writeBitsToImage(bits, image):
    bits += '1'
    if len(bits) > (image.size[0] * image.size[1]) * 3:
        print("Text is to long, text will be cropped")
    image_pixelmap = image.load()
    imageSize0 = image.size[0]
    imageSize1 = image.size[1]
    for x in range(imageSize0):
        for y in range(imageSize1):
            r,g,b = image_pixelmap[x,y]
            r -= r % 2
            g -= g % 2
            b -= b % 2
            image_pixelmap[x,y] = r,g,b
    for pixel_index in range(0, imageSize0 * imageSize1):
        x = pixel_index % imageSize1
        y = int(pixel_index / imageSize1)
        bit_triple = bits[pixel_index * 3: pixel_index * 3 + 3]
        if len(bit_triple) == 0:
            break
        bit_triple = bit_triple.ljust(3,"0")
        r,g,b = image_pixelmap[x,y]
        r += int(bit_triple[0])
        g += int(bit_triple[1])
        b += int(bit_triple[2])
        image_pixelmap[x,y] = r,g,b
    return image

def readBitsFromImage(image):
    bits = []
    image_pixel = image.load()
    print(image_pixel)
    imageSize0 = image.size[0]
    print imageSize0
    imageSize1 = image.size[1]
    print imageSize1
    pixelsum = imageSize0 * imageSize1
    print("pixel sum: ", pixelsum)
    for pixel_index in range(0, imageSize0 * imageSize1):
        #print("pixel index:", pixel_index )
        x = pixel_index % imageSize1
        #print ("x:",x)
        y = int(pixel_index / imageSize1)
        #print ("y:", y)
        r,g,b = image_pixel[x,y]
        bits.append(r % 2)
        bits.append(g % 2)
        bits.append(b % 2)
    bits = [str(x) for x in bits]
    bits = ''.join(bits).rstrip('0')
    return bits[:-1] #remove last one

def generateHmacSha256(key, text):
    key_hash = hashlib.sha256(key.encode('utf-8')).digest()
    return hmac.new(key_hash, text.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

def checkHmacSha256(hmac, key, text):
    return generateHmacSha256(key,text) == hmac

def encrypt (key,bits):
    key_hash = hashlib.sha256(key.encode('utf-8')).digest()[0:16]
    print ('key_hash', hashlib.sha256(key.encode('utf-8')).digest())
    print ("Keyhash",key_hash)
    return xtea.encrypt(key_hash, bits)

def decrypt (key, bits):
    key_hash = hashlib.sha256(key.encode('utf-8')).digest()[0:16]
    return xtea.decrypt(key_hash,bits)

def main(args):
    keyHmac = args.m
    keyXtea = args.k
    image = Image.open(args.imagePath[0])
    imageOutpuPath = args.imagePath[0] + '.sae'

    if args.e:
        with open(args.textPath, 'r') as f:
            text = "".join(f.readlines())
        generatedHmac = generateHmacSha256(keyHmac, text)
        textWithHmacBits = stringToBits(generatedHmac + text)
        textWithHmacXteaBits = encrypt(keyXtea,textWithHmacBits)
        imageOut = writeBitsToImage(textWithHmacXteaBits, image)
        image.save(imageOutpuPath, 'BMP')

    if args.d:
        print(image)
        bits = readBitsFromImage(image)
        bits = decrypt(keyXtea,bits)

        extractedHmac = bitsToString(bits[0:512])
        extractedText = bitsToString(bits[512:])
        print('Mac Test: ', checkHmacSha256(extractedHmac, keyHmac,extractedText))
        print(extractedText)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', help='encrypt',action='store_true')
    parser.add_argument('-d', help='decrypt',action='store_true')
    parser.add_argument('-m', required=True, help='MAC key')
    parser.add_argument('-k', required=True,help='Crypto K')
    parser.add_argument('textPath', nargs='?')
    parser.add_argument('imagePath', nargs=1)
    args = parser.parse_args()
    main(args)
