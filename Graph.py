#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pyvis.network import Network


# In[2]:


gsheetkey = "1jSxkmmJNuxqj9Sqnvoa8qafvG3XvpOhrsZJWufTTKu0"
sheet_name = 'Relationships'
url= f'https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=xlsx'

df = pd.read_excel(url, sheet_name = sheet_name, engine='openpyxl')
df.head()


# In[82]:


def build_graph(df, highlight=None):
    graph = Network(
        width = "100%",
        height= "95vh",
        directed = True,
        bgcolor = '#222222',
        font_color = 'white',
        neighborhood_highlight = True,
#         select_menu = True
#         filter_menu = True
    )
    graph.toggle_hide_edges_on_drag(True)
    graph.repulsion(
        node_distance=100,
        spring_length=200,
    )
    graph.set_edge_smooth("discrete")
    
    # add nodes
    for node in np.unique(np.concatenate(
        (df["Cause"].to_numpy(), df["Effect"].to_numpy())
    )):
        if (node == highlight):
            graph.add_node(node, node, size=10, title=node, color = "orange")
        else:
            graph.add_node(node, node, size=10, title=node)
        
    # add edges
    for src, dst, w in zip(df["Cause"].to_numpy(), df["Effect"].to_numpy(), df["Weight"].to_numpy().astype(float)):
        if w > 0:
            graph.add_edge(src, dst, arrowStrikethrough=False, color="green")
        elif w < 0:
            graph.add_edge(src, dst, arrowStrikethrough=False, color="red")
        else:
            pass

    graph.save_graph('output.html')
    
build_graph(df, "PlanetEco Profit")    

