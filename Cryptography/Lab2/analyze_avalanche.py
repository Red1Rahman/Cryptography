input1=open("cipher1.txt", "r")
input2=open("CipherWithChangedKey.txt", "r")
output=open("outKeyAvalanche", "w")
def parity(num):
	if(num==0):
		return 0
	return (num%2)+parity(num>>1)

found=0
while found!=12:
	message1=input1.readline()
	message2=input2.readline()
	if(len(message1)<=1):
		continue
	sum=0
	for i in range(len(message1)-1):
		ch1=int(message1[i], 16)
		ch2=int(message2[i], 16)		
		sum+=parity(ch1^ch2)
	found+=1
	output.write(str(sum)+'\n')
