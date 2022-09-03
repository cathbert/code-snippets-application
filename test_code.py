
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(5, 5))

# l = low resolution i = intermedia resolution h = high resolution f = full resolution

m = Basemap(projection='mill',
            llcrnrlat=25,
            urcrnrlat=50,
            llcrnrlon=-130,
            urcrnrlon=-60, resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=1)
m.drawstates(color='b')

# m.drawcounties(color='darkred')
# m.fillcontinents()
# m.etopo()

# m.bluemarble()

xs = []
ys = []

# ----- Plot NewYork coordinates
NYC_lat, NYC_lon = 40.7127, -74.0059
x_point, y_point = m(NYC_lon, NYC_lat)
xs.append(x_point)
ys.append(y_point)
m.plot(x_point, y_point, 'm^', markersize=9)  # o=circle *=star ^=triangle

# ----- Plot Los Angeles coordinates
LA_lat, LA_lon = 34.05, -118.25
x_point, y_point = m(LA_lon, LA_lat)
xs.append(x_point)
ys.append(y_point)


m.plot(x_point, y_point, 'r*', markersize=9)  # o=circle *=star ^=triangle
m.plot(xs, ys, 'y', linewidth=2, label='Flight 354')
m.drawgreatcircle(NYC_lon, NYC_lat, LA_lon, LA_lat, color='c', linewidth=3, label='Arc')
plt.legend(loc=4)

plt.title("basemap tutorial")
plt.show()


