import corr_tree_new
import pandas as pd 
import copy 
import numpy as np 
import sklearn
def get_terminal_length(tree):
    terminal_lengths = {}
    for terminal in tree.get_terminals():
        path = tree.get_path(terminal)
        TBL = 0 # terminal branch length
        for ele in path:
            TBL += ele.branch_length
        terminal_lengths[terminal] = TBL
    sorted_terminal = sorted(terminal_lengths,key=terminal_lengths.get,reverse=True)
    sorted_terminal_lengths ={}
    for ele in sorted_terminal:
        sorted_terminal_lengths[ele] = terminal_lengths[ele]
   # print(sorted_terminal_lengths)
    return sorted_terminal_lengths

def cut_tree(tree,cp=0.2):
    """ 
    cut some branches of the tree.
    return the pruned branches.
    Args:
        tree: a Phylo.tree object
        cp: a percent used to cut the edge.
    """
    cp = 1-cp
    clades = []
    const = 1 # limit the terminal of a subtree
    terminal_lengths = get_terminal_length(tree)
    for terminal in terminal_lengths:
        current_terminals = tree.get_terminals()
        if not terminal in current_terminals:
            continue
        threshold = terminal_lengths[terminal]*cp
        temp = 0
        path = tree.get_path(terminal)
        for ele in path:
            temp += ele.branch_length
            if temp > threshold:
                #if not ele in current_terminals:
                    
                if len(ele.get_terminals()) > const:
                    backup = copy.copy(ele)
                    ele.clades = []
                    clades.append(backup)
                break
    return clades
def get_mvp_tree(feature_table_path, tree_path, metadata_path):
    mvp_tree = corr_tree_new.MvpTree(feature_table_path, tree_path, metadata_path)
    return mvp_tree
def sep_mvp_tree(mvp_tree,cp):
    tree = copy.copy(mvp_tree.feature_tree)
    sub_trees = cut_tree(tree,cp)
    print(len(sub_trees))
    return sub_trees

def get_node_score(node,coef=[1,1,1]):
    score = coef[0]*np.mean(node.sample_series)+\
        coef[1]*node.GI+coef[2]*np.std(node.sample_series)
    return score     

def search_sub_tree(sub_tree,coef,list1 = []):
    #print('search_sub_tree')
    p_score  = get_node_score(sub_tree,coef)
    child_score = 0
    for ele in sub_tree.clades:
        child_score += get_node_score(ele,coef)
    child_score = child_score/2
    if p_score <= child_score: 
        for ele in sub_tree.clades:
            search_sub_tree(ele,coef,list1)
    else:
        list1.append(sub_tree)
    print(len(list1))
    return list1



    

def generate_new_OTU_table(sub_trees,coef):
    """get a OTU table from the root node of the subtrees.
    Args:
        list1: obtained from the search_sub_tree function.
        coef: used for compute the score function,e.g.[1,1,1]
    """
    series = []
    for sub_tree in sub_trees:
        list1 = search_sub_tree(sub_tree,coef,list1=[])
        for ele in list1:
            series.append(ele.sample_series)
    df = pd.DataFrame(series)
    print(df.shape)
    return df
        

def Machine_learning():
    pass
if __name__ == "__main__":
    mvp_tree = get_mvp_tree('upload_files/feature-table.biom',\
        'upload_files/tree.nwk','upload_files/demo_metadata.tsv')
    sub_trees = sep_mvp_tree(mvp_tree,cp=0.2)
    df = generate_new_OTU_table(sub_trees,coef).T
    metadata = pd.read_csv('upload_files/demo_metadata.tsv', sep= '\t')
    obj_col = 'BodySite'