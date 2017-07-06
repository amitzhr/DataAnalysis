import json
import math
import random
import os

def generate_indices(full_double_probs):
    indices = set()
    i = 0
    while i < 100:
        index = random.randint(0, len(full_double_probs))
        if not isinstance(full_double_probs[index], list) or index in indices:
            continue
        i += 1
        indices.add(index)

    #for m in [1221, 2023, 858, 3438, 3439, 3440, 3430, 3431, 3432, 3433, 3434, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981]:
    #    indices.add(m)
    #indices = range(1000)
    #indices = [x for x in indices if isinstance(full_double_probs, list)]
    return list(indices)

def index_probs(probs, indices):
    return [probs[i] for i in indices]

def index_double_probs(double_probs, indices):
    l = [double_probs[i] for i in indices if isinstance(double_probs[i], list)]
    return [[x[i] for i in indices] for x in l]

def index_movie_sequels(movie_sequels, indices):
    new_sequels = []
    for s in movie_sequels:
        l = []
        for x in s:
            if x in indices:
                l.append(indices.index(x))
        if l:
            new_sequels.append(l)

    return new_sequels

def read_movie_sequels(dataset_dir):
    return json.load(open(os.path.join(dataset_dir, "movie_sequels.txt"), "rb"))

def read_full_double_probs(dataset_dir):
    return json.load(open(os.path.join(dataset_dir, "full_double_probs.txt"), "rb"))

def read_full_probs(dataset_dir):
    return json.load(open(os.path.join(dataset_dir, "full_probs.txt"), "rb")), read_full_double_probs(dataset_dir)

def read_probs(dataset_dir):
    return json.load(open(os.path.join(dataset_dir, "double_probs.txt"), "rb"))

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

    json.dump(double_probs, open("double_probs.txt", "wb"))

def calculate_objective(clusters, probs, double_probs):
    if isinstance(clusters[0][0], list):
        m = 9999
        i = 1
        for c in clusters:
            x = calculate_objective(c, probs, double_probs)
            print "Obj: %d %d" % (i, x)
            if x < m:
                m = x
            i += 1
        return m

    objective = 0
    for c in clusters:
        N = len(c)
        if N == 1:
            objective += math.log(1.0 / probs[c[0]])
        else:
            for i in xrange(N):
                for j in xrange(i + 1, N):
                    objective += (1.0 / (N - 1)) * math.log(1.0 / double_probs[c[i]][c[j]])
    return objective

def pivot_cluster(probs):
    clustering = []
    N = len(probs)

    def find_random_index():
        valid_indices = [i for i in xrange(N) if isinstance(probs[i], list)]
        if len(valid_indices) == 0:
            return None
        else:
            return random.choice(valid_indices)

    i = find_random_index()
    while i is not None:
        cluster = [i]
        for j in xrange(i + 1, N):
            if not isinstance(probs[j], list):
                continue

            if probs[i][j] == 1:
                cluster.append(j)
                probs[j] = 0

        probs[i] = 0
        clustering.append(cluster)
        i = find_random_index()

    return clustering

def print_movie_names(clusters, indices, dataset_dir):
    real_clusters = []
    indices = list(indices)
    for c in clusters:
        real_c = [indices[i] for i in c]
        real_clusters.append(real_c)

    movie_dic = {}
    movies_data = open(os.path.join(dataset_dir, "movies.dat"), "rb").readlines()
    for movie_line in movies_data:
        id = movie_line.split('::')[0]
        movie_name = movie_line.split('::')[1]
        movie_dic[id] = movie_name

    for c in real_clusters:
        text_list = ["%d %s" % (movie, movie_dic[str(movie)]) for movie in c]
        print ", ".join(text_list)
