import sys
import random

def generate_movie_ids():
    movie_list = open("movies.dat", "rb").read().splitlines()
    bad_movies = open("bad_movies.txt", "rb").read().splitlines()
    good_movie_list = [x for x in movie_list if x.split("::")[0] not in bad_movies]
    return [x.split("::")[0] for x in random.sample(good_movie_list, 3000)]

def main():
    open(sys.argv[1], "wb").write('\n'.join(generate_movie_ids()))

if __name__ == "__main__":
    main()