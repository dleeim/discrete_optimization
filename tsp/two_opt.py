#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import sys
import time

Point = namedtuple("Point", ["x", "y"])


# ---------- geometry ----------
def euclid(p, q):
    return math.hypot(p.x - q.x, p.y - q.y)


def build_dist_dict(points):
    n = len(points)
    D = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            d = euclid(points[i], points[j])
            D[i][j] = D[j][i] = d
        D[i][i] = 0.0  # optional, but convenient
    return D


def tour_length(tour, D):
    cost = D[tour[-1]][tour[0]]
    for a, b in zip(tour, tour[1:]):
        cost += D[a][b]
    return cost


# ---------- 2-opt using the dict-matrix ----------
def two_opt(tour, D, first_improvement=True):
    n = len(tour)
    best_delta = 0.0
    best_i = best_j = None

    for i in range(n - 1):
        a, b = tour[i], tour[i + 1]
        dab = D[a][b]

        # j loops over edges that are not adjacent to edge (a,b)
        for j in range(i + 2, n if i else n - 1):
            c, d = tour[j], tour[(j + 1) % n]
            dcd = D[c][d]

            delta = dab + dcd - D[a][c] - D[b][d]
            if delta > 1e-12:  # improvement
                if first_improvement:
                    new_tour = tour[: i + 1] + tour[i + 1 : j + 1][::-1] + tour[j + 1 :]
                    new_len = tour_length(new_tour, D)
                    return new_tour, new_len, True

                if delta > best_delta:
                    best_delta, best_i, best_j = delta, i, j

    if best_delta > 1e-12:
        i, j = best_i, best_j
        new_tour = tour[: i + 1] + tour[i + 1 : j + 1][::-1] + tour[j + 1 :]
        new_len = tour_length(new_tour, D)
        return new_tour, new_len, True

    return tour, tour_length(tour, D), False  # no improvement


# ---------- main entry ----------
def two_opt_solve_it(input_data):

    tokens = input_data.split()
    n = int(tokens[0])
    coords = list(map(float, tokens[1:]))
    points = [Point(coords[2 * i], coords[2 * i + 1]) for i in range(n)]

    D = build_dist_dict(points)

    tour = list(range(n))
    best_len = tour_length(tour, D)

    improved = True
    while improved:
        tour, best_len, improved = two_opt(tour, D, first_improvement=True)

    output = f"{best_len:.2f} 0\n" + " ".join(map(str, tour))
    return output