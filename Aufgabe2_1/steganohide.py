from PIL import Image
import binascii,sys

def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)

def hex2rgb(hexcode):
    return tuple(map(ord, hexcode[1:].decode('hex')))

def str2bin(message):
    binary = bin(int(binascii.hexlify(message), 16))
    return binary[2:]

def readTextFile(fileName):
    message = open(fileName,'r').read()
    return message

def encode(hexcode, number):
    if hexcode[-1] in ('0','1','2','3','4','5'):
        hexcode = hexcode[:-1] + number
        return hexcode
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

def main(argv):
    textfile = sys.argv[1]
    message = readTextFile(textfile)
    imagefile = sys.argv[2]

    hide(imagefile,message)

if __name__ == "__main__":
	main(sys.argv[1:])
