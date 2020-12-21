import tensorflow._api.v2.compat.v1 as tf
tf.enable_eager_execution()
import numpy as np
import matplotlib.pyplot as plt
import csv


def readData():
    lix = list()
    f = open('test.csv', 'rt').readlines()
    d = csv.reader(f)
    for line in d:
        linflo = list()
        for ite in line:
            linflo.append(float(ite))
        lix.append(linflo)
        pass
    x = np.mat(lix)
    return x
data = readData()
print(data.shape)
#PCA
def pca(x,dim = 2):
    '''
        x:输入矩阵
        dim:降维之后的维度数
    '''
    with tf.name_scope("PCA"):

        m,n= tf.to_float(x.get_shape()[0]),tf.to_int32(x.get_shape()[1])
        assert not tf.assert_less(dim,n)
        mean = tf.reduce_mean(x,axis=1)
        x_new = x - tf.reshape(mean,(-1,1))
        cov = tf.matmul(x_new,x_new,transpose_a=True)/(m - 1)
        e,v = tf.linalg.eigh(cov,name="eigh")
        e_index_sort = tf.math.top_k(e,sorted=True,k=dim)[1]
        v_new = tf.gather(v,indices=e_index_sort)
        pca = tf.matmul(x_new,v_new,transpose_b=True)
    return pca
pca_data = tf.constant(np.reshape(data,(data.shape[0],-1)),dtype=tf.float32)
pca_data = pca(pca_data,dim=2)
plt.scatter(pca_data[:, 0], pca_data[:, 1], c='black')
plt.show()