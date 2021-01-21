import matplotlib.pyplot as plt
import numpy as np

x = "Behavioral"
y = "Networkability"
z = "Cost"
q = "DeviceIdentification"


print(len(x))
print(len(y))
print(len(z))
print(len(q))

def func(m,x,b):
    
    print(m*x + b)
    
print()
m = 3.97
b = 8.6
func(m,len(x),b)
func(m,len(y),b)
func(m,len(z),b)
func(m,len(q),b)

xx = [len(x),len(y),len(z),len(q)]
yy = [50,60,25,90] 



m, b = np.polyfit(xx, yy, 1)

print(m)
print(b)

plt.scatter(xx,yy)
