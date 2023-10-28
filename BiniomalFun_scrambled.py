import math
import matplotlib.pyplot as plt
import random
import numpy as np

def pdf(n,p,k):
    return math.comb(n,k)* p**k * (1-p)**(n-k)
    
def cdf(n,p,k):
    sum = 0
    for i in range(k+1):
        sum += pdf(n,p,i)
    return sum
    
n=25
p=0.3
k=10
proba = 1-cdf(n,p,k) + pdf(n,p,k)
print("Let X ~ Bin({},{}). Then, Pr(X >={})={}".format(n, p, k,proba))








