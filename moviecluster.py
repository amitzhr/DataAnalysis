import pickle
import time
import math
import random
import os
import delta_cluster
import spectral
import pivot_cluster

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

    double_probs = pivot_cluster.read_probs()
    full_probs, full_double_probs = pivot_cluster.read_full_probs()
    movie_sequels = pivot_cluster.read_movie_sequels()

    while True:
        try:
            os.system("pause")
            reload(spectral)
            reload(pivot_cluster)
            reload(delta_cluster)
            indices = pivot_cluster.generate_indices(full_double_probs)

            indexed_double_probs = pivot_cluster.index_double_probs(double_probs, indices)
            indexed_full_double_probs = pivot_cluster.index_double_probs(full_double_probs, indices)
            indexed_probs = pivot_cluster.index_probs(full_probs, indices)
            indexed_movie_sequels = pivot_cluster.index_movie_sequels(movie_sequels, indices)

            clusters = pivot_cluster.pivot_cluster(indexed_double_probs[:])
            clusters2 = delta_cluster.delta_cluster(indexed_probs, indexed_double_probs[:], indexed_movie_sequels)
            objective = pivot_cluster.calculate_objective(clusters, indexed_probs, indexed_full_double_probs)
            objective2 = pivot_cluster.calculate_objective(clusters2, indexed_probs, indexed_full_double_probs)

            pivot_cluster.print_movie_names(clusters, indices)
            pivot_cluster.print_movie_names(clusters2, indices)
            print "Objective1: %d Objective2: %d" % (objective, objective2)
            print "Len1: %d Len2: %d" % (len(clusters), len(clusters2))

        except KeyboardInterrupt:
            break
        except:
            import traceback
            traceback.print_exc()

    end_time = time.time()
    print "Finished in %d seconds" % (end_time - start_time)


if __name__ == "__main__":
    main()
