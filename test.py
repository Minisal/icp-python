import os
import icp
import time
import numpy as np
from plyfile import *
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D



# Constants
N = 10                                    # number of random points in the dataset
num_tests = 1                             # number of test iterations
num_tests_icp = 1
dim = 3                                     # number of dimensions of the points
noise_sigma = .01                           # standard deviation error to be added
translation = .1                            # max translation of the test set
rotation = .1                               # max rotation (radians) of the test set


def read_ply_xyz(filename):
    assert(os.path.isfile(filename))
    with open(filename, 'rb') as f:
        plydata = PlyData.read(f)
        num_verts = plydata['vertex'].count
        vertices = np.zeros(shape=[num_verts, 3], dtype=np.float32)
        vertices[:,0] = plydata['vertex'].data['x']
        vertices[:,1] = plydata['vertex'].data['y']
        vertices[:,2] = plydata['vertex'].data['z']
    return vertices 

def write_ply_xyz(path, points, text=True):
    """
    path: path to save: '/xx/yy/zz.ply'
    points: point clouds: size (N,3)
    """
    points = [(points[i,0], points[i,1], points[i,2]) for i in range(points.shape[0])]
    vertex = np.array(points, dtype=[('x','f4'), ('y','f4'),('z','f4')])
    el = PlyElement.describe(vertex, 'vertex', comments=['vertices'])
    PlyData([el],text=text).write(path)


def rotation_matrix(axis, theta):
    axis = axis/np.sqrt(np.dot(axis, axis))
    a = np.cos(theta/2.)
    b, c, d = -axis*np.sin(theta/2.)

    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                  [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])


def test_best_fit(A,B):

    # Generate a random dataset
    # A = np.random.rand(N, dim)

    total_time = 0

    for i in range(num_tests):

        # B = np.copy(A)

        # Translate
        # t = np.random.rand(dim)*translation
        # B += t

        # Rotate
        # R = rotation_matrix(np.random.rand(dim), np.random.rand()*rotation)
        # B = np.dot(R, B.T).T

        # Add noise
        # B += np.random.randn(N, dim) * noise_sigma

        # Find best fit transform
        start = time.time()
        T, R1, t1 = icp.best_fit_transform(B, A)
        total_time += time.time() - start

        

        # Make C a homogeneous representation of B
        # C = np.ones((N, 4))
        # C[:,0:3] = B

        # Transform C
        # C = np.dot(T, C.T).T

        # assert np.allclose(C[:,0:3], A, atol=6*noise_sigma) # T should transform B (or C) to A
        # assert np.allclose(-t1, t, atol=6*noise_sigma)      # t and t1 should be inverses
        # assert np.allclose(R1.T, R, atol=6*noise_sigma)     # R and R1 should be inverses

    print("tansform:\n",T)
    print("\nroatation:\n",R1)
    print("\ntransformation:\n",t1)
    print('\nbest fit time: {:.3}'.format(total_time/num_tests))

    return


def test_icp(A, B):

    # Generate a random dataset
    # A = np.random.rand(N, dim)

    total_time = 0

    for i in range(num_tests_icp):

        # B = np.copy(A)

        # Translate
        # t = np.random.rand(dim)*translation
        # B += t

        # Rotate
        # R = rotation_matrix(np.random.rand(dim), np.random.rand() * rotation)
        # B = np.dot(R, B.T).T

        # Add noise
        # B += np.random.randn(N, dim) * noise_sigma

        # Shuffle to disrupt correspondence
        # np.random.shuffle(B)

        # Run ICP
        start = time.time()
        T, distances, iterations = icp.icp(B, A, tolerance=0.000001)
        total_time += time.time() - start

        # Make C a homogeneous representation of B
        # C = np.ones((N, 4))
        # C[:,0:3] = np.copy(B)

        # Transform C
        # C = np.dot(T, C.T).T

        # assert np.mean(distances) < 6*noise_sigma                   # mean error should be small
        # assert np.allclose(T[0:3,0:3].T, R, atol=6*noise_sigma)     # T and R should be inverses
        # assert np.allclose(-T[0:3,3], t, atol=6*noise_sigma)        # T and t should be inverses

    print("tansform:\n", T)
    print("\nmean distance:\n", np.mean(distances))
    print("\niterations:\n", iterations)
    print('\nicp time: {:.3}'.format(total_time/num_tests))

    return T


if __name__ == "__main__":
    src = read_ply_xyz("bun000.ply")
    dst = read_ply_xyz("bun045.ply")

    # display point clouds
    fig = plt.figure()
    ax = Axes3D(fig)

    ax.scatter(src[:,0],src[:,1],src[:,2],c="black") # source
    ax.scatter(dst[:,0],dst[:,1],dst[:,2],c="blue")   # destination

    print("\n ===== test best fit =====\n")
    test_best_fit(dst, src)
    print("\n\n ===== test icp =====\n")
    T = test_icp(dst, src)

    rst = np.ones((dim+1,src.shape[0])) # make points homogeneous
    rst[:dim,:] = np.copy(src.T)
    rst = np.dot(T, rst)
    rst = rst[:dim,:].T
    ax.scatter(rst[:,0],rst[:,1],rst[:,2],c="red") # results

    # save ply
    write_ply_xyz("result.ply", rst)

    # set top view
    ax.azim=-90
    ax.dist=10
    ax.elev=90

    plt.show()

    
