import sys
global MOD
MOD = (1<<8) + (1<<4) + (1<<3) + (1<<1) + 1

def add(a, b):
	return a^b

def sub(a, b):
	return a^b

def mul(a, b):
	res=0
	amul=a
	while(b!=0):
		if((b&1)!=0):
			res=add(res, amul)
			#print("Adding "+str(amul))
			#print("Res " + str(res))
		amul=amul<<1
		b=b>>1	
	return res


def mod(a, b):
	rem=a
	bitCntA=0
	acopy=a
	while(acopy!=0):
		acopy=acopy>>1
		bitCntA=bitCntA+1
	bitCntB=0
	bcopy=b
	while(bcopy!=0):
		bcopy=bcopy>>1
		bitCntB=bitCntB+1
	bcopy=b
	while(bitCntB<bitCntA):
		bitCntB=bitCntB+1
		b=b<<1
	rem=a
	while(b>=bcopy):
		if((rem & (1<<(bitCntB-1)))!=0):
			rem=rem^b
		b=b>>1
		bitCntB=bitCntB-1
	return rem


def modularInv(x):
	for i in range(1<<8):
		if(mod(mul(x, i), MOD)==1):
			return i
	return 0

global sbox
sbox=[[0]*16 for x in xrange(16)]
global isbox
isbox=[[0]*16 for x in xrange(16)]

def putSubByte(val):
	modInv=modularInv(val)
	b=[]
	c=[]
	bprime=[]
	for i in range(8):
		if((modInv&(1<<i))!=0):
			b.append(1)
		else:
			b.append(0)
	c.append(1)
	c.append(1)
	c.append(0)
	c.append(0)
	c.append(0)
	c.append(1)
	c.append(1)
	c.append(0)	
	for i in range(8):
		#print(str(i)+ " "+str((i+4)%8) + " "+ str((i+5)%8) + " "+ str((i+6)%8) + " " + str((i+7)%8))
		bprime.append(b[i] ^ b[(i+4)%8] ^ b[(i+5)%8] ^ b[(i+6)%8] ^ b[(i+7)%8] ^ c[i])
	ret=0
	for i in range(8):
		ret=ret*2
		ret=ret+bprime[7-i]
	#print(str(val>>4) + " " + str(val%(1<<4)))
	sbox[val>>4][val%(1<<4)]=ret

def putiSubByte(val):
	b=[]
	c=[]
	bprime=[]
	for i in range(8):
		if((val&(1<<i))!=0):
			b.append(1)
		else:
			b.append(0)
	c.append(1)
	c.append(0)
	c.append(1)
	c.append(0)
	c.append(0)
	c.append(0)
	c.append(0)
	c.append(0)	
	for i in range(8):
		#print(str(i)+ " "+str((i+4)%8) + " "+ str((i+5)%8) + " "+ str((i+6)%8) + " " + str((i+7)%8))
		bprime.append(b[(i+2)%8] ^ b[(i+5)%8] ^ b[(i+7)%8] ^ c[i])
	ret=0
	for i in range(8):
		ret=ret*2
		ret=ret+bprime[7-i]
	#print(str(val>>4) + " " + str(val%(1<<4)))
	isbox[val>>4][val%(1<<4)]=modularInv(ret)

for i in range((1<<8)):
	putSubByte(i)
	putiSubByte(i)

#for i in range(16):
#	for j in range(16):
#		sys.stdout.write(str(hex(sbox[i][j]))+" ")
#	print("")

for i in range(16):
	for j in range(16):
		sys.stdout.write(str(hex(isbox[i][j]))+" ")
	print("")


#print(mod(mul(4, 203), MOD))
#for i in range(1<<8):
#	print(str(i) + " "+ str(modularInv(i)))
global mat
mat=[[0]*4 for x in xrange(4)]

def buildMatrixFromInput():
	inputFile = open("input.txt", "r")
	message=inputFile.readline()
	row=0
	col=0
	i=0	
	while i<16:		
		mat[row][col]=ord(message[i])
		col=col+1
		if col==4:
			row=row+1
			col=0
		i=i+1

buildMatrixFromInput()



def shiftRows():
	sv=mat[1][0]
	for i in range(3):
		mat[1][i]=mat[1][i+1]
	mat[1][3]=sv
	for i in range(2):
		mat[2][i], mat[2][i+2] = mat[2][i+2], mat[2][i]
	sv=mat[3][3]
	i=2
	while i>=0:
		mat[3][i+1]=mat[3][i]
		i=i-1	
	mat[3][0]=sv

def printInputMatrix(mat):
	for i in range(4):
		for j in range(4):
			sys.stdout.write(str(hex(mat[i][j]))+" ")
		print("")


printInputMatrix(mat)
shiftRows()
print("")
printInputMatrix(mat)


global mixColumnMatrix
mixColumnMatrix=[[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
inverseMixColumnMatrix=[[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]

def mixColumnsMultiplication(a, b):
	if(b==1):
		return a
	if(b==2):
		a=(a<<1)
		if((a&(1<<8))!=0):
			a=(a%(1<<8))
			a=a^((1<<4) + (1<<3) + (1<<1) + (1<<0))
		return a
	if(b==3):
		return a^mixColumnsMultiplication(a, b-1)

def matrixMultiplication(a, b):
	res=[[0]*4 for x in xrange(4)]	
	for i in range(4):
		for j in range(4):
			res[i][j]=0
			for k in range(4):
				res[i][j]=res[i][j]^(mixColumnsMultiplication(b[k][j], a[i][k]))
	return res


def mixColumns():
	mat=matrixMultiplication(mixColumnMatrix, mat)	

print("")

printInputMatrix(mat)


global key
key=[[0]*4 for x in xrange(4)]

def buildKeyFromInput():
	keyFile = open("Key.txt", "r")
	message=keyFile.readline()
	row=0
	col=0
	i=0	
	while i<16:		
		key[row][col]=ord(message[i])
		col=col+1
		if col==4:
			row=row+1
			col=0
		i=i+1

buildKeyFromInput()

def addRoundKey():
	for i in range(4):
		for j in range(4):
			mat[i][j]=mat[i][j]^key[i][j]
addRoundKey()

global word, linearKey
word=[0]*44
linearKey=[0]*16
def buildLinearKey():
	sz=0
	for i in range(4):
		for j in range(4):
			linearKey[4*i+j]=key[i][j]

global RCon
RCon=[1, 2, 4, 8, 16, 2*16, 4*16, 8*16, 16+11, 3*16+6]

def KeyExpansion():
	buildLinearKey()	
	for i in range(4):
		word[i]=(linearKey[4*i]<<24)+ (linearKey[4*i+1]<<16) + (linearKey[4*i+2]<<8) + linearKey[4*i+3]
	for i in range(4, 44):
		temp=word[i-1]
		if((i%4)==0):
					

KeyExpansion()
