import sys
a = 0
k = 105263157894736840

def sum_k(k):
    new = int(str(k)[-1]+str(k)[:-1])
    return new

while a == 0:
    new = sum_k(k)
    if new == 2*k:
        print(k) 
        a=a+1
    elif k%10 == 0:
        k=k+1
    else:
        k=k+1
    if k%10000000 == 0:
        print(k)
# a = 0
# k = 1
# seek = 46656

# def proiz(k):
#     p = 1
#     for a in str(k):
#         p = p*int(a)
#     return(p)

# while a != 16:
#     new = proiz(k)
#     if new == seek:
#         print(k) 
#         a=a+1
#         k=k+1
#     elif k%10000000 == 0:
#         print(k)
#         k=k+1
#     else:
#         k=k+1
