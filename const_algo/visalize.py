import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def main(points, tour: list, title):
  # poly: [(x0, y0), (x1, y1), (x2, y2)]
  fig = plt.figure()
  lines = [ [tour[i], tour[i+1]] for i in range(len(tour)-1)]
  lines.append([tour[-1], tour[0]])
  lc = LineCollection(lines, colors="blue")

  fig, ax = plt.subplots()
  ax.add_collection(lc)
  ax.plot([points[i][0] for i in range(len(points))], [points[i][1] for i in range(len(points))], ".", color="black", alpha=0.6)
  ax.autoscale()
  ax.set_title(title)
  plt.savefig(title)
