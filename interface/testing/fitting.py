from pylab import *

x = np.array((36,43,31))
y = np.array((268,316,202))

m,b = polyfit(x,y,1)

print(m)
print(b)

print(m*31 + b)