import pickle
import time
import math
import random
from spectral import spectral

def index_probs(probs, indices):
    return [probs[i] for i in indices]

def main():
    start_time = time.time()

#    full_probs, full_double_probs = read_full_probs()
    #convert_full_probs_to_probs(full_probs, full_double_probs)
#    full_double_probs = read_full_double_probs()

#    inds = set()
#    for i in xrange(100):
#        inds.add(random.randint(0, len(full_double_probs)))
    #print "Generated %d indices" % len(inds)
#    indices = [i for i in inds if isinstance(full_double_probs[i], list)]
#    C = spectral(index_double_probs(full_double_probs, indices), 18)

#    probs = read_probs()
    #indices = [i for i in range(1, 200) if isinstance(probs[i], list)]
#    clusters = pivot_cluster(index_double_probs(probs, indices))

#    C2 = []
#    for c in C:
#        c = [indices[x] for x in c]
#        C2.append(c)

#    clusters2 = []
#    for c in clusters:
#        c = [indices[x] for x in c]
#        clusters2.append(c)

    #objective = calculate_objective(clusters2, full_probs, index_double_probs(full_double_probs, indices))
    #objective2 = calculate_objective(C2, full_probs, index_double_probs(full_double_probs, indices))
    #print "Objective1: %d, Objective2: %d" % (objective, objective2)
    #if objective < objective2:
    #    print "SABATO"
    #else:
    #    print "YOAV"

    double_probs = read_probs()
    full_probs, full_double_probs = read_full_probs()

    inds = set()
    for i in xrange(100):
        inds.add(random.randint(0, len(full_double_probs)))
    indices = [i for i in inds if isinstance(full_double_probs[i], list)]

    indexed_double_probs = index_double_probs(double_probs, indices)
    indexed_full_double_probs = index_double_probs(full_double_probs, indices)
    indexed_probs = index_probs(full_probs, indices)
    import pdb
    pdb.set_trace()
    clusters = pivot_cluster(indexed_double_probs)
    objective = calculate_objective(clusters, indexed_probs, indexed_full_double_probs)
    C = spectral(indexed_full_double_probs, 18)
    objective2 = calculate_objective(C, indexed_probs, indexed_full_double_probs)
    print "Objective1: %d Objective2: %d" % (objective, objective2)

    end_time = time.time()
    print "Finished in %d seconds" % (end_time - start_time)

def index_double_probs(double_probs, indices):
    l = [double_probs[i] for i in indices if isinstance(double_probs[i], list)]
    return [[x[i] for i in indices] for x in l]

def read_full_double_probs():
    return pickle.load(open("full_double_probs.txt", "rb"))

def read_full_probs():
    return pickle.load(open("full_probs.txt", "rb")), read_full_double_probs()

def read_probs():
    return pickle.load(open("double_probs.txt", "rb"))

def read_probs_small():
    return pickle.load(open("double_probs_small.txt", "rb"))

def convert_probs_to_small(probs):
    pickle.dump(probs[:100][:100], open("double_probs_small.txt", "wb"))

def convert_full_probs_to_probs(full_probs, full_double_probs):
    N = len(full_double_probs)
    double_probs = [0] * (N + 1)

    for i in xrange(N):
        current_member = [0] * (N + 1)
        if not isinstance(full_double_probs[i], list):
            continue
        for j in xrange(N):
            current_member[j] = int(full_double_probs[i][j] >= full_probs[i] * full_probs[j])
        double_probs[i] = current_member

    pickle.dump(double_probs, open("double_probs.txt", "wb"))

def calculate_objective(clusters, probs, double_probs):
    objective = 0
    for c in clusters:
        N = len(c)
        for i in xrange(N):
            if N == 1:
                objective += math.log(1.0 / probs[c[0]])
            else:
                for j in xrange(N):
                    if i != j:
                        try:
                            objective += (1.0 / (N - 1)) * math.log(1.0 / double_probs[c[i]][c[j]])
                        except:
                            import pdb
                            pdb.set_trace()
    return objective

def pivot_cluster(probs):
    clustering = []
    N = len(probs)

    def find_min_index():
        for i in xrange(N):
            if isinstance(probs[i], list):
                return i
        else:
            return None

    i = find_min_index()
    counter = 0
    while i is not None:
        cluster = [i]
        for j in xrange(i + 1, N):
            if not isinstance(probs[j], list):
                continue

            if probs[i][j] == 1:
                counter += 1
                cluster.append(j)
                probs[j] = 0

        probs[i] = 0
        clustering.append(cluster)
        i = find_min_index()

    #print counter
    return clustering

if __name__ == "__main__":
    main()
