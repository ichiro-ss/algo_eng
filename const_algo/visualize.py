import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def main(points, tour: list, title):
    # poly: [(x0, y0), (x1, y1), (x2, y2)]
    fig = plt.figure()
    lines = [[points[tour[i]], points[tour[i+1]]] for i in range(len(tour)-1)]
    lines.append([points[tour[-1]], points[tour[0]]])
    lc = LineCollection(lines, colors="blue")

    fig, ax = plt.subplots()
    ax.add_collection(lc)
    ax.annotate("", xy=lines[0][1], xytext=lines[0][0], arrowprops=dict(width=1, headwidth=5, headlength=2))

    ax.plot([points[i][0] for i in range(len(points))], [points[i][1] for i in range(len(points))], ".", color="black", alpha=0.6)
    ax.plot(points[tour[0]][0], points[tour[0]][1], ".", color="orange", markersize=10)
    ax.autoscale()
    ax.set_title(title)

    #   boxdic = {
    #     "facecolor": "lightblue",
    #     "boxstyle": "Round",
    #   }
    #   ax.text(points[tour[0]][0], points[tour[0]][1], "start", bbox=boxdic)
    plt.savefig("vis/"+title+"png")
    plt.close()
