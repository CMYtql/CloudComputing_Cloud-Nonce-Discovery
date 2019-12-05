# -*- coding: utf-8 -*-
import hashlib
import time
import sys

def goldennonce(D,N,T,index):
    # d means how many leading 0
    d = '0'*int(D)
    block_data = 'COMSM0010cloud'
    # start timing before the loop for golden nonce discovery
    start = time.perf_counter()

    # lower_bound=int(index) , upper_bound= 2**32, step=int(N)
    for num in range(int(index),2**32,int(N)):
        #append the number to the block data
        value = str(num) + block_data
        # the first hash handling
        hash1= hashlib.sha256(value.encode('utf-8')).hexdigest()
        #twice hash
        hash2= hashlib.sha256(hash1.encode('utf-8')).hexdigest()
        # finish timing after twice hash handling
        runtime = (time.perf_counter() - start)
        
        # compare the real runtime with the desired runtime input by user
        # if larger, it means timeout and stop searching for golden nonce.
        if int(runtime)>int(T):
            print('Oops. Timeout!')
            break
        # if within time T specified by user
        # match the leading bits of hashing result with difficulty-level specified by user
        # if true, the golden nonce is found, break the loop.
        if hash2.startswith(d):
            print('Golden nonce is '+ str(num) + ', its hash is '+ hash2)
            print('Well done with time used(s): '+str(runtime)) 
            break       
   
if __name__ == "__main__":
    try:
        # four parameters transferred to the function goldennonce()
        # use argv to get the values
        D,N,T,index=sys.argv[1:5]
        goldennonce(D,N,T,index)
    except Exception as e:
        print(e)