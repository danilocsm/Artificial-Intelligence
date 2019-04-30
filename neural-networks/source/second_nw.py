import tensorflow as tf 

with tf.Session() as sess:
    # new_saver = tf.train.import_meta_graph('models/my_test_model-9350.meta')
    new_saver = tf.train.Saver()
    new_saver.restore(sess,'./my_test_model-11000')
    print(sess.run('eval_op'))