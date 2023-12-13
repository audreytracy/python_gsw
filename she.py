import numpy as np
import math
import random
from scipy.linalg import block_diag

# PARAMETERS
q = 27581 # modulus
l = math.ceil(math.log2(q)) # length of binary values
n = 5 # lattice dimension
m = n*l
t = [random.randint(0,q-1) for i in range(n-1)]
s = t.copy()
s.append(1)
t = np.array([t])
s = np.array(s) # PRIVATE KEY
B = np.random.randint(q, size=(n-1, m), dtype=np.int64).astype(np.int64)
e=[random.randint(0,2) for i in range(m)] # just set error to small value at first
b = np.add(np.dot(t,B), e) % q
A = np.row_stack((-1*B, b))%q # PUBLIC KEY
g = 2**np.arange(l)
G = block_diag(*[g for null in range(n)]) # gadget matrix
R = np.array([[random.randint(0,1) for i in range(m)] for i in range(m)]) # random 0/1 matrix


def encrypt(message):
    return (np.dot(A, R) + message*G) % q

def decrypt(ciphertext):
    div = np.rint(np.divide(np.dot(s, ciphertext) % q, np.dot(s, G) % q))
    possible_messages = np.unique(div)
    message = 0
    shortest_dist = float('inf')
    for mu in possible_messages:
        dist = (np.dot(s, ciphertext) - mu*np.dot(s, G)) % q
        dist = np.dot(dist, dist)
        if dist < shortest_dist:
            message = mu
            shortest_dist = dist
    return int(message)

print(decrypt(encrypt(55))) # change value
print(decrypt(encrypt(11)+encrypt(44))) # change number of additions