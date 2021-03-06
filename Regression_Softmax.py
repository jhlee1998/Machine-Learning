# -*- coding: utf-8 -*-
"""Soft Max

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JzPlFKgxiqX39K7m5X3mIT2X2q3cVQRJ
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

np.random.seed(seed=1)
N = 100
K = 3
T3 = np.zeros((N,3), dtype=np.uint8)
T2 = np.zeros((N,2), dtype=np.uint8)
X = np.zeros((N,2))
X_range0 = [-3, 3]
X_range1 = [-3, 3]
Mu = np.array([[-.5, -.5],[-.5, 1.0],[1,-.5]])
Sig = np.array([[.7, .7],[.8,.3],[.3,.8]])
Pi = np.array([0.4, 0.8, 1])
for n in range (N):
  wk = np.random.rand()
  for k in range(K):
    if wk < Pi[k]:
      T3[n,k] = 1
      break
      
  for k in range(2):
    X[n, k] = (np.random.randn()*Sig[T3[n, :]==1, k]+Mu[T3[n, :]==1,k])
T2[:, 0] = T3[:, 0]
T2[:, 1] = T3[:, 1] | T3[:, 2]

def show_data2(x, t):
  wk, K = t.shape
  c = [[.5, .5, .5], [1,1,1],[0,0,0]]
  for k in range(K):
    plt.plot(x[t[:,k]==1,0],x[t[:,k]==1,1], linestyle='none', markeredgecolor='black', marker = 'o', color = c[k], alpha = 0.8)
    plt.grid (True)

plt.figure(figsize = (7.5, 3))
plt.subplots_adjust(wspace=0.5)
plt.subplot(1, 2, 1)
show_data2(X, T2)
plt.xlim(X_range0)
plt.ylim(X_range1)

plt.subplot(1, 2, 2)
show_data2(X, T3)
plt.xlim(X_range0)
plt.ylim(X_range1)
plt.show()

def softmax3(x0, x1, w):
  K = 3
  w = w.reshape((3, 3))
  n = len(x1)
  y = np.zeros((n, K))
  for k in range(K):
    y[:, k] = np.exp(w[k,0]*x0+w[k,1]*x1+w[k,2])
  wk = np.sum(y, axis = 1)
  wk = y.T / wk
  y = wk.T
  return y

W = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
y = softmax3(X[:3, 0], X[:3, 1], W)
print(np.round(y, 3))

def cce_softmax3_cost(w, x, t):
  X_n = x.shape[0]
  y = softmax3(x[:,0], x[:,1], w)
  cost = 0
  N, K = y.shape
  for n in range(N):
    for k in range(K):
      cost = cost - (t[n, k]*np.log(y[n, k]))
  cost = cost / X_n
  return cost

W = np.array([1, 2, 3, 6, 5, 5, 7, 8, 9])
cce_softmax3_cost(W,X, T3)

def cce_softmax3_slope(w, x, t):
  X_n = x.shape[0]
  y = softmax3(x[:, 0], x[:, 1], w)
  slope = np.zeros((3, 3))
  N, K = y.shape
  for n in range(N):
    for k in range(K):
      slope[k, :] = slope[k, :] - (t[n, k] - y[n, k])*np.r_[x[n, :], 1]
  slope = slope / X_n
  return slope.reshape(-1)

W = np.array([1, 2, 3, 6, 5, 5, 7, 8, 9])
cce_softmax3_slope(W, X, T3)

from scipy.optimize import minimize

def cce_softmax3_optimum_weight_finder(w_init, x, t):
  res = minimize(cce_softmax3_cost, w_init, args = (x,t), jac = cce_softmax3_slope, method="CG")
  return res.x

def show_softmax3_countour(w):
  xn = 30
  x0 = np.linspace(X_range0[0], X_range0[1],xn)
  x1 = np.linspace(X_range1[0], X_range1[1],xn)

  xx0, xx1 = np.meshgrid(x0, x1)
  y = np.zeros((xn, xn, 3))
  for i in range (xn):
    wk = softmax3(xx0[:, i], xx1[:, i], w)
    for j in range (3):
      y[:, i, j] = wk[:, j]
  for j in range (3):
    cont = plt. contour(xx0, xx1, y[:, :, j], levels=(0.5, 0.9), colors=['blue', 'k'])
    cont.clabel(fmt='%1.1f', fontsize = 9)
  plt. grid (True)

W_init = np.zeros((3,3))
W = cce_softmax3_optimum_weight_finder(W_init, X, T3)

cost = cce_softmax3_cost(W, X, T3)
print = ("cost = {0:.2f}", format(cost))

plt.figure(figsize=(3,3))
show_data2(X, T3)
show_softmax3_countour(W)

plt.show()