sol1
import base64
#chaine hexa
hex_string="49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
#conver hex to byte 
to_byte=bytes.fromhex(hex_string)
#conver bytes  to b64
b64=base64.b64encode(to_byte)
print(b64)

