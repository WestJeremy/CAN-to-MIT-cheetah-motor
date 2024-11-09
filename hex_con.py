import numpy as np
import math


p1=0X74
p2=0XCF

lim = 4*np.pi


print("first",p1)
print("second",p2)

out=(p1)<<8^(p2)
print("total:",out)


print("convert to numeral deg",math.degrees((out/(2**16-1) * 2*lim )-(lim)) )


print("convert to numeral rads",((out/(2**16-1) * 2*lim )-(lim)) )


print("1 raw is:",math.degrees((2/(2**16-1) * 2*lim )-(lim)) )
# 0.03295948729687289 

high=p1
low=p2
actual=(high)*16*16+low
print(actual)

print(hex(int(2**16/4 *3))   )



b'\x19\x00\x00\x00\x08\x00\x00\x00\x7f\xff\x7f\xf0\x1837\xff'
b'\x19\x00\x00\x00\x08\x00\x00\x00u\xcf\x7f\xf0\x1837\xff'
b'\x19\x00\x00\x00\x08\x00\x00\x00\x7f\xff\x7f\xf0\x1837\xff'

b'\x7f\xff\x7f\xf0\x1837\xff'
b'u\xcf\x7f\xf0\x1837\xff'
b'\x7f\xff\x7f\xf0\x1837\xff'


'0111010111001111011111111111000000011000001100110011011111111111'
b'u\xcf\x7f\xf0\x1837\xff'

import keyboard
print("Press 'q' to stop the thread.")
keyboard.wait('q')  # Wait until 'q' is pressed
print("Press 'q' to stop the thread.")
