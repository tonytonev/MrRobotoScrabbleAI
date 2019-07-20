def head(stringtree):
    p = stringtree.find('\001')
    if p == -1:
        return stringtree
    return stringtree[:p]

def split(stringtree):
    args = []
    e = 0
    s = 0
    if not stringtree.count('\001'):
        return []
    for i,c in enumerate(stringtree):
        if c == '\001':
                if s == e:
                        start = i+1
                s += 1
        elif c == '\002':
                e += 1
                if s == e:
                        args.append(stringtree[start:i])
    return args
    
def utils(st):
	start = st.find('\004') +1
	end = st.find('\004',start)
	return st[start:end]
    
def grow(head,list):
    st = head
    for a in list:
        st += '\001' + a + '\002'
    return st
