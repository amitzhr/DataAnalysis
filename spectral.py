import numpy
from kmeans import kmeans, Point

def spectral(double_probs, probs):
    W = double_probs[:]
    N = len(W)
    for i in xrange(N):
        for j in xrange(N):
            W[i][j] = double_probs[i][j] + 1 - probs[i] * probs[j]

    #clusters = []
    #for i in xrange(1, int(N * 2 / 3.0)):
        #clusters.append(spectral_inner(W, i))
    return spectral_inner(W, 0)

def spectral_inner(W, k):
    m = numpy.size(W, 1)
    D = numpy.diag(W * numpy.ones((m, 1)))
    L = D - W
    eigenvalues, eigenvectors = numpy.linalg.eig(L)

    indices = numpy.argsort(eigenvalues)

    eigen_sorted = eigenvalues[indices]

    # Calculate the optimal k
    eigen_diff = []
    for i in xrange(0, len(eigen_sorted) - 2):
        eigen_diff.append(eigen_sorted[i+1] - eigen_sorted[i])
    k = eigen_diff.index(max(eigen_diff)) + 1
    import pdb
    pdb.set_trace()
    print "%d, %d" % (len(W[0]), k)

    Ut = eigenvectors[:, indices[0:k]]

    f = numpy.vectorize(lambda x: x.real)
    Ut = f(Ut)

    C = kmeans([Point(x) for x in Ut], k)

    A = []
    for c in C:
        cluster = []
        for x in c.points:
            cluster.append(Ut.tolist().index(x.coords.tolist()))
        A.append(cluster)

    return A
