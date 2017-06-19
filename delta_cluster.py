import pickle

def n_plus(i, double_probs):
    a = []
    for j in xrange(len(double_probs[i])):
        if double_probs[j] and double_probs[i][j] == 1:
            a.append(j)
    if i not in a:
        print "WTF n plus"
        import pdb
        pdb.set_trace()
    return a

def is_delta_good(C, i, delta, double_probs):
    n_plus_v = n_plus(i, double_probs)
    condition_a = len([x for x in C if x in n_plus_v]) >= (1 - delta) * len(C)
    condition_b = len([x for x in n_plus_v if x not in C]) <= delta * len(C)
    return condition_a

def delta_cluster(probs, double_probs, movie_sequels):
    clustering = []
    N = len(double_probs)
    delta = 1 / 44.0

    def find_best_index():
        best_index = None
        max_prob = 0
        for i in xrange(N):
            if isinstance(double_probs[i], list) and probs[i] > max_prob:
                max_prob = probs[i]
                best_index = i
        return best_index

    i = find_best_index()
    while i is not None:
        cluster = n_plus(i, double_probs)
        new_cluster = cluster[:]
        for j in cluster:
            if not is_delta_good(new_cluster, j, 3 * delta, double_probs):
                new_cluster.remove(j)

        members_to_add = []
        for j in xrange(N):
            if isinstance(double_probs[j], list) and j not in new_cluster:
                if is_delta_good(new_cluster, j, 7 * delta, double_probs):
                    members_to_add.append(j)
        new_cluster += members_to_add

        # Check sequels
        for c in new_cluster:
            for s in movie_sequels:
                if c in s:
                    for x in s:
                        if x not in new_cluster:
                            new_cluster.append(x)

        clustering.append(new_cluster)

        for j in new_cluster:
            double_probs[j] = 0

        i = find_best_index()

    print clustering
    return clustering