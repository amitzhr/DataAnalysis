def n_plus(i, double_probs, probs):
    try:
        a = []
        for j in xrange(len(double_probs[i])):
            if double_probs[j] and double_probs[i][j] >= probs[i] * probs[j]:
                a.append(j)
        if i not in a:
            print "WTF n plus"
            import pdb
            pdb.set_trace()
        return a
    except:
        import pdb
        pdb.set_trace()

def is_delta_good(C, i, delta, double_probs, probs):
    s1 = 0
    s2 = 0
    for x in C:
        if x != i:
            s1 += double_probs[i][x]
            s2 += probs[i] * probs[x]

    return s1 >= (1 + delta) * s2

def delta_cluster(double_probs, probs):
    clustering = []
    N = len(double_probs)
    delta = 1.0

    def find_min_index():
        for i in xrange(N):
            if isinstance(double_probs[i], list):
                return i
        else:
            return None

    i = find_min_index()
    while i is not None:
        cluster = n_plus(i, double_probs, probs)
        new_cluster = cluster[:]
        for j in cluster:
            if j != i and not is_delta_good(new_cluster, j, 3 * delta, double_probs, probs):
                new_cluster.remove(j)

        members_to_add = []
        for j in xrange(N):
            if isinstance(double_probs[j], list) and j not in new_cluster:
                if is_delta_good(new_cluster, j, 7 * delta, double_probs, probs):
                    members_to_add.append(j)
        new_cluster += members_to_add

        clustering.append(new_cluster)
        if i not in new_cluster:
            print "WTF delta_cluster"
            import pdb
            pdb.set_trace()

        for j in new_cluster:
            double_probs[j] = 0

        i = find_min_index()

    print clustering
    return clustering