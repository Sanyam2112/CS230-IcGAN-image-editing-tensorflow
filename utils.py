import os
import errno
import numpy as np
import scipy
import scipy.misc
import matplotlib.pyplot as plt


def mkdir_p(path):

    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            print('Path already exists.')
        else:
            raise


class celebA(object):

    def __init__(self):

        self.dataname = "celebA"
        self.dims = 28 * 28
        self.shape = [28, 28, 3]
        self.image_size = 28

    def load_celebA(self):

        data = np.load('./data/celebA_img/X_8192.npy')
        label = np.load('./data/y40_8192.npy')

        return data, label

    @staticmethod
    def getNextBatch(input, input_y, rand, batch_num, batch_size=64):
        return input[rand + (batch_num) * batch_size: rand + (batch_num + 1) * batch_size], \
               input_y[rand + (batch_num) * batch_size: rand + (batch_num + 1) * batch_size]


class MnistData(object):

    def __init__(self):

        self.dataname = "mnist"
        self.dims = 28*28
        self.shape = [28 , 28 , 1]
        self.image_size = 28

    def load_mnist(self):

        data_dir = os.path.join("./data", "mnist")

        fd = open(os.path.join(data_dir, 'train-images-idx3-ubyte'))
        loaded = np.fromfile(file=fd , dtype=np.uint8)
        trX = loaded[16:].reshape((60000, 28 , 28 ,  1 )).astype(np.float)

        fd = open(os.path.join(data_dir, 'train-labels-idx1-ubyte'))
        loaded = np.fromfile(file=fd, dtype=np.uint8)
        trY = loaded[8:].reshape((60000)).astype(np.float)

        fd = open(os.path.join(data_dir, 't10k-images-idx3-ubyte'))
        loaded = np.fromfile(file=fd, dtype=np.uint8)
        teX = loaded[16:].reshape((10000, 28 , 28 , 1)).astype(np.float)

        fd = open(os.path.join(data_dir, 't10k-labels-idx1-ubyte'))
        loaded = np.fromfile(file=fd, dtype=np.uint8)
        teY = loaded[8:].reshape((10000)).astype(np.float)

        trY = np.asarray(trY)
        teY = np.asarray(teY)

        X = np.concatenate((trX, teX), axis=0)
        y = np.concatenate((trY, teY), axis=0)

        seed = 547
        np.random.seed(seed)
        np.random.shuffle(X)
        np.random.seed(seed)
        np.random.shuffle(y)

        #convert label to one-hot

        y_vec = np.zeros((len(y), 10), dtype=np.float)
        for i, label in enumerate(y):
            y_vec[i, int(y[i])] = 1.0

        return X / 255. , y_vec

    @staticmethod
    def getNextBatch(input, input_y, rand, batch_num, batch_size=64):
        return input[rand + (batch_num) * batch_size: rand + (batch_num + 1)*batch_size], \
               input_y[rand + (batch_num) * batch_size: rand + (batch_num + 1) * batch_size]

def get_image(image_path, is_grayscale=False):
    return np.array(inverse_transform(imread(image_path, is_grayscale)))

def save_images(images, size, image_path):
    return imsave(inverse_transform(images), size, image_path)

def save_images_single(image, image_path):
    return scipy.misc.imsave(image_path, image)

def imread(path, is_grayscale=False):
    if (is_grayscale):
        return scipy.misc.imread(path, flatten=True).astype(np.float)
    else:
        return scipy.misc.imread(path).astype(np.float)

def imsave(images, size, path):
    return scipy.misc.imsave(path, merge(images, size))

def merge(images, size):
    h, w = images.shape[1], images.shape[2]
    img = np.zeros((h * size[0], w * size[1], 3))
    for idx, image in enumerate(images):
        i = idx % size[1]
        j = idx // size[1]
        img[j * h:j * h + h, i * w: i * w + w, :] = image

    return img

def inverse_transform(image):
    return (image + 1.) / 2.

def read_image_list(category):
    filenames = []
    print("list file")
    list = os.listdir(category)

    for file in list:
        filenames.append(category + "/" + file)

    print("list file ending!")

    return filenames

##from caffe
def vis_square(visu_path, data, type):
    """Take an array of shape (n, height, width) or (n, height, width , 3)
       and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)"""

    # normalize data for display
    data = (data - data.min()) / (data.max() - data.min())

    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))

    padding = (((0, n ** 2 - data.shape[0]),
                (0, 1), (0, 1))  # add some space between filters
               + ((0, 0),) * (data.ndim - 3))  # don't pad the last dimension (if there is one)
    data = np.pad(data, padding, mode='constant', constant_values=1)  # pad with ones (white)

    # tilethe filters into an im age
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))

    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])

    plt.imshow(data[:, :, 0])
    plt.axis('off')

    if type:
        plt.savefig('./{}/weights.png'.format(visu_path), format='png')
    else:
        plt.savefig('./{}/activation.png'.format(visu_path), format='png')

def sample_label():

    num = 64
    label_vector = np.zeros((num , 10), dtype=np.float)
    for i in range(0 , num):
        label_vector[i , i//8] = 1.0

    return label_vector

def sample_label_celebA():

    num = 64
    feature = 40
    label_vector = np.zeros((num, feature), dtype=np.float)
    for i in range(0, num):
        for j in range(0, feature):
            label_vector[i, j] = 0

    return label_vector





