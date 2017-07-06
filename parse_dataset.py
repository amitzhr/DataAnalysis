import json

class Movie(object):
    def __init__(self, id, prob):
        self.id = id
        self.prob = prob
        pass

    def __repr__(self):
        return "<Movie ID=%s prob=%f>" % (self.id, self.prob)

def main():
    data = open("ratings.dat", "rb").read()
    lines = data.splitlines()
    movie_user = []
    for line in lines:
        movie_user.append([int(x) for x in line.split("::")[0:2]])

    movies = {}
    for mu in movie_user:
        movie_id = mu[1]
        if movie_id not in movies:
            movies[movie_id] = set()
        movies[movie_id].add(mu[0])

    print "Num of movies: %d" % len(movies)
    for m, v in movies.items():
        if len(v) < 10:
            del movies[m]

    users = {}
    for mu in movie_user:
        user_id = mu[0]
        if mu[1] not in movies:
            continue
        if user_id not in users:
            users[user_id] = set()
        users[user_id].add(mu[1])

    N = len(users.keys())
    k = len(movies.keys())

    movie_objects = []
    for movie_id, users_ids in movies.items():
        sigma = 0
        for user in users_ids:
            sigma += +  2.0 / len(users[user])
        prob = (1.0 / (N + 1) ) * ( (2.0 / k) + sigma)
        movie_objects.append(Movie(movie_id, prob))

    movie_probs = [0] * (N + 1)
    for movie in movie_objects:
        movie_probs[movie.id] = movie.prob

    json.dump(movie_probs, open(r"full_probs.txt", "wb"))

    import pdb
    pdb.set_trace()

    max_index = max(movies.keys()) + 1

    double_prob = [0] * max_index
    for movie_id, user_ids in movies.items():
        probs = [0] * max_index
        for movie_id2, user_ids2 in movies.items():
            epsilon = 0
            for u in user_ids:
                if u in user_ids2:
                    ni = len(users[u])
                    epsilon += 2.0 / (ni * (ni - 1))
            probs[movie_id2] = (1.0 / (N + 1)) * ((2.0 / (k * (k - 1))) + epsilon)
        double_prob[movie_id] = probs

    bad_movies = []
    for i in xrange(len(double_prob)):
        if not isinstance(double_prob[i], list):
            bad_movies.append(str(i))
    open("bad_movies.txt", "wb").write("\n".join(bad_movies))

    json.dump(double_prob, open(r"full_double_probs.txt", "wb"))

    parse_movie_sequels()

def strip_movie_name(movie_name):
    REMOVE = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', '1', '2', '3', '4', '5', '6', 'Part', 'The', ':', ',']
    # Remove the year
    movie_name = ' '.join(movie_name.split(' ')[:-1])

    # Remove everything after ':'
    movie_name = movie_name.split(':')[0]

    for x in REMOVE:
        movie_name = movie_name.replace(x, "")
    movie_name = movie_name.strip()
    return movie_name

def parse_movie_sequels():
    movie_dic = {}
    movies_data = open("movies.dat", "rb").readlines()
    for movie_line in movies_data:
        id = int(movie_line.split('::')[0])
        movie_name = movie_line.split('::')[1]
        movie_dic[id] = strip_movie_name(movie_name)

    sequels = []
    for id, name in movie_dic.iteritems():
        s = []
        for id2, name2 in movie_dic.iteritems():
            if name == name2 and id != id2:
                s.append(id2)
        if len(s) > 0:
            s.append(id)
            s.sort()
            if s not in sequels:
                sequels.append(s)
    json.dump(sequels, open("movie_sequels.txt", "wb"))


if __name__ == "__main__":
    main()