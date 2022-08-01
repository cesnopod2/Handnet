import matplotlib.pyplot as plt
# X,Y,Z PLOT
figure = plt.Figure()
ax1 = figure.add_subplot(311)
ax2 = figure.add_subplot(312)
ax3 = figure.add_subplot(313)

x_data = []
y_data = []
z_data = []

skeleton_data = None
x_skeleton_coordinate = None
y_skeleton_coordinate = None
z_skeleton_coordinate = None

time_data = []
# SKELETON PLOT
figure_skeleton = plt.Figure()
skeleton_ax = figure_skeleton.add_subplot(111, projection='3d')
# skeleton_ax.set_xlim3d([0, 500])
# skeleton_ax.set_ylim3d([200, 1100])
# skeleton_ax.set_zlim3d([-200, 200])
skeleton_ax.xaxis.set_ticklabels([])
skeleton_ax.axes.yaxis.set_ticklabels([])
skeleton_ax.axes.zaxis.set_ticklabels([])


def animate_skeleton(i):
    global x_skeleton_coordinate, y_skeleton_coordinate, z_skeleton_coordinate
    try:
        skeleton_ax.clear()
        skeleton_ax.xaxis.set_ticklabels([])
        skeleton_ax.axes.yaxis.set_ticklabels([])
        skeleton_ax.axes.zaxis.set_ticklabels([])
        skeleton_ax.plot(x_skeleton_coordinate[0:5], y_skeleton_coordinate[0:5], z_skeleton_coordinate[0:5], ls='-',
                         color='red')
        skeleton_ax.plot(np.hstack((x_skeleton_coordinate[0], x_skeleton_coordinate[5:9])),
                         np.hstack((y_skeleton_coordinate[0], y_skeleton_coordinate[5:9])),
                         np.hstack((z_skeleton_coordinate[0], z_skeleton_coordinate[5:9])),
                         ls='-', color='blue'
                         )
        skeleton_ax.plot(np.hstack((x_skeleton_coordinate[0], x_skeleton_coordinate[9:13])),
                         np.hstack((y_skeleton_coordinate[0], y_skeleton_coordinate[9:13])),
                         np.hstack((z_skeleton_coordinate[0], z_skeleton_coordinate[9:13])),
                         ls='-', color='red'
                         )
        skeleton_ax.plot(np.hstack((x_skeleton_coordinate[0], x_skeleton_coordinate[13:17])),
                         np.hstack((y_skeleton_coordinate[0], y_skeleton_coordinate[13:17])),
                         np.hstack((z_skeleton_coordinate[0], z_skeleton_coordinate[13:17])),
                         ls='-', color='red'
                         )

        skeleton_ax.plot(np.hstack((x_skeleton_coordinate[0], x_skeleton_coordinate[17:])),
                         np.hstack((y_skeleton_coordinate[0], y_skeleton_coordinate[17:])),
                         np.hstack((z_skeleton_coordinate[0], z_skeleton_coordinate[17:])),
                         ls='-', color='blue'
                         )
        skeleton_ax.scatter3D(x_skeleton_coordinate, y_skeleton_coordinate, z_skeleton_coordinate, cmap='Greens')
    except TypeError:
        skeleton_ax.clear()


def animate_data(i):
    global x_data, y_data, z_data, time_data

    ax1.clear()
    ax2.clear()
    ax3.clear()

    ax1.plot(time_data, x_data)
    ax2.plot(time_data, y_data)
    ax3.plot(time_data, z_data)
    ax1.set_title("X coordinate")
    ax2.set_title("Y coordinate")
    ax3.set_title("Z coordinate")

    # setting visibility of axis
    ax1.get_xaxis().set_visible(False)
    ax2.get_xaxis().set_visible(False)
    ax3.get_xaxis().set_visible(False)