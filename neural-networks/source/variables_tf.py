import tensorflow as tf 

def layer(data, weight_shape, bias_shape):

    weight_init = tf.random_uniform_initializer(minval=-1,maxval=1)
    bias_init = tf.constant_initializer(value=0)
    # prevents the reuse of a variable
    W = tf.get_variable("W",weight_shape,initializer=weight_init)

    b = tf.get_variable("b",bias_shape,initializer=bias_init)

    return tf.matmul(data,W) + b

def my_network(data):

    with tf.variable_scope("layer_1"):
        output_1 = layer(data,[100,784],[100])
    
    with tf.variable_scope("layer_2"):
        output_2 = layer(output_1, [100,50],[50])
    
    with tf.variable_scope("layer_3"):
        output_3 = layer(output_2, [50,10],[10])
    
    return output_3


i_1 = tf.placeholder(tf.float32,[100,784],name="i_1")

my_network(i_1)

i_2 = tf.placeholder(tf.float32,[100,784],name="i_2")

my_network(i_2)