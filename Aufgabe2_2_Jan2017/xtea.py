import random

num_Cycles = 32

def randomIV():
    bits = []
    for i in range(0, 64):
        number = int(round(random.random()))
        bits.append(str(number))
    #     bits.append(str(round(random.random())))
    return ''.join(bits)

def encrypt(key,bits):
    cypher_blocks = []
    blocks = splitIntoBlock(bits)
    for block in blocks:
        if len(cypher_blocks) == 0:
            iv = randomIV()
            cypher_block = encryptOneBlock(key, iv)
            cypher_blocks.append(iv)
        else:
            cypher_block = encryptOneBlock(key, cypher_blocks[-1:][0])
        cypher_blocks.append(XOR(block, cypher_block))
    return "".join(cypher_blocks)

def decrypt(key, cypherbits):
    cypher_blocks = splitIntoBlock(cypherbits)
    iv = cypher_blocks[0]
    cypher_blocks = cypher_blocks[1:]
    blocks = []
    last_cypher_block = iv
    for cypher_block in cypher_blocks:
        block = encryptOneBlock(key, last_cypher_block)
        blocks.append(XOR(block, cypher_block))
        last_cypher_block = cypher_block
    return "".join(blocks)

def encryptOneBlock(key, block):
    assert (len(block) == 64)
    v0 = int(block[0:32], 2)
    print ("v0", v0)
    v1 = int(block[32:64], 2)
    print ("v1", v1)
    print ("key: ", key[0:4])


    k = [from_bytes(key[0:4],big_endian = True),
         from_bytes(key[4:8],big_endian = True),
         from_bytes(key[8:12],big_endian = True),
         from_bytes(key[12:16],big_endian = True)]
    delta = 0x9E3779B9
    sum = 0
    for i in range(0, num_Cycles):
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + k[sum % 3])
        sum += delta
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + k[(sum >> 11) % 3])

    block = IntToBits(v0) + IntToBits(v1)
    return block

def splitIntoBlock(bits):
    blocks = []
    for i in range(0, len(bits), 64):
        block = bits[i:i + 64]
        if len(block) == 64:
            print("block in splittblocks", len(block))
            blocks.append(block)
        else:
            pad = '0' * (64 - len(block) % 64)
            block += pad
            print ("blocks aus else: ", len(block))
            blocks.append(block)
    return blocks

def XOR(a,b):
    XOR = []
    for bit_a, bit_b in zip(a,b):
        XOR.append(str(int(bit_a) ^ int(bit_b)))
    return "".join(XOR)

def IntToBits(i):
    return bin(i)[2:]

def from_bytes (data, big_endian = True):
    if isinstance(data, str):
        data = bytearray(data)
    if big_endian:
        data = reversed(data)
    num = 0
    for offset, byte in enumerate(data):
        num += byte << (offset * 8)
    return num
