import pickle

class Movie(object):
    def __init__(self, id, prob):
        self.id = id
        self.prob = prob
        pass

    def __repr__(self):
        return "<Movie ID=%s prob=%f>" % (self.id, self.prob)

def main():
    data = open("ratings.dat","rb").read()
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

    pickle.dump(movie_probs, open(r"full_probs.txt", "wb"))

    s = 0
    for m in movie_objects:
        s += m.prob
    print "Sum of probs: %d" % s

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

    pickle.dump(double_prob, open(r"full_double_probs.txt", "wb"))

    sum_of_2d = 0
    for x in double_prob:
        if x:
            sum_of_2d += sum(x)

    print "Sum of double probs: %d" % sum_of_2d


if __name__ == "__main__":
    main()