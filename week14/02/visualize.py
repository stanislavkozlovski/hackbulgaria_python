import matplotlib
matplotlib.use("gtk")

import matplotlib.pyplot as plot

from read_db import calculate_server_occurences
result = calculate_server_occurences()
plot.bar(range(len(result)), result.values(), align='center')
plot.xticks(range(len(result)), result.keys())
plot.hist([vl for vl in calculate_server_occurences().values()], 50, normed=1, facecolor='green', alpha=0.75)
plot.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
plot.axis([40, 160, 0, 0.03])
plot.grid(True)
plot.show()