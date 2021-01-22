# -*- coding: utf-8 -*-
"""Cross Entropy 2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yNZHdofssfch5w-WVRMGQnCeNwA7u6by
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

def sigmoid2(x0, x1, w):
  y = w[0]*x0 + w[1]*x1+w[2]
  y = 1 / (1+np.exp(-y))
  return y

from mpl_toolkits.mplot3d import axes3d

def show3d_sigmoid2(ax, w):
  xn = 50
  x0 = np.linspace(X_range0[0], X_range0[1], xn)
  x1 = np.linspace(X_range1[0], X_range1[1], xn)
  xx0, xx1 = np.meshgrid(x0,x1)
  y = sigmoid2(xx0,xx1,w)
  ax.plot_surface(xx0,xx1,y,color='blue', edgecolor='gray', rstride=5, cstride=5, alpha=0.3)

def show_data2_3d(ax,x,t):
  c = [[.5, .5, .5], [1, 1, 1]]
  for i in range(2):
    ax.plot(x[t[:, i]==1, 0], x[t[:,i]==1,1], 1-i,marker='o', color=c[i], markeredgecolor='black', linestyle='none', markersize=5, alpha=0.8)
  Ax.view_init(elev=25, azim=-30)

Ax = plt.subplot(1,1,1, projection='3d')
W = [-1, -1, -1]
show3d_sigmoid2(Ax, W)
show_data2_3d(Ax, X, T2)

def show_contour_sigmoid2(w):
  xn = 30
  x0 = np.linspace(X_range0[0], X_range0[1], xn)
  x1 = np.linspace(X_range1[0], X_range1[1], xn)
  xx0, xx1 = np.meshgrid(x0, x1)
  y = sigmoid2(xx0, xx1, w)
  cont = plt.contour(xx0, xx1, y, levels=(0.2, 0.5, 0.8), colors = ['k', 'cornflowerblue', 'k'])
  cont.clabel(fmt='%1.1f', fontsize = 10)
  plt.grid(True)

plt.figure(figsize=(3,3))
W = [-1, -1, -1]
show_contour_sigmoid2(W)

def cce_cost2(w, x, t):
  X_n = x.shape[0]
  y = sigmoid2(x[:, 0], x[:, 1], w)
  cost = 0
  for n in range(len(y)):
    cost = cost - (t[n, 0]*np.log(y[n])+(1-t[n,0])*np.log(1-y[n]))
  cost = cost / X_n
  return cost

def cce_slope2(w, x, t):
  X_n = x.shape [0]
  y = sigmoid2(x[:,0], x[:, 1], w)
  slope = np.zeros(3)
  for n in range(len(y)):
    slope[0] = slope[0]+(y[n]-t[n, 0]*x[n,0])
    slope[1] = slope[1]+(y[n]-t[n, 0]*x[n,1])
    slope[2] = slope[2]+(y[n]-t[n, 0])
    slope = slope / X_n

    return slope

from scipy.optimize import minimize

def fit_sigmoid2(w_init, x, t):
  res = minimize(cce_cost2, w_init, args=(x,t), jac=cce_slope2, method="CG")
  return res.x

plt.figure(1, figsize=(7,3))
plt.subplots_adjust(wspace=0.5)

Ax = plt.subplot(1,2,1, projection='3d')
W_init = [-1, 0, 0]
W = fit_sigmoid2(W_init, X, T2)
print("w0 = {0:.2f}, w1 = {1:.2f}, w2 = {2:.2f}".format(W[0],W[1],W[2]))
show3d_sigmoid2(Ax, W)

show_data2_3d(Ax, X, T2)
cost = cce_cost2(W, X, T2)
print("cost = {0:.2f}" .format(cost))

Ax = plt.subplot(1, 2, 2)
show_data2(X, T2)
show_contour_sigmoid2(W)
plt.show()

def cce_optimum_weight_finder2(x, t):
  w_init = [-1, 0, 0]
  alpha = 0.1
  n_max = 1000
  eps = 0.001
  w_n = np.zeros([n_max, 3])
  w_n[0,:] = w_init
  for n in range(n_max):
    slope = cce_slope2(w_n[n-1], x, t)
    w_n[n, 0] = w_n[n-1, 0] - alpha * slope[0]
    w_n[n, 1] = w_n[n-1, 1] - alpha * slope[1]
    w_n[n, 2] = w_n[n-1, 2] - alpha * slope[2]
    loss = cce_cost2(w_n[n-1], x, t)
    if max(np.absolute(slope)) < eps:
      break
  w0 = w_n[n, 0]
  w1 = w_n[n, 1]
  w2 = w_n[n, 2]
  return w0, w1, w2

k = cce_optimum_weight_finder2(X, T2)
print(k)


plt.figure(1, figsize=(7,3))
plt.subplots_adjust(wspace=0.5)

Ax = plt.subplot(1,2,1, projection='3d')
W_init = [-1, 0, 0]
W = cce_optimum_weight_finder2(X, T2)
print("w0 = {0:.2f}, w1 = {1:.2f}, w2 = {2:.2f}".format(W[0],W[1],W[2]))
show3d_sigmoid2(Ax, W)

show_data2_3d(Ax, X, T2)
cost = cce_cost2(W, X, T2)
print("cost = {0:.2f}" .format(cost))

plt.show()