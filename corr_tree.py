from Bio import Phylo
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot, plot
init_notebook_mode(connected=True)
import plotly.graph_objs as go
import math
import gini_index_compute
def get_branch_depth(clade):
    if clade.clades:
        clade.child ={}
        for subclade in clade.clades:
            #print(subclade.name)
            clade.child[subclade]= get_branch_depth(subclade)+1
        clade.depth = max(clade.child.values())
        return max(clade.child.values())
    else:
        clade.child = {}
        clade.depth = 0
        return 0
def get_y_coordinates(tree):
    """
    Associates to  each clade an x-coord.
       returns dict {clade: x-coord}
    """
    '''
    xcoords = tree.depths()
    #print(xcoords)
    #tree.depth() maps tree clades to depths (by branch length).
    #returns a dict {clade: depth} where clade runs over all Clade instances of the tree, and depth is the distance from root
    #to clade
    
    #  If there are no branch lengths, assign unit branch lengths
    
    if not max(xcoords.values()):
        xcoords = tree.depths(unit_branch_lengths=True)
    else:
        M = max(xcoords.values())
        for ele in xcoords:
            xcoords[ele]=M-xcoords[ele]
    #print('xcoords')
    #print(xcoords)
    #M = max(xcoords.values())
    #for ele in xcoords:
    #    xcoords[ele]=math.log2(1+((xcoords[ele]+M)/(M+M)))
    #    xcoords[ele]=-math.exp(-(xcoords[ele])**2)
    '''
    """
    xcoords = tree.depths(unit_branch_lengths=True)
    M = max(xcoords.values())
    for ele in xcoords:
        xcoords[ele]=M-xcoords[ele]
    """
    '''
    for ele in tree.get_terminals():
        xcoords[ele]=0
    '''
    xcoords = {}
    get_branch_depth(tree.root)
    for clade in tree.find_clades(order='level'):
        xcoords[clade] = clade.depth
    return xcoords

def corr(array, corr_type='spearman', col_label=col_label):
    #initial_seq = [0,0.0]
    # stats.corr.
    """get the correlation betweent two  arrays which possess the same length
    Return:
        correlation value: emmm..
        pvalue: the null hypothesis is arr1 and arr2 are not uncorrelated.
        For example, it will return (0.9,0.0) which means thre corr is 0.9 and
        arr1 and arr2 are significantly correlated.
    """
    methods = {'spearman':stats.spearmanr,
               'pearson':stats.pearsonr
               }
    method = methods[corr_type]
    return method(array,col_label)

def get_x_coordinates(tree, dist=1):
    """Get the x coordinates.
    Args:
        tree: a tree with sample_dict, which can be generate from
            the gini index compute module.
        corr:
            a method which compute the correlation between two arrays.
    Return:
       returns  dict {clade: y-coord}
       The y-coordinates are  (float) multiple of integers (i*dist below)
       dist depends on the number of tree leafs
        """
    for clade in tree.find_clades(order='level'):
        #TODO corr function
        ycoords[clade] = corr(clade.sample_dict.values())
    return ycoords

def get_lines(tree,clade,xcoords,ycoords,traces):
    path = tree.get_path(clade)
    x0 = xcoords[clade]
    y0 = ycoords[clade]
    if len(path)>1:
        parent= path[-2]
        x_p = xcoords[parent]
        y_p = ycoords[parent]
        trace_p = go.Scatter(# trace parent vertical line
            x = (x0,x0),
            y = (y0,y_p),
            marker=dict(color='rgb(25,25,25)'),
            mode = 'lines',
            hoverinfo='none'
        )
        traces.append(trace_p)
    else:
        if len(path) == 1: # this calde is the subclade of root
            y_r = ycoords[tree.root]
            trace_p = go.Scatter(x=(x0,x0),
                                y=(y0,y_r),
                                 mode='lines',
                                 marker =dict(color='rgb(25,25,25)'),
                                 hoverinfo='none'
                                )
            traces.append(trace_p)

            
    if clade.clades:
        x_l = xcoords[clade.clades[0]]
        x_r = xcoords[clade.clades[-1]]
        trace_c = go.Scatter(
        x = (x_l,x_r),
        y = (y0,y0) ,
        marker=dict(color='rgb(25,25,25)'),
        mode = 'lines',
        hoverinfo='none'
        )
        traces.append(trace_c)
        for ele in clade.clades:
            get_lines(tree,ele,xcoords,ycoords,traces=traces)
    else:
        pass

        '''
        # dash lines
        if y0 >0:
            trace_t = go.Scatter(
            line = dict(color='rgb(25,25,25)',dash='dash'),
            mode = 'lines',
            hoverinfo='none',
            x =(x0,x0),
            y=(y0,0))
            traces.append(trace_t)
        '''
def plot_tree(tree):
    text_dict ={}
    i = 0
    for clade in tree.find_clades(order='level'):
        if clade.name:
            text_dict[clade]='<br>name:'+clade.name+'<br> clade num:'+str(i)
        else:
            text_dict[clade]='<br>clade num:'+str(i)
        i+=1
    #tree = Phylo.read('test_tree.nwk','newick')
    y_coords = get_y_coordinates(tree)
    x_coords = get_x_coordinates(tree)
    X = []
    Y = []
    text = []
    for key in x_coords.keys():
        X.append(x_coords[key])
        Y.append(y_coords[key])
        text.append(text_dict[key])
    traces = []
    get_lines(tree,tree.root,x_coords,y_coords,traces=traces)
    trace = go.Scatter(
        x = X,
        y = Y,
        mode = 'markers',
        text= text,
        name=''
    )
    data = [trace]
    layout = dict(showlegend=False,
            xaxis=dict(
                autorange=True,
                 showgrid=False,
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False
                ),
            yaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False
                ),
            hovermode = 'closest'
    )
    for ele in traces:
        data.append(ele)
    fig =go.Figure(data=data,layout=layout)
    tree_div = plot(fig,output_type='div')
    return tree_div
def run_this_script(tree_file, feature_table):
    tree = gini_index_compute.perform(tree_file, feature_table)
    div = plot_tree(tree)
    return div
if __name__ == "__main__":
    #tree = Phylo.read('test_tree.nwk','newick')
    tree = gini_index_compute.perform()
    f = open('tree_test.html','w')
    f.write(plot_tree(tree))