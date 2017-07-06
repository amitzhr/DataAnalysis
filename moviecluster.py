import time
import os
import delta_cluster
import spectral
import pivot_cluster
import sys

def load_movie_ids(subset_file_path, dataset_dir):
    assert os.path.exists(subset_file_path), "subset path doesn't exist!"
    data = open(subset_file_path, "rb").read()
    movie_ids = [int(x) for x in data.splitlines()]
    bad_movie_ids = [int(x) for x in open(os.path.join(dataset_dir, "bad_movies.txt"), "rb").read().splitlines()]
    for x in movie_ids:
        if x in bad_movie_ids:
            raise Exception("Bad movie ID %d given! (Not above 10 ratings?)" % x)
    return movie_ids

def correlation_main(dataset_dir, subset_file_path):
    double_probs = pivot_cluster.read_probs(dataset_dir)
    full_probs, full_double_probs = pivot_cluster.read_full_probs(dataset_dir)
    movie_ids = load_movie_ids(subset_file_path, dataset_dir)

    indexed_double_probs = pivot_cluster.index_double_probs(double_probs, movie_ids)
    indexed_full_double_probs = pivot_cluster.index_double_probs(full_double_probs, movie_ids)
    indexed_probs = pivot_cluster.index_probs(full_probs, movie_ids)

    clusters = pivot_cluster.pivot_cluster(indexed_double_probs[:])
    objective = pivot_cluster.calculate_objective(clusters, indexed_probs, indexed_full_double_probs)

    pivot_cluster.print_movie_names(clusters, movie_ids, dataset_dir)
    print "Objective: %d" % objective

def improved_main(dataset_dir, subset_file_path):
    double_probs = pivot_cluster.read_probs(dataset_dir)
    full_probs, full_double_probs = pivot_cluster.read_full_probs(dataset_dir)
    movie_ids = load_movie_ids(subset_file_path, dataset_dir)
    movie_sequels = pivot_cluster.read_movie_sequels(dataset_dir)

    indexed_double_probs = pivot_cluster.index_double_probs(double_probs, movie_ids)
    indexed_full_double_probs = pivot_cluster.index_double_probs(full_double_probs, movie_ids)
    indexed_probs = pivot_cluster.index_probs(full_probs, movie_ids)
    indexed_movie_sequels = pivot_cluster.index_movie_sequels(movie_sequels, movie_ids)

    clusters = delta_cluster.delta_cluster(indexed_probs, indexed_double_probs[:], indexed_movie_sequels)
    objective = pivot_cluster.calculate_objective(clusters, indexed_probs, indexed_full_double_probs)

    pivot_cluster.print_movie_names(clusters, movie_ids, dataset_dir)
    print "Objective: %d" % objective

def main():
    start_time = time.time()

    assert len(sys.argv) == 4, "Incorrect number of parameters!"
    dataset_dir = sys.argv[1]
    mode = int(sys.argv[2])
    subset_file_path = sys.argv[3]
    assert mode in [1,2], "Incorrect mode given!"

    if mode == 1:
        correlation_main(dataset_dir, subset_file_path)
    elif mode == 2:
        improved_main(dataset_dir, subset_file_path)

    end_time = time.time()
    print "Finished in %d seconds" % (end_time - start_time)

if __name__ == "__main__":
    main()
