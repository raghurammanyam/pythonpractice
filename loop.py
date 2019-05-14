abc='helloworld'
str=[x for x in abc]
for i in (str):
    for x in range(len(str)//2):
        print(str[:1])
        if (len(str)-1)>(x+1):
            print(str[:x]+' '+str[:x+1])
    #print('\n')
