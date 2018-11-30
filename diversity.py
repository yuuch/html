import pandas as pd
import plotly
from plotly import graph_objs as go
import sklearn.manifold
import numpy as np
def alpha_diversity(alpha_table, metadata,label_col):
    """ split the alpha table into serveral parts according to the metadata.
    Args:
        alpha_table: an key-value list storing the diversity for every sample
             (file name ,String)
        metadata: record the macro feature of every sample.(File name, String)
    Return :
        a dict contains every label and its samples.
        e.g. dict0 = {'class0':[0,1,2,3,4,5], 'class1': [5, 6, 7, 8, 9]}
    """
    metadata = pd.read_csv(metadata, sep='\t')
    alpha_table = pd.read_csv(alpha_table, sep='\t')
    try:
        merged = alpha_table.merge(
            metadata, left_on='Unnamed: 0', right_on='#SampleID')
    except:
        print('Wrong column name')
    tmp_col_name = alpha_table.columns[1]
    diversity = merged[tmp_col_name]
    labels = merged[label_col]
    result_dict = {}
    for i in range(len(labels)):
        key = labels[i]
        if key  in result_dict:
            result_dict[key].append(diversity[i])
        else:
            result_dict[key] =[diversity[i]]
    return result_dict

def alpha_box_plot(result_dict):
    data = []
    for ele in result_dict:
        tmp_str = '(n='+str(len(ele))+')'
        trace = go.Box(
            name = ele+tmp_str,
            y = result_dict[ele]
        )
        data.append(trace)
    layout = go.Layout(
        title = "alpha diversity"
    )
    fig = go.Figure(data=data, layout=layout)
    div = plotly.offline.plot(fig,output_type='div')
    return div

def beta_diversity(distance_matrix, metadata_file, n_components=2, col='BodySite'):
    """ obtain the visualize of the distance matrix.
    Args:
        distance_matrix:
            distance between samples.
    Return:
        a dict storing the points from the same label.
    """
    metadata = pd.read_csv(metadata_file,sep='\t')
    df = pd.read_csv(distance_matrix, sep='\t')
    df = df.set_index(df.columns[0])
    values= df.values
    embedding = sklearn.manifold.Isomap(n_components=n_components)
    X = embedding.fit_transform(values)
    cols = ['x0','x1']
    if n_components == 3:
        cols.append('x2')
    value_df = pd.DataFrame(X,index=df.index, columns=cols)
    merged = value_df.merge(metadata,left_index=True,right_on='#SampleID')
    labels = merged[col]
    indexes = merged.index
    coordinates = merged[cols]
    result_dict = {}
    for i in range(len(labels)):
        key = labels.iloc[i]
        if key in result_dict:
            result_dict[key].append(coordinates.iloc[i])
        else:
            result_dict[key] = [coordinates.iloc[i]]
    return result_dict

def plot_beta_scatter(result_dict):
    data = []
    for ele in result_dict:
        tmp = np.array(result_dict[ele])
        if len(result_dict[ele][0]) == 2:
            trace = go.Scatter(
                x = tmp[:,0],
                y = tmp[:,1],
                name = ele,
                mode = 'markers'
            )
            data.append(trace)
        else:
            trace = go.Scatter3d(
                x = tmp[:,0],
                y = tmp[:,1],
                z = tmp[:,2],
                mode = 'markers',
                name = ele
            )
            data.append(trace)
    layout = go.Layout(title="beta diversity")
    fig = go.Figure(data=data, layout=layout)
    div = plotly.offline.plot(fig,output_type='div')
    return div



    







        




    

    
    

