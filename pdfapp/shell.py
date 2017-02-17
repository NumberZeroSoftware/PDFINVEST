from subprocess import Popen

def call_main(string):
	var1 = " "
	var2 = " "
	boo = True
	for i in range(len(string)-1,-1,-1): 
		if(boo==True and string[i]!='/'):
			var1+=string[i]
		elif (boo==True and string[i]=='/'):
			var2+=string[i]
			boo = False
		elif (boo==False):
			var2+=string[i]
	var1 = var1[::-1]
	var2 = var2[::-1]
	Process=Popen('./myscript %s %s' % (str(var1),str(var2),), shell=True)

def main():
	call_main("/home/gdka/hola.pdf")

if __name__ == "__main__":
	main()