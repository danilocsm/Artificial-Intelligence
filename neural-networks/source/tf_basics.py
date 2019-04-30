import tensorflow as tf 
import numpy as np
# from read_data import get_minibatch()

x = tf.placeholder(tf.float32,name='x',shape=[None,784])
W = tf.Variable(tf.random_uniform([784,10],-1,1),name='W')
b = tf.Variable(tf.zeros([10]),name='biases')

output = tf.matmul(x,W) + b
# initialize all Variables in the graph
init_op = tf.global_variables_initializer()

with tf.Session() as sess:
    # run the session to initialize the Variables
    sess.run(init_op) 
    # this will feed the placeholder
    rand_array = np.random.rand(10,784)
    feed_dict={x:rand_array}

    print(sess.run(output,feed_dict=feed_dict))