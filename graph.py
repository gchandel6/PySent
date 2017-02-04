import matplotlib.pyplot as plt
import matplotlib.animation as anm 
import time
# from matplotlib import style

# style.use("ggplot")

pic = plt.figure()
ax1 = pic.add_subplot(1,1,1)

def animate(i):

	pullData = open("twitter-out.txt","r").read()
	array = pullData.split('\n')

	xarr=[]
	yarr=[]

	x=0
	y=0

	for line in array:

		x+=1
		if "pos" in line:
			y+=1
		elif "neg" in line:
			y-=1
		
		xarr.append(x)
		yarr.append(y)

	ax1.clear()
	ax1.plot(xarr,yarr)


ani = anm.FuncAnimation(pic,animate,interval=1000)
plt.show()