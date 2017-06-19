def partition(collection):
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset
        yield [ [ first ] ] + smaller


something = list(range(1,80))

c = []
for n, p in enumerate(partition(something), 1):
    if len(p) == 10:
        c.append(sorted(p))
    if n > 9999999:
        break

import pdb
pdb.set_trace()


