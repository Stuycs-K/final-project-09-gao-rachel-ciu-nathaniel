# *** Code from https://rosettacode.org/wiki/MD5/Implementation#Python ***
import math

rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

constants = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

functions = 16*[lambda b, c, d: (b & c) | (~b & d)] + \
            16*[lambda b, c, d: (d & b) | (~d & c)] + \
            16*[lambda b, c, d: b ^ c ^ d] + \
            16*[lambda b, c, d: c ^ (b | ~d)]

index_functions = 16*[lambda i: i] + \
                  16*[lambda i: (5*i + 1)%16] + \
                  16*[lambda i: (3*i + 5)%16] + \
                  16*[lambda i: (7*i)%16]

def left_rotate(x, amount):
    print("FAMK")
    print(md5_to_hex(x))
    x &= 0xFFFFFFFF
    print("In left rotate")
    print("First shift")
    print((x<<amount))
    print("Second shift")
    print((x>>(32-amount)))
    print("The or")
    print((x<<amount) | (x>>(32-amount))) 
    return ((x<<amount) | (x>>(32-amount))) & 0xFFFFFFFF

def md5(message):

    message = bytearray(message) #copy our input into a mutable buffer
    orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    message.append(0x80)
    while len(message)%64 != 56:
        message.append(0)
    message += orig_len_in_bits.to_bytes(8, byteorder='little')

    hash_pieces = init_values[:]

    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:chunk_ofst+64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i) # refers to word order
            print("\nindex function")
            print(index_functions[i](i))

            print("bitwise result")
            print(md5_to_hex(f)) # equals the result of just bitwise 

            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4*g:4*g+4], byteorder='little')

            print("FandA")
            print( md5_to_hex(a + f))

            print("WordList")
            print(md5_to_hex(int.from_bytes(chunk[4*g:4*g+4], byteorder='little')))

            print("FAM")
            print(md5_to_hex(a + f + int.from_bytes(chunk[4*g:4*g+4], byteorder='little'))) 
            # print("Actually word")
            # print(md5_to_hex(int.from_bytes(chunk[4*g:4*g+4], byteorder='little')))
            
            print("FAMK")
            print(md5_to_hex(to_rotate)) # should = FAMK
            # rotate here means shifting

            print("rotate_amount")
            print(rotate_amounts[i])


            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
            # new_b should = FAMKSB

            print("FAMKS")
            print(md5_to_hex(left_rotate(to_rotate, rotate_amounts[i])))

            print("FAMKSB")
            print(md5_to_hex(new_b))


            a, b, c, d = d, new_b, b, c

            print("a: " + md5_to_hex(a))
            print("b: " + md5_to_hex(b))
            print("c: " + md5_to_hex(c))
            print("d: " + md5_to_hex(d))
            
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF
        
    
    return sum(x<<(32*i) for i, x in enumerate(hash_pieces))
        
def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='little'))

def to_hex(value): 
    return '{:02x}'.format(value)

if __name__=='__main__':
    demo =[b"Hello World"]
    # demo = [b"", b"a", b"abc", b"message digest", b"abcdefghijklmnopqrstuvwxyz",
    #         b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    #         b"12345678901234567890123456789012345678901234567890123456789012345678901234567890"]
    for message in demo:
        print(md5_to_hex(md5(message)),' <= "',message.decode('ascii'),'"', sep='')

