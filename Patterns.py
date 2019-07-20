import re
def slice(line):
	if not line.count(' ') or not line.strip():
		return []
	
	spaces = re.split(r'[^ ]+',line)
	letters = line.split()
	patterns = []
	leng = len(letters)
	for i in range(1,leng + 1):
		for c in range(leng - i + 1):
			np = bridgelist(letters[c:c+i],spaces[c:c+i+1])
			if c > 0:
				np = cutfspace(np)
			if c+i < leng:
				np = cutlspace(np)
			x = sumlen(spaces[:c+1])
			x += sumlen(letters[:c])
			x -= np.find(np.strip())
			patterns.append((np,x))
        return patterns
def cutfspace(x):
    return x[int(x[0] == ' '):]
def cutlspace(x):
    return x[:x[-1] == ' ' and -1 or len(x)]
def sumlen(a):
    return sum([len(b) for b in a])
def bridgelist(list,bridges):
	holder = [bridges[0]]
	for l, b in zip(list,bridges[1:]):
		holder.append(l + b)
	return "".join(holder)


