import numpy as np

B = np.matrix([[1,1,1,1,1,1,1,1,1,1,1,0],
               [1,1,1,1,1,1,1,1,1,0,1,1],
               [1,1,1,1,1,1,1,1,1,1,0,1],
               [1,1,1,1,1,1,0,1,1,1,1,1],
               [1,1,1,1,1,1,1,0,1,1,1,1],
               [1,1,1,1,1,1,1,1,0,1,1,1],
               [1,1,1,0,1,1,1,1,1,1,1,1],
               [1,1,1,1,0,1,1,1,1,1,1,1],
               [1,1,1,1,1,0,1,1,1,1,1,1],
               [1,0,1,1,1,1,1,1,1,1,1,1],
               [1,1,0,1,1,1,1,1,1,1,1,1],
               [0,1,1,1,1,1,1,1,1,1,1,1]])
v = np.matrix([[-15],[21],[-83],[4],[-33],[20],[31],[-44],[7],[16],[24],[58]])

one_domi = 1/10*v
two_domi = 1/100*(10*v+np.dot(B,v))
print(one_domi)
print(two_domi)