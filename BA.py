# author='Abdallah Sobehy'
# author_email='abdallah.sobehy@telecom-sudparis.eu'
# date='3/12/2015'	
from __future__ import division
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
import random as rd
import pylab
from matplotlib.pyplot import pause
from Tkinter import *
## 
# Creates a BA graph and shows it in a animated manner
# @param total_nodes all nodes to be present in the graph
# @param start_nodes initial nodes of the graph (unconnected)
# @param edges number of edges new node added to the graph has (should be smaller than or equal to start_nodes) 
# @param pause_time time between figure update with new node
# @param show_deg a boolean if True shows degree distribution graph.
def animate_BA(total_nodes,start_nodes,edges, pause_time, show_deg):
	# Check that edges are smaller than or equal to start_nodes
    if edges > start_nodes:
        print "starting nodes must be more than edges of incoming nodes !"
        return
    # initialize graph
    G = nx.Graph()
    # Dictionary to contain the node positions to have consistent positions shown everytime time graph is redrawn with new node
    node_pos = {}
    # Add start nodes to the graph (not connected)
    G.add_nodes_from(xrange(start_nodes))
    # Give the start nodes random poistions in the plotting area
    for i in xrange(start_nodes):
        node_pos[i] = (np.random.random(),np.random.random())
    # Initial plot with only start nodes
    fig = plt.figure('Animation of Barabasi-Albert Graph')
    fig.text(0, 0.97, 'starting nodes: green ',style='italic',fontsize=14)
    fig.text(0, 0.94, 'New node: blue ',style='italic',fontsize=14)
    fig.text(0, 0.91, 'Previously added nodes: red', style='italic',fontsize=14)
    nx.draw_networkx(G,node_pos, node_color = 'green')
    plt.draw()
    pause(pause_time)
    # Adding new node
    for i in xrange(total_nodes - start_nodes):
    	# Compute duration of calculations for consistent timing
    	loop_start_time = time.time()
    	# Call choose_neighbors to retrieve the neighbors the new node will connect to according to their degree
        neighbors = choose_neighbors(G, edges)
        # A Check to make sure the correct umber of neighbors are chosen
        if (len(neighbors) != edges):
            print "Error, number of neighbors is not as expected"
            return
        # Add the new node to the graph
        G.add_node(start_nodes + i)
        # Save new edges in a list for drawing purposed
        new_edges = []
        for n in neighbors:
            G.add_edge(start_nodes + i, n)
            new_edges.append((start_nodes + i, n))
        plt.clf()
        # Create a color map for nodes to differenctiate between: stating nodes (green), new node (blue) and already added nodes (red)
        color_map = []
        for j in G.nodes_iter():
            if j < start_nodes:
                color_map.append('green')
            elif j == start_nodes + i :
                color_map.append('blue')
            else: color_map.append('red')
        # Define new node's position and draw the graph
        node_pos[start_nodes+i]=(np.random.random(),np.random.random())
        nx.draw_networkx(G, node_pos, node_color = color_map)
        nx.draw_networkx_edges(G, node_pos,new_edges, width = 2.0 , edge_color = 'b' )
        fig = plt.figure('Animation of Barabasi-Albert Graph')
        fig.text(0, 0.97, 'starting nodes: green                 Iteration: '+ str(i+1),style='italic',fontsize=14)
        fig.text(0, 0.94, 'New node: blue ['+str(start_nodes + i) + ']',style='italic',fontsize=14)
        fig.text(0, 0.91, 'Previously added nodes: red', style='italic',fontsize=14)

        plt.draw()
        loop_duration = time.time() - loop_start_time
        # Pause for the needed time, taking the calculation time into account
        if pause_time - loop_duration > 0 :
        	pause(pause_time - loop_duration)
    if show_deg:
        print 'Press any key to continue'
        raw_input()
        degree_distributon(G)
    else:
        print 'Press any key to exit'
        raw_input()
##
# returns a list of neighbors chosen with probability: (deg(i)+1)/Sum(deg(i)+1)
# @param G graph from which the neighbors will be chosen
# @param num_of_neighbors number of neighbors will be chosen
#
def choose_neighbors(G, num_neighbors):
    # limits is a list that stores floats between 0 and 1 which defines
    # the probabaility range for each node to be chosen as a neighbor depending on its degree
    # for ex: if limits[0] = 0 and limits[1] = 0.1 then the probability of choosing node 0 as a neighbors is 0.1 - 0
    # The first element of limits is always 0 and the last element is always 1
    limits = [0.0]
    # number of edges already in the graph
    num_edges = G.number_of_edges()
    # number of nodes already in the graph
    num_nodes = G.number_of_nodes()
    # iterate nodes to calculate limits depending on degree
    for i in G:
        # Each node is assigned a range depending in the degree probability of BA so that with random number between 0 and 1 it i will be chosen
        limits.append((G.degree(i)+1)/(2*num_edges + num_nodes) + limits[i])
    # After specifying limits select_neighbors function is called to generate random numbers and choose neighbors accordingly
    return select_neighbors(limits, num_neighbors)

##
# selects neighbors by generating a random number and comparing it to the limits to choose neighbors
# @param limits probabaility range for each node 
# @param num_neighbors number of neighbors that will be chosen
# returns a list of selected nodes
#
def select_neighbors(limits, num_neighbors):
    # list to contain keys of neighbors
    neighbors = []
    # A flag to indicate a chosen neighbor has already been chosen (to prevent connecting to the same node twice)
    already_neighbor = False
    # iterate num_neighbors times to add neighbors to the list
    i = 0
    while i < num_neighbors:
        rnd = np.random.random() # random number between 0 and 1
        # compare the random number to the limits and add node accordingly
        for j in range(len(limits) - 1):
            if rnd >= limits[j] and rnd < limits[j+1]:
                # if j is already a neighbor
                if j in neighbors:
                	# Raise the flag
                    already_neighbor =True
                else:
                	# if j is not already a neighbor add it to the neighbors list
                    neighbors.append(j)    
        # if the alread_neighbor flag is true, decrement i to redo the choice randomly and reset flag               
        if already_neighbor == True:
            already_neighbor = False
            i -= 1 # To repeat the choice of the node
        i+=1
    return neighbors
##
# Draws the graph of degree against portion of nodes.
#
def degree_distributon(G):
    plt.close()
    num_nodes = G.number_of_nodes()
    max_degree = 0
    # Calculate the maximum degree to know the range of x-axis
    for n in G.nodes():
        if G.degree(n) > max_degree:
            max_degree = G.degree(n)
    # X-axis and y-axis vlaues
    x = []
    y_tmp = []
    # loop for all degrees until the maximum to compute the portion of nodes for that degree
    for i in xrange(max_degree+1):
        x.append(i)
        y_tmp.append(0)
        for n in G.nodes():
            if G.degree(n) == i:
                y_tmp[i] += 1
        y = [i/num_nodes for i in y_tmp]
    # Plot the graph
    deg, = plt.plot(x, y,label='Degree distribution',linewidth=0, marker= 'x',markersize = 8 )
    plt.ylabel('Portion of Nodes')
    plt.xlabel('Degree')
    plt.title('Degree distribution')
    plt.show()
