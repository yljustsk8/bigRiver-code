import numpy as np
import tensorflow as tf

def weight(shape):
    init=tf.random_normal(shape,stddev=0.01)
    return tf.Variable(init)

def bias(shape):
    init=tf.random_normal(shape)
    return tf.Variable(init)

def conv(x,w):
    return tf.nn.conv2d(x,w,strides=[1,1,1,1],padding="SAME")

def max_pool(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")

SIZE=64
x_data=tf.placeholder(tf.float32,[None,SIZE,SIZE,3])
y_data=tf.placeholder(tf.float32,[None,None])
prob1=tf.placeholder(tf.float32)
prob2=tf.placeholder(tf.float32)


def cnnLayer(x,w,b,keep):
    cnn=tf.nn.relu(conv(x, w)+ b)
    pool=max_pool(cnn)
    drop=tf.nn.dropout(pool,keep)

    return drop

def Network(x,classnum):

    w1 = weight([3, 3, 3, 32])
    b1 = bias([32])

    w2 = weight([3, 3, 32, 64])
    b2 = bias([64])

    w3 = weight([3, 3, 64, 64])
    b3 = bias([64])

    w4 = weight([8 * 8 * 64, 512])
    b4 = bias([512])

    w5 = weight([512, classnum])
    b5 = bias([classnum])

    #添加卷积层
    o1=cnnLayer(x,w1,b1,prob1)
    o2=cnnLayer(o1,w2,b2,prob1)
    o3=cnnLayer(o2,w3,b3,prob1)

    #添加普通层
    o3=tf.reshape(o3,[-1,8*8*64])
    o4=tf.nn.relu(tf.matmul(o3,w4)+b4)
    o4=tf.nn.dropout(o4,prob2)

    o5=tf.nn.softmax(tf.matmul(o4,w5)+b5)

    return o5

def train(x_input,y_input,save_path):
    pred=Network(x_data,y_input.shape[1])

    print("pred:",pred)
    print("y_input:",y_input.shape)

    loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred,labels=y_data))
    accuracy=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(pred,1),tf.argmax(y_input,1)),tf.float32))
    op = tf.train.AdamOptimizer(0.01).minimize(loss)

    saver=tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        batch_size=10
        batch_num=len(x_input)//batch_size
        print("batch_num:",batch_num)
        for i in range(10):
            r=np.random.permutation(len(x_input))
            train_x=x_input[r,:]
            train_y=y_input[r,:]
            print("train_x:",train_x.shape)
            print("train_y:",train_y.shape)
            for j in range(batch_num):
                feed_x=train_x[j*batch_size:(j+1)*batch_size]
                feed_y=train_y[j*batch_size:(j+1)*batch_size]

                _,_loss=sess.run([op,loss],feed_dict={x_data:feed_x,y_data:feed_y,prob1:0.75,prob2:0.75})
                print(i*batch_size+j,_loss)
            acc=accuracy.eval({x_data:train_x,y_data:train_y,prob1:1.0,prob2:1.0})
            print("times:{} accuracy:{}".format(i+1,acc))
            saver.save(sess,save_path)


def predict(x,classnum,loadpath):
    saver=tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess,loadpath)
        pred = Network(x, classnum)

        _pred=sess.run(pred,feed_dict={x_data:pred,prob1:1.0,prob2:1.0})

    return tf.argmax(_pred),tf.reduce_max(_pred)