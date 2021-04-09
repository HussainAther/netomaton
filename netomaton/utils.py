import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.collections as mcoll


def plot_grid(activities, shape=None, slice=-1, title='', colormap='Greys', vmin=None, vmax=None,
              node_annotations=None, show_grid=False):
    if shape is not None:
        activities = np.array(activities).reshape((len(activities), shape[0], shape[1]))[slice]
    cmap = plt.get_cmap(colormap)
    plt.title(title)
    plt.imshow(activities, interpolation='none', cmap=cmap, vmin=vmin, vmax=vmax)

    if node_annotations is not None:
        for i in range(len(node_annotations)):
            for j in range(len(node_annotations[i])):
                plt.text(j, i, node_annotations[i][j], ha="center", va="center", color="grey",
                         fontdict={'weight':'bold','size':6})

    if show_grid:
        plt.grid(which='major', axis='both', linestyle='-', color='grey', linewidth=0.5)
        plt.xticks(np.arange(-.5, len(activities[0]), 1), "")
        plt.yticks(np.arange(-.5, len(activities), 1), "")
        plt.tick_params(axis='both', which='both', length=0)

    plt.show()


def plot_grid_multiple(ca_list, shape=None, slice=-1, titles=None, colormap='Greys', vmin=None, vmax=None):
    cmap = plt.get_cmap(colormap)
    for i in range(0, len(ca_list)):
        plt.figure(i)
        if titles is not None:
            plt.title(titles[i])
        activities = list(ca_list[i])
        if shape is not None:
            activities = np.array(activities).reshape((len(activities), shape[0], shape[1]))[slice]
        plt.imshow(activities, interpolation='none', cmap=cmap, vmin=vmin, vmax=vmax)
    plt.show()


def animate(activities, title='', shape=None, save=False, interval=50, colormap='Greys', vmin=None, vmax=None,
            show_grid=False, show_margin=True, scale=0.6, dpi=80):
    if shape is not None:
        activities = _reshape_for_animation(activities, shape)
    cmap = plt.get_cmap(colormap)
    fig, ax = plt.subplots()
    plt.title(title)
    if not show_margin:
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    grid_linewidth = 0.0
    if show_grid:
        plt.xticks(np.arange(-.5, len(activities[0][0]), 1), "")
        plt.yticks(np.arange(-.5, len(activities[0]), 1), "")
        plt.tick_params(axis='both', which='both', length=0)
        grid_linewidth = 0.5

    vertical = np.arange(-.5, len(activities[0][0]), 1)
    horizontal = np.arange(-.5, len(activities[0]), 1)
    lines = ([[(x, y) for y in (-.5, horizontal[-1])] for x in vertical] +
             [[(x, y) for x in (-.5, vertical[-1])] for y in horizontal])
    grid = mcoll.LineCollection(lines, linestyles='-', linewidths=grid_linewidth, color='grey')
    ax.add_collection(grid)

    im = plt.imshow(activities[0], animated=True, cmap=cmap, vmin=vmin, vmax=vmax)
    if not show_margin:
        baseheight, basewidth = im.get_size()
        fig.set_size_inches(basewidth*scale, baseheight*scale, forward=True)

    i = {'index': 0}
    def updatefig(*args):
        i['index'] += 1
        if i['index'] == len(activities):
            i['index'] = 0
        im.set_array(activities[i['index']])
        return im, grid
    ani = animation.FuncAnimation(fig, updatefig, interval=interval, blit=True, save_count=len(activities))
    if save:
        ani.save('evolved.gif', dpi=dpi, writer="imagemagick")
    plt.show()


def animate_plot1D(x, y, save=False, interval=50, dpi=80):
    fig1 = plt.figure()
    line, = plt.plot(x, y[0])
    def update_line(activity):
        line.set_data(x, activity)
        return line,
    ani = animation.FuncAnimation(fig1, update_line, frames=y, blit=True, interval=interval)
    if save:
        ani.save('plot.gif', dpi=dpi, writer="imagemagick")
    plt.show()


