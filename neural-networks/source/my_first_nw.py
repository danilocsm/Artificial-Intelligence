import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# Parameters
learning_rate = 0.01
training_epochs = 30
batch_size = 100
display_step = 1
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

def layer(x, weight_shape, bias_shape):

    weight_stdev = (2.0/weight_shape[0])**0.5
    w_init = tf.random_normal_initializer(stddev=weight_stdev)
    bias_init = tf.constant_initializer(value=0)

    W = tf.get_variable("W",weight_shape,initializer=w_init)

    b = tf.get_variable("b",bias_shape,initializer=bias_init)

    return tf.nn.relu(tf.matmul(x,W)+b)

# produces a probability distribution over the output classes given a minibatch
def inference(x):

    with tf.variable_scope("hidden_1"):
        hidden_1 = layer(x,[784,256],[256])

    with tf.variable_scope("hidden_2"):
        hidden_2 = layer(hidden_1,[256,256],[256])

    with tf.variable_scope("hidden_3"):
        output = layer(hidden_2,[256,10],[10])

    return output
    # init = tf.constant_initializer(value=0)
    # with tf.variable_scope("layer"):
    #     W = tf.get_variable("W",[784,10],
    #                         initializer=init)
    #     b = tf.get_variable("b",[10],
    #                     initializer=init)

    #     output = tf.nn.softmax(tf.matmul(x, W) + b)
    # return output

# computes the value of the error function (in this case, the cross-entropy loss)
def loss(output, y):

    # dot_product = y * tf.log(output)

    # xentropy = -tf.reduce_sum(dot_product,reduction_indices=1)

    # loss = tf.reduce_mean(xentropy)
    xentropy = tf.nn.softmax_cross_entropy_with_logits(logits=output,labels=y)
    loss = tf.reduce_mean(xentropy)
    return loss

# responsible for computing the gradients of the model's parameters and updating the model
def training(cost, global_step):

    # tf.scalar_summary("cost",cost)
    global learning_rate
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train_op = optimizer.minimize(cost, global_step=global_step)

    return train_op

#will determine the effectiveness of a model
def evaluate(output, y):

    correct_prediction = tf.equal(tf.argmax(output,1),
                                    tf.argmax(y,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

    return accuracy

with tf.Graph().as_default():

    x = tf.placeholder("float",[None,784])

    y = tf.placeholder("float",[None,10])

    output = inference(x)

    cost = loss(output, y)

    global_step = tf.Variable(0,name='global_step',trainable=False)

    train_op = training(cost,global_step)

    eval_op = evaluate(output, y)

    saver = tf.train.Saver(max_to_keep=4)

    init_op = tf.global_variables_initializer()

    sess = tf.Session()

    # writer = tf.summary.FileWriter("logistic_logs",sess.graph)

    sess.run(init_op)

    # Training cycle
    for epoch in range(training_epochs):

        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)
        # Loop over all batches
        for i in range(total_batch):
            mbatch_x, mbatch_y = mnist.train.next_batch(batch_size)

            feed_dict = {x : mbatch_x, y : mbatch_y}
            sess.run(train_op,feed_dict=feed_dict)

            minibatch_cost = sess.run(cost,feed_dict=feed_dict)

            avg_cost += minibatch_cost/total_batch

        if epoch % display_step ==0:
            val_feed_dict = {
                x : mnist.validation.images,
                y : mnist.validation.labels
            }
            accuracy = sess.run(eval_op,feed_dict=val_feed_dict)
            print("Validation Error:{0}".format(1-accuracy))

            saver.save(sess,"models/my_test_model",global_step=global_step)

    print("Optimization Finished!")

    test_feed_dict = {
        x : mnist.test.images,
        y : mnist.test.labels
    }

    accuracy = sess.run(eval_op, feed_dict=test_feed_dict)
    print("Accuracy {0}".format(accuracy))
    # saver.save(sess,"/home/danilocrgm/Documents/miscellaneous/neural_networks/models/model.ckpt")
    # writer.close()
