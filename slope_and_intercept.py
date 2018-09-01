import tensorflow as tf

tf.reset_default_graph
tf.placeholder

input = tf.placeholder(dtype=tf.float32, shape=None)
output = tf.placeholder(dtype=tf.float32, shape=None)

slope = tf.Variable(1, dtype=tf.float32)
intercept = tf.Variable(1, dtype=tf.float32)

y = slope * input + intercept

error = y - output
squared_error = tf.square(error)
loss = tf.reduce_mean(squared_error)
optimizer = tf.train.GradientDescentOptimizer(learning_rate=.01)
train = optimizer.minimize(loss)

# run the session
init = tf.global_variables_initializer()

x_values = [1,2,3,4,5,6]
y_values = [3,6,9,12,15,18]

with tf.Session() as sess:
    sess.run(init)
    for i in range(2000):
        sess.run(train, feed_dict = {input:x_values, output:y_values})
        if i % 100 == 0:
            print(sess.run([slope, intercept]))