def _reshape_for_animation(activities, shape):
    if len(shape) == 1:
        assert shape[0] == len(activities[0]), "shape must equal the length of an activity vector"
        new_activities = []
        for i, a in enumerate(activities):
            new_activity = []
            new_activity.extend(activities[0:i+1])
            while len(new_activity) < len(activities):
                new_activity.append([0]*len(activities[0]))
            new_activities.append(new_activity)
        return np.array(new_activities)
    elif len(shape) == 2:
        return np.reshape(activities, (len(activities), shape[0], shape[1]))
    else:
        raise Exception("shape must be a tuple of length 1 or 2")


def plot_network(adjacency_matrix, layout="shell", with_labels=True, node_color="#1f78b4", node_size=300):
    G = nx.MultiDiGraph()
    for n, _ in enumerate(adjacency_matrix):
        G.add_node(n)
    for row_index, row in enumerate(adjacency_matrix):
        for node_index, val in enumerate(row):
            if val != 0.:
                G.add_edge(row_index, node_index)

    if layout == "shell":
        nx.draw_shell(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
    elif layout == "spring":
        nx.draw_spring(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
    elif isinstance(layout, dict):
        nx.draw(G, pos=layout, with_labels=with_labels, node_color=node_color, node_size=node_size)
    else:
        raise Exception("unsupported layout: %s" % layout)
    plt.show()


def animate_network(adjacency_matrices, save=False, interval=50, dpi=80, layout="shell",
                    with_labels=True, node_color="b", node_size=30):
    fig, ax = plt.subplots()

    def update(adjacency_matrix):
        ax.clear()

        G = nx.MultiDiGraph()
        for n, _ in enumerate(adjacency_matrix):
            G.add_node(n)
        for row_index, row in enumerate(adjacency_matrix):
            for node_index, val in enumerate(row):
                if val != 0.:
                    G.add_edge(row_index, node_index)

        if layout == "shell":
            nx.draw_shell(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
        elif layout == "spring":
            nx.draw_spring(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
        elif isinstance(layout, dict):
            nx.draw(G, pos=layout, with_labels=with_labels, node_color=node_color, node_size=node_size)
        else:
            raise Exception("unsupported layout: %s" % layout)

    ani = animation.FuncAnimation(fig, update, frames=adjacency_matrices, interval=interval,
                                  save_count=len(adjacency_matrices))
    if save:
        ani.save('evolved.gif', dpi=dpi, writer="imagemagick")
    plt.show()


def animate_connectivity_map(connectivity_maps, save=False, interval=50, dpi=80, layout="shell",
                    with_labels=True, node_color="b", node_size=30):
    fig, ax = plt.subplots()

    def update(connectivity_map):
        ax.clear()

        G = connectivity_map_to_nx(connectivity_map)

        if layout == "shell":
            nx.draw_shell(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
        elif layout == "spring":
            nx.draw_spring(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
        elif isinstance(layout, dict):
            nx.draw(G, pos=layout, with_labels=with_labels, node_color=node_color, node_size=node_size)
        else:
            raise Exception("unsupported layout: %s" % layout)

    ani = animation.FuncAnimation(fig, update, frames=connectivity_maps.values(), interval=interval,
                                  save_count=len(connectivity_maps))
    if save:
        ani.save('evolved.gif', dpi=dpi, writer="imagemagick")
    plt.show()


def connectivity_map_to_nx(connectivity_map):
    G = nx.MultiDiGraph()
    for node in connectivity_map:
        G.add_node(node)
        for from_node, connection_state in connectivity_map[node].items():
            for _ in connection_state:
                G.add_edge(from_node, node)
    return G


def get_node_degrees(connectivity_map):
    node_in_degrees = {}
    node_out_degrees = {}
    for k, v in connectivity_map.items():
        if k not in node_in_degrees:
            node_in_degrees[k] = 0
        for k2 in v:
            if k2 not in node_out_degrees:
                node_out_degrees[k2] = 0
            n = len(v[k2])
            node_out_degrees[k2] += n
            node_in_degrees[k] += n
    return node_in_degrees, node_out_degrees
