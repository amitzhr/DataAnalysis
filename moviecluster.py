import pickle
import time
import math
import copy

def main():
    start_time = time.time()

    #full_probs, full_double_probs = read_full_probs()
    #convert_full_probs_to_probs(full_probs, full_double_probs)
    full_probs, full_double_probs = read_full_probs()
    clusters = pivot_cluster(read_probs())
    objective = calculate_objective(clusters, full_probs, full_double_probs)
    import pdb
    pdb.set_trace()

    end_time = time.time()
    print "Finished in %d seconds" % (end_time - start_time)

def read_full_probs():
    return pickle.load(open("full_probs.txt", "rb")), pickle.load(open("full_double_probs.txt", "rb"))

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
            if not isinstance(double_probs[i], list):
                continue
            for j in xrange(N):
                if i != j and isinstance(double_probs[j], list):
                    try:
                        if N == 1:
                            objective += math.log(1.0 / probs[c[0]])
                        else:
                            objective += (1.0 / (N - 1)) * math.log(1.0 / double_probs[i][j])
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
    while i:
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

    print counter
    return clustering

if __name__ == "__main__":
    main()
