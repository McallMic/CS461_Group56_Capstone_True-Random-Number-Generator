import matplotlib.pyplot as plt
import numpy as np

file = open("RANDOM_OUTPUT.txt","r")
x = []
y = []
for i in file:
    x.append(int(i))

s=len(x) #maintain the length of the original list
file.close() #close the file after reading

#break the list into two halves and store the second half in y
for i in range((len(x)//2)):
    y.append(x[(i+len(x)//2)])
for i in range((len(x)//2)):
    x.pop()

plt.xlim([0, 500])
plt.ylim([0, 500])
plt.scatter(x,y)
plt.show()

#This is currently assuming the list of generated numbers is even, and the range of the generated numbers is between 0 and 500.

