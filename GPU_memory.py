import random 
import matplotlib.pyplot as plt



#initialization
oh=2
ow=2
th=2
tw=2
sh=2
sw=2
bw=2
bh=2



def TexCrtoLg8(p,bw,bh,sw,sh,tw,th,ow,oh):
        i = p[0]
        j = p[1]
        
        oi=i//(tw*sw*bw)
        oj=j//(th*sh*bh)
        
        i=i%(tw*sw*bw)
        j=j%(th*sh*bh)
             
        
        val=oi*tw*th*bw*bh*sw*sh+oj*tw*th*bw*bh*sw*sh*ow        
        val+=(i//(sw*bw))*bw*bh*sw*sh+(j//(sh*bh))*bw*bh*sw*sh*tw+((i%(bw*sw))//bw)*bw*bh+((j%(bh*sh))//bh)*bw*bh*sw+(i%bw)+(j%bh)*bw
        return val

def MAP(p,m):
    i = p[0]
    j=  p[1]
   
    return i*m+j
Buff_init=[]

def Init(n,m, Buff_init):
    for i in range (n): 
        for j in range (m): 
            Buff_init.append((i,j))
    random.shuffle(Buff_init)
    counter=0
##2D Tex
    TexBuff= [ []  for x in range(n)]
    for i in range(n):
        for j in range(m):
            (TexBuff[i]).append(Buff_init[counter])
            counter+=1
    P=0
    for i in range (n):
        for j in range (m):
                if TexBuff[i][j]==((i,j)):
                    P+=1
                    x=random.randint(0,n-1)
                    y=random.randint(0,m-1) #avoid another loop
                    while(TexBuff[i][j]==((x,y))):
                        x=random.randint(0,n-1)
                        y=random.randint(0,m-1)
                    TexBuff[i][j],TexBuff[x][y]=TexBuff[x][y],TexBuff[i][j]
                    

    RAM = [ 0  for x in range(n*m)]
    i=0
    j=0
    for i in range(n):
        for j in range(m):
            p = TexCrtoLg8((i,j),bw,bh,sw,sh,tw,th,ow,oh)        
            RAM[p]=TexBuff[i][j]
            
    addresses=[]
    for g in RAM:
        addresses.append(TexCrtoLg8((i,j),bw,bh,sw,sh,tw,th,ow,oh))
        
    return addresses



    

##########Cache class##############
class Tag(object):
    def __init__(self,cycle,hits,misses,tag):
        self.tag = tag
        self.cycle = cycle
        self.misses = misses
        self.hits = hits

class Cache(object):
    def __init__(self,size,ways,sets,blocksize,misses,hits,cycles):
        self.size = size
        self.ways = ways
        self.sets = sets
        self.blocksize = blocksize
        self.tags = [ Tag(0,0,0,-1)  for x in range(self.sets*self.ways)]
        self.hits = 0
        self.misses = 0
        self.cycles = 0
            
    def read(self,address):
        cr_set = (address//self.blocksize)%(self.sets)
        tag = address//self.blocksize
        ret = 0
        self.cycles +=1
        found = 0
        for i in range(self.ways):
            if self.tags[i*self.sets+cr_set].tag == tag:
                self.hits +=1
                ret = 1
                self.tags[i*self.sets+cr_set].cycle = self.cycles
                self.tags[i*self.sets+cr_set].hits += 1
                found = 1
                break
            
        if found == 0:
            minway = 0
            mincycle = self.tags[cr_set].cycle
            for i in range(self.ways):
                if mincycle > self.tags[i*self.sets+cr_set].cycle:
                    mincycle = self.tags[i*self.sets+cr_set].cycle
                    minway = i
            
            self.misses +=1
            ret = 0
            self.tags[minway*self.sets+cr_set].cycle = self.cycles
            self.tags[minway*self.sets+cr_set].tag = tag
            self.tags[minway*self.sets+cr_set].misses += 1
            
        return ret
    
    def printSetStats(self):
        for s in range(self.size//self.blocksize//self.ways):
            self.misses = 0
            self.hits = 0
            for w in range(self.ways):
                self.misses += self.tags[w*self.sets+s].misses
                self.hits += self.tags[w*self.sets+s].hits
                if self.misses + self.hits != 0:
                    print("hit ratio for set "+str(s)+" = "+str(float(self.hits/(self.hits+self.misses)))+ ", reads = "+str(self.hits+self.misses))
        return
                    
def main():  
    misses = []  
    size = []              
    iterations = 50
    n=1
    m=1000
    for k in range(iterations):
        m +=1500 
        X = Cache(2**16,4,512,32,0,0,0)
        Addrs = Init(n,m,Buff_init)
        for u in range(100):
            for l in range(2**12):
                p = Addrs[l%(len(Addrs))]
                X.read(p)
        misses.append(X.misses/(X.misses+X.hits))
        size.append(n*m)
        print(misses, size)
        
    fig= plt.figure(figsize=(12,8))    
    plt.plot(size, misses)
    plt.xlabel('size in bytes',fontsize = 14)
    plt.ylabel('miss rate',fontsize = 14)
    plt.show()
    
main()
        

    

