import random
x=0
inputFile=open("InputFile.txt","w+")
i=1
while x<200:
     seatsReserved=random.randint(1,20)
     x+=seatsReserved
     inputFile.write('{} {}{}'.format("R"+'{:04d}'.format(i),seatsReserved,'\n'))
     i=i+1

inputFile.close()