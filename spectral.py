import numpy
from kmeans import kmeans, Point

def spectral(W, k):
    m = numpy.size(W, 1)
    D = numpy.diag(W * numpy.ones((m, 1)))
    L = D - W
    eigenvalues, eigenvectors = numpy.linalg.eig(L)

    indices = numpy.argsort(eigenvalues)

    eigen_sorted = eigenvalues[indices]

    # Calculate the optimal k
    eigen_diff = []
    for i in xrange(2, int(len(eigen_sorted) * 3.0 / 4.0)):
        eigen_diff.append(eigen_sorted[i+1] - eigen_sorted[i])
    k = eigen_diff.index(max(eigen_diff)) + 2

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