##
# Configuration of the Barabas-Albert Graph paramaters form the GUI
#
def configure():
    error_flag = False
    # Exception if the input value is not an integer for the total nodes
    try:
        errlbl_t = Label(Gui, text='\t\t\t\t\t\t').place(relx=0.58, rely=0.1)
        t = int(total_nodes.get())
    except ValueError:
        errlbl_t = Label(Gui, text='Please enter an Integer.').place(relx=0.58, rely=0.1)
        error_flag = True
    # Exception if the input value is not an integer for the start nodes
    try:
        errlbl_s = Label(Gui, text='\t\t\t\t\t\t').place(relx=0.58, rely=0.2)
        s = int(start_nodes.get())
    except ValueError :
        errlbl_s = Label(Gui, text='Please enter an Integer.').place(relx=0.58, rely=0.2)
        error_flag = True
    # Exception if the input value is not an integer for edges
    try:
        errlbl_e = Label(Gui, text='\t\t\t\t\t\t').place(relx=0.58, rely=0.3)
        e = int(edges.get())
    except ValueError :
        errlbl_e = Label(Gui, text='Please enter an Integer.').place(relx=0.58, rely=0.3)
        error_flag = True
    # Exception if the input value is not float for pause time
    try:
        errlbl_t = Label(Gui, text='\t\t\t\t\t\t').place(relx=0.58, rely=0.4)
        p = float(pause_time.get())
    except ValueError :
        errlbl_t = Label(Gui, text='Please enter a Float.').place(relx=0.58, rely=0.4)
        error_flag = True
    # Exception if start nodes is pnegative or smaller than the number of edges
    try:
        if e > s or s<0:
            raise AttributeError()
    except AttributeError:
        errlbl_s = Label(Gui, text='Start nodes must be positive and >= Edges!').place(relx=0.58, rely=0.2)
        error_flag = True
    # Exception if the total nodes is negative or smaller than start nodes
    try:
        if t < s or t<0:
            raise AttributeError()
    except AttributeError:
        errlbl_t = Label(Gui, text='Total nodes must be positive and >= Start nodes.').place(relx=0.58, rely=0.1)
        error_flag = True
    # Exception if Edges is negative
    try:
        if e < 0:
            raise AttributeError()
    except AttributeError:
        errlbl_e = Label(Gui, text='Edges must be positive.').place(relx=0.58, rely=0.3)
        error_flag = True
    # Exception if pause time is less than or equal 0
    try:
        if p <= 0:
            raise AttributeError()
    except AttributeError:
        errlbl_t = Label(Gui, text='Please enter a positive Float.').place(relx=0.58, rely=0.4)
        error_flag = True

    if error_flag:
        return
    else:
        Gui.destroy()
        animate_BA(t,s,e,p,deg_choice.get())
        
# Main function starts here where the configuration of the graph can be written
if __name__ == "__main__":
    # Create Tkinter Object
    Gui = Tk()
    # total_nodes all nodes to be present in the graph
    total_nodes = StringVar()
    # start_nodes initial nodes of the graph (unconnected)
    start_nodes = StringVar()
    # edges number of edges new node added to the graph has (should be smaller than or equal to start_nodes)     
    edges = StringVar()
    # pause_time time between figure update with new node
    pause_time = StringVar()
    # a boolean if True shows degree distribution graph.
    deg_choice = BooleanVar()
    # Create mroot window
    Gui.geometry('750x450')
    Gui.title('Barabasi-Albert Graph Animation')

    lbl0 = Label(Gui,text= 'Animation Parameters').place(relx=0.37, rely=0.02)

    lbl1 = Label(Gui,text= 'Number of nodes').place(relx=0.1, rely=0.1) 
    entry1 = Entry(Gui, textvariable=total_nodes).place(relx=0.35, rely=0.1)

    lbl2= Label(Gui,text= 'Starting Nodes').place(relx=0.1, rely=0.2) 
    entry1 = Entry(Gui, textvariable=start_nodes).place(relx=0.35, rely=0.2)

    lbl3 = Label(Gui,text= 'New node Edges').place(relx=0.1, rely=0.3) 
    entry3 = Entry(Gui, textvariable=edges).place(relx=0.35, rely=0.3)

    lbl4 = Label(Gui,text= 'Pause time').place(relx=0.1, rely=0.4) 
    entry4 = Entry(Gui, textvariable=pause_time).place(relx=0.35, rely=0.4)

    Check_box = Checkbutton(Gui, text='Show Degree Distribution', variable = deg_choice, onvalue = True, offvalue=False).place(relx=0.09,rely = 0.5)
    btn1 = Button(Gui, text = 'Set paramaters & Animate', command=configure, bg='grey').place(relx=0.35,rely=0.5)
    lbl_end = Label(Gui,text= 'Author: Abdallah Sobehy date: 12/2015\nSupervised by: Dr. joanna Tomasik\nMsc CCN Network Algorithms').place(relx=0.25,rely=0.87)
 
    Gui.mainloop()
    
# Test Cases executed interactively
# All conditions satisfied: Integer for all text boxes, total_nodes >= start_nodes, start_nodes>= Edges, (check box True, false)
# Wrong input detection: (String values tried for each text box)
# Wrong input detection: Total nodes < start nodes
# Wrong input detection: start nodes < edges of new node
# Wrong input detection: Negative values for each text box
# Wrong input value: 0 for pause time
