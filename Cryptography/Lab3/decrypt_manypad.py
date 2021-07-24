with open('cipher.txt', 'r') as f:
    c_texts = f.read().split('\n')

for i in range(len(c_texts)):
    c_texts[i] = [c_texts[i][j]+c_texts[i][j+1] for j in range(0, len(c_texts[i]), 2)]
    c_texts[i] = [(int('0x'+hexx, 16)) for hexx in c_texts[i]]
    print(c_texts[i])
        
