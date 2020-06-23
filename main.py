import sys
import getopt
import networkx as nx
import numpy as np
from joblib import Parallel, delayed
from Simulation import Simulation
import GraphicRepresentation as gr
import GraphParser


# executes a single run of the simulation and returns the infection history
def run_sim_once(prepared_graph, number_of_steps, start_infected, multihoming, mh_immunity, virus_variables, privacy,
                 graph_type, sim_id=0):
    # if it is a generated graph, there is a new version for each simulation to avoid artifacts of one specific
    # generated graph affecting the results
    net_graph = prepared_graph
    if graph_type == 'clique':
        net_graph = nx.complete_graph(1000)
    elif graph_type == 'barbell':
        net_graph = nx.barbell_graph(500, 0)
    elif graph_type == 'barabasi':
        net_graph = nx.barabasi_albert_graph(4039, 22)
    elif graph_type == 'custom':
        net_graph = prepared_graph
    else:
        print("No valid graph type chosen.")
        exit()
    sim = Simulation(net_graph, number_of_steps=number_of_steps, start_infected=start_infected, multihoming=multihoming,
                     mh_immunity=mh_immunity, virus_variables=virus_variables, privacy=privacy, sim_id=sim_id)
    # return sim.infection_after_step
    return [sim.simple_history, sim.payout_history]


def main(argv):
    number_of_sims = 4
    kind_of_graph = 'barabasi'
    virus_variables = (24, 332, 16, 332, 1000)
    number_of_steps = 1000
    start_infected = 30
    multihoming = False
    mh_immunity = 0.5
    privacy = False
    visualisation = False
    save = False
    save_name = 'outtest'
    title = ''

    # handles additional arguments taken from command line
    # '-h' shows the proper way to use arguments
    # '-v' or '--visualisation' toggles the graph of infected over time being saved as a .png file
    # '-s' or '--save' toggles creation of a .txt save file which can be turned into a graph of infected over time later
    # '--name <filename>' sets the name for both the .png and .txt files mentioned above ("outtest" by default)
    # '-m' or '--multihoming' + ' <degree_of_mutual_immunity> toggles the possibility for both viruses to infect the
    # same node with <degree_of_mutual_immunity> being a float between 0 (no interaction with existing infections) and 1
    # (an existing infection blocks others completely - like no multihoming)
    # '--graph <graph_type>' to choose one of the provided graphs
    # TODO: Implement custom graph from file
    # TODO: Implement custom virus properties
    # '--sims <number of simulations>' sets the number of simulations to run and average for the end result
    # '--steps <number of steps>' sets the number of steps each simulation runs for
    # '--start <number at start>' sets the number of infected each virus starts with
    # '--privacy' toggles the influence of privacy levels on the simulation
    # TODO: Implement privacy values as arguments (Idea: Split into --privacy1 and --privacy2 both toggling privacy but
    #  taking values for virus 1 and 2's privacy level respectively)
    proper_format = "file.py -v -s -m\nalternative long options:\n--visualisation\n" \
                    "--graph <clique/barbell/barabasi/custom>\n--save\n--name <filename>\n--sims <#ofsims>\n" \
                    "--steps <#ofsteps>\n--start <#infectedatstart>\n--multihoming <degree_of_mutual_immunity>\n" \
                    "--privacy"
    try:
        opts, args = getopt.getopt(argv, "hvsm:", ["visualisation", "graph=", "save=", "name=", "sims=", "steps=",
                                                   "start=", "multihoming=", "privacy"])
    except getopt.GetoptError:
        print(proper_format)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(proper_format)
            sys.exit()
        elif opt in ("-v", "--visualisation"):
            visualisation = True
        elif opt in ("-s", "--save"):
            save = True
        elif opt == "--name":
            save_name = arg
        elif opt == "--graph":
            kind_of_graph = arg
        elif opt == "--sims":
            number_of_sims = int(arg)
        elif opt == "--steps":
            number_of_steps = int(arg)
        elif opt == "--start":
            start_infected = int(arg)
        elif opt in ("-m", "--multihoming"):
            multihoming = True
            mh_immunity = float(arg)
        elif opt == "--privacy":
            privacy = True

    # here the settings for different kinds of graphs are applied
    if kind_of_graph == 'clique':
        title += ' Clique Graph'
        net_graph = nx.complete_graph(1000)
        virus_variables = (6, 999, 4, 999, 10000)
    elif kind_of_graph == 'barbell':
        title += ' Barbell Graph'
        net_graph = nx.barbell_graph(500, 0)
        virus_variables = (6, 499, 4, 499, 10000)
    elif kind_of_graph == 'barabasi':
        title += ' Barabasi Albert Graph'
        net_graph = nx.barabasi_albert_graph(4039, 22)
        virus_variables = (24, 332, 16, 332, 10000)
    elif kind_of_graph == 'custom':
        title += ' Custom Graph'
        net_graph = GraphParser.read_graph_from_edge_file('peer.all.020515')
        virus_variables = (168, 2072, 112, 2072, 10000)
    else:
        print("Please choose one of the following options for a graph: clique, barbell, barabasi, custom.")
        sys.exit()

    multi_hist = Parallel(n_jobs=-1)(delayed(run_sim_once)(net_graph, number_of_steps, start_infected, multihoming,
                                                           mh_immunity, virus_variables, privacy, kind_of_graph,
                                                           sim_id=x + 1)
                                     for x in range(0, number_of_sims))
    infection_history = []
    payout_history = []
    average_total_payout_1 = 0
    for history in multi_hist:
        infection_history.append(history[0])
        payout_history.append(history[1])
        average_total_payout_1 += history[1][1][number_of_steps - 1] / len(multi_hist)
    print('Total payout 1: ' + str(int(average_total_payout_1)))
    if visualisation:
        save_as_png = save_name + '.png'
        gr.plot_average_of(infection_history, save_as=save_as_png, title=title, multihoming=multihoming)
        print("Saved as " + save_as_png)
        save_payout_as_png = save_name + '_payout.png'
        payout_title = 'Payout over Time'
        payout_y_label = 'Aggregate Payout'
        gr.plot_average_of(payout_history, save_as=save_payout_as_png, y_label=payout_y_label, title=payout_title)
        print('Saved as ' + save_payout_as_png)

    if save:
        average_history = gr.average_of_histories(multi_hist[0])
        save_as_text = save_name + '.txt'
        np.savetxt(save_as_text, average_history)
        print("Saved as " + save_as_text)
    print('Done.')
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])

