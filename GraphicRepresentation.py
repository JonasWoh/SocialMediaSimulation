import matplotlib.pyplot as plt


# takes an array of arrays each containing a number value for each node (0 = not infected, 1 = infected by virus 1, 2 =
# infected by virus 2, 3 = infected by both virus 1 and 2) representing the status of the graph at each step
# returns an array consisting of [number of the current step], [number of infected_v1] and [number of infected v_2]
# representing the aggregate infected per virus at each step
def convert_infection_after_step(infection_after_step):
    total_infected = [[], [], []]
    counter = 0
    for step in infection_after_step:
        infected_v1 = 0
        infected_v2 = 0
        for n in step:
            if n == 1:
                infected_v1 += 1
            if n == 2:
                infected_v2 += 1
            # only for multihoming
            if n == 3:
                infected_v1 += 1
                infected_v2 += 1
        total_infected[0].append(counter)
        total_infected[1].append(infected_v1)
        total_infected[2].append(infected_v2)
        counter += 1
    return total_infected


# takes an array consisting of [number of the current step], [number of infected_v1] and [number of infected v_2]
# optionally labels for x- and y-axis, a title and a path to save the result to
# plots a graph showing the numbers of infected per virus for each step and saves it
def plot_converted(total_infected, x_label='Time', y_label='Users', title='',
                   save_as='outtest.png', multihoming=False):
    _, whole_plot = plt.subplots()
    v1, = whole_plot.plot(total_infected[0], total_infected[1], lw=1, color='green', alpha=1)  # virus 1 is plotted
    v2, = whole_plot.plot(total_infected[0], total_infected[2], lw=1, color='red', alpha=1)  # virus 2 is plotted
    if multihoming:
        v3, = whole_plot.plot(total_infected[0], total_infected[3], lw=1, color='blue', alpha=1)  # multihoming users
        _.legend((v1, v2, v3), ('Company 1', 'Company 2', 'Shared Users'), 'center right')
    else:
        _.legend((v1, v2), ('Company 1', 'Company 2'), 'center right')
    # whole_plot.set_title(title)  # activate if graph needs a title
    whole_plot.set_xlabel(x_label)
    whole_plot.set_ylabel(y_label)
    plt.savefig(save_as)


# takes an array of simulation histories of identical lengths consisting of number of infected per virus per step
# returns an array containing the average number of infected per virus per step among all simulations
def average_of_histories(multiple_histories, multihoming=False):
    length = len(multiple_histories[0][0])
    number_of_histories = len(multiple_histories)
    if multihoming:
        # prepares the array to be filled
        average_history = [[h for h in range(0, length)], [0 for h in range(0, length)], [0 for h in range(0, length)],
                           [0 for h in range(0, length)]]
        for history in multiple_histories:
            for n in range(0, length):
                average_history[1][n] += history[1][n] / number_of_histories
                average_history[2][n] += history[2][n] / number_of_histories
                average_history[3][n] += history[3][n] / number_of_histories
    else:
        average_history = [[h for h in range(0, length)], [0 for h in range(0, length)], [0 for h in range(0, length)]]
        for history in multiple_histories:
            for n in range(0, length):
                average_history[1][n] += history[1][n] / number_of_histories
                average_history[2][n] += history[2][n] / number_of_histories
    return average_history


# takes an array of histories <multiple_histories> of identical length, labels for x- and y-axis and a title
# calculates the average numbers of infected for each virus per step
# plots the result as a visual graph
def plot_average_of(multiple_histories, x_label='Time', y_label='Users', title='',
                    save_as='outtest.png', multihoming=False):

    average_history = average_of_histories(multiple_histories, multihoming=multihoming)
    if len(multiple_histories) != 1:
        title = title + " (Average of %d Simulations)" % (len(multiple_histories))
    plot_converted(average_history, x_label, y_label, title, save_as=save_as, multihoming=multihoming)
