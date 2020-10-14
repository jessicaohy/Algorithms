# Jessica Oh Hui Yu
# 29886465
# FIT3155 Advanced algorithms and data structures
# Assignment 3
# Task 1

import sys
import random

def dec2binbits(dec):
    """
    This function converts an integer with base 10 (dec) to binary.
    :param dec:
    :return: binaryList
    :complexity worse case = O(log(N))
    where N is the number of digits
    """
    binaryList=[]                                   # contains binary

    while dec>0:
        binaryList.append(dec%2)                    # remainder either 0 or 1
        dec=dec//2                                  # integer division

    binaryList.reverse()                            # reverse to get binary list
    # print(l)
    return binaryList

def repeatedSquaring(a, b, n):
    """
    THis function computes repeated squaring, replacing the pow() function.
    :param a:
    :param b:
    :param n:
    :return: result
    :complexity worse case = O(log(N))
    where N is the number of bits
    """
    binaryList = dec2binbits(b)                     # convert into a list of binary
    binaryList.reverse()                            # least significant to most significant

    # list for doing repeated squaring
    repeatedSquaringList = []
    for i in range(len(binaryList)):
        repeatedSquaringList.append(-1)
    repeatedSquaringList[0] = a                     # first position is a

    result = 1
    for i in range(1, len(repeatedSquaringList)):
        repeatedSquaringList[i] = (repeatedSquaringList[i-1] * repeatedSquaringList[i-1]) % n   # multiply prev no. tgt
        if binaryList[i] != 0:
            result = (result * repeatedSquaringList[i]) % n
    # print("result = ", result)
    return result



def millerRabin(n, nBits):
    """
    This function test if a number is a prime number using the Miller-Rabin's randomized algorithm.
    :param n:
    :param nBits:
    :return: True or False
    :complexity O(log(N))
    where N is the number of bits
    """

    # number of iterations
    # some constants time k bits
    # every k times will get 1 prime no.
    nIterations = 3 * nBits

    # % = remainder, // = integer division
    if n % 2 == 0:
        return False                                # composite

    s = 0
    t = n - 1

    while t % 2 == 0:                               # while it is even number
        s = s + 1
        t = t/2

    # at this stage, n-1 = 2^s.t, where t is odd

    # using repeated squaring instead of pow() as pow() is very expensive to implement here
    # loop repeated squaring, testing if it is prime
    for i in range(nIterations):

        # choose a random number from 2 to n-1
        a = random.randint(2, n-1)

        if repeatedSquaring(a, n-1, n) != 1:
            # print("outside")
            return False                            # composite

        for j in range(1,s):

            if repeatedSquaring(a, (1 << j)*t, n) == 1 and repeatedSquaring(a, (1 << (j-1))*t, n) != 1 and repeatedSquaring(a, (1 << (j-1))*t, n) !=-1:
                # to make sure prime numbers are not treated as composite
                if repeatedSquaring(a, (1 << j)*t, n) % n == 1 % n or repeatedSquaring(a, (1 << j)*t, n) % n == -1 % n:
                    continue
                else:
                    # print("inside")
                    return False                    # composite

    return True                                     # PROBABLY PRIME. accuracy depends on number of iterations


def genPrime(k):                                            # k = k bits long
    """
    This function generates a prime number from a range of number, and prints it.
    :param k:
    :return:
    :complexity worse case = O(Mlog(N))
    where M is the number of numbers in the range
    where N is the number of bits in a number
    """
    foundPrime = False

    while foundPrime == False:                              # keep finding until found prime number
        # print("\n")

        # 1. uniformly picking any random number
        # print(random.randint(0,1))
        # shift left bit. base 2 on left , power on the right
        fromRange = 1 << (k-1)                              # 2 ^ (k-1)
        toRange =  (1 << k) - 1                             # (2 ^ k) - 1
        randomNo = random.randint(fromRange, toRange)

        # if found prime number
        if millerRabin(randomNo, k) == True:
            print(randomNo)                                 # PRINT
            foundPrime = True                               # stop finding


################# M A I N #####################
if __name__== "__main__":
    k = sys.argv[1]     # 2nd argument in terminal

    k = int(k)          # convert to integer
    genPrime(k)         # call function




