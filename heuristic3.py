from __future__ import print_function
import time
from itertools import chain
import sys
inpName=sys.argv[1]
outName=sys.argv[2]
finished=False
t1=time.time()
################################################################
def deepcopy(arr):
    return [row[:] for row in arr]
def copy1(done):
    return done[:]
def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
################################################################
def parse():
    fp=open(inpName,"r")
    line=""
    line=fp.readline()
    line=line.split(' ')
    num=eval(line[2])
    line=fp.readline()
    arr=[[]]
    count=0

    while len(line)>0:
        list1=line.split(' ')
        list1=list1[0:-1]
        for i in range(0,len(list1)):
            if isInt(list1[i]):
                arr[count].append(eval(list1[i]))
        arr.append([])
        line=fp.readline()
        count+=1
    del arr[count]
    return [arr,count,num]
#################################################################
def write_sat(done):
    f2=open(outName,'w')
    f2.write('%s\n'%('SAT'))
    for i in range(1,len(done)):
        if done[i]=='+':
            f2.write('%s '%(i))
        else:
            f2.write('-%d '%(i))
        # if done[i]=='+':
        #     f2.write('%s 0\n'%(i))
        # else:
        #     f2.write('-%d 0\n'%(i))
    f2.write('%d\n'%(0))

def assign_literal(arr,done,count):
    remove=[]
    pos=-1
    changed=0
    result=[0,[],[],0,0]
    #('**',arr)
    for l in arr:
        pos+=1
        if len(l)==1:
            var=abs(l[0])
            if done[var]==' ':
                done[var]='+' if l[0]>0 else '-'
                remove.append(pos)
                count-=1
                changed+=1
            else:
                sign='+' if l[0]>0 else '-'
                if sign!=done[var]:
                    result[0]=0
                    return result
    for k in range(len(remove)-1,-1,-1):
        del arr[remove[k]]
    result[0]=1
    result[1]=arr
    result[2]=done
    result[3]=count
    result[4]=changed
    return result        
def unitProp(arr,count,done):
    global finished 
    flag=0
    pos=-1
    remove=[]
    for l in arr:
        pos+=1
        remove_literal=[]
        for j in range(len(l)):
            if l[j]>0:
                sign='+'
                invert_sign='-'
            elif l[j]<0:
                invert_sign='+'
                sign='-' 
            val=abs(l[j])
            if done[val]==sign:
                remove.append(pos)
                count-=1
                break
            elif done[val]==invert_sign:
                remove_literal.append(j)
        for k in range(len(remove_literal)-1,-1,-1):
            del arr[pos][remove_literal[k]]
    for k in range(len(remove)-1,-1,-1):
        del arr[remove[k]]
    while True:
        ans=assign_literal(arr,done,count)
        arr=ans[1]
        done=ans[2]
        count=ans[3]
        changed=ans[4]
       
        if ans[0]==0:
            flag=1
            break
        elif changed>0:
       
            pos=-1
            remove=[]
            for l in arr:
                pos+=1
                remove_literal=[]
                for j in range(len(l)):
                    sign='+' if l[j]>0 else '-'
                    invert_sign='+' if l[j]<0 else '-' 
                    val=abs(l[j])
                    if done[val]==sign:
                        remove.append(pos)
                        count-=1
                        break
                    elif done[val]==invert_sign:
                        remove_literal.append(j)
                for k in range(len(remove_literal)-1,-1,-1):
                    del arr[pos][remove_literal[k]]
            for k in range(len(remove)-1,-1,-1):
                del arr[remove[k]]
            continue
        else:
            break
    if flag is 0:
        return [True,arr,count,done]
    if flag == 1:
        finished= False
        return [False,arr,count,done]

    
#################################################################
def write_unsat():
    f2=open(outName,'w')
    f2.write('%s\n'%('UNSAT'))
#################################################################

def find_sat(arr,done,counter,count):
   
    global finished
    if counter>=count:
        if finished==False:
            finished=True
            write_sat(done)       
    if finished is True:
        return
    if finished is False:
        clause=arr[counter]
        temp=copy1(done)
        flag=0
        for i in range(len(clause)):
           
            var=clause[i]
            if var>0:
                invert_sign='-'
            if var<0:
                invert_sign='+'    
            if done[abs(var)]==' ':
                if var<0:
                    done[abs(var)]='-'
                else:
                    done[abs(var)]='+'
                flag=1
            temp2=[]
            temp_arr=[[]*count]

            temp_arr[0:counter+1]=deepcopy(arr[0:counter+1])
            temp2[:]=deepcopy(arr[counter+1:])
            done=pureLiteralElimination(arr,count,done,num)
            res=unitProp(temp2,len(temp2),done)
            if res[0] == False:
                done=copy1(temp)
                done[abs(var)]= invert_sign
                continue
            else:
                temp_arr[counter+1:]=deepcopy(res[1])
                temp_arr=deepcopy(temp_arr[:counter+1+res[2]])
                done=copy1(res[3])
                find_sat(temp_arr,done,counter+1,counter+1+res[2])

            if finished is True:
                return    
            done=copy1(temp)
            done[abs(var)]= invert_sign
        if flag==0:
            return
################################################################
def pureLiteralElimination(arr,count,done,num):

    ale=0
    d=list(chain.from_iterable(arr))
    flag1=False
    flag2=False
    for i in range(1,num):
        if done[i]==' ':
            if i in d:
                flag1=True
            if -i in d:
                flag2=True
            if flag1==True and flag2==False:
                done[i]='+'
                ale+=1
                print(ale)
            elif flag1==False and flag2==True:
                done[i]='-'  
                ale+=1
                print(ale)
        flag1=False
        flag2=False 
    return done
################################################################
flg=0
res=parse()
arr=res[0]
count=res[1]
num=res[2]+1
done=[' ']*(res[2]+1)
done=pureLiteralElimination(arr,count,done,num)
res=unitProp(arr,count,done)
if res[0]==True:
    arr=res[1]
    count=res[2]
    done=res[3]  
    find_sat(arr,done,0,count)             
t2=time.time()
t_tot=t2-t1
print('Total time taken:',t_tot)
print('')