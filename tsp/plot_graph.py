from pathlib import Path
from collections import namedtuple
import matplotlib.pyplot as plt

Point = namedtuple("Point", ["x", "y"])


# ── helpers ───────────────────────────────────────────────────────────
def _read_instance(path: Path):
    toks = path.read_text().strip().split()
    n = int(toks[0])
    coords = list(map(float, toks[1:]))
    return [Point(coords[2 * i], coords[2 * i + 1]) for i in range(n)]


def _read_tour(path: Path):
    *_, last = path.read_text().splitlines()  # keep only final line
    return list(map(int, last.split()))


# ── public function ──────────────────────────────────────────────────
def plot_instance(instance_path, tour_path):
    """Open a Matplotlib window/inline plot of the salesman’s route."""
    pts   = _read_instance(Path(instance_path))
    tour  = _read_tour(Path(tour_path))
    tour += [tour[0]]  # close the loop

    xs = [pts[i].x for i in tour]
    ys = [pts[i].y for i in tour]

    plt.figure(figsize=(12, 8))
    plt.plot(xs, ys, "-o", linewidth=1, markersize=3)

    for idx, p in enumerate(pts):
        plt.text(p.x, p.y, str(idx), fontsize=6,
                 ha="right", va="bottom")

    plt.axis("equal")
    plt.axis("off")
    plt.title(f"TSP tour  •  {len(pts)} cities")
    plt.show()