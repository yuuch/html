import biom
import pandas as pd 
from Bio import Phylo 
import plotly
import plotly.graph_objs as go
import copy
import numpy as np
class Annotation(object):
    def __init__(self, cols, feature_table_file, taxo_file):
        #self.tree = tree#Phylo.read(file = tree_file,format = tree_file_format)
        #obtain features(cols) from tree.get_terminals() which parallel to the tree.
        self.cols = cols
        self.feature_table = biom.load_table(feature_table_file).to_dataframe().to_dense()
        self.feature_table = self.feature_table.div(self.feature_table.sum(axis=0),axis=1)
        self.taxonomy = pd.read_csv(taxo_file,sep='\t')
        self.taxonomy.index = self.taxonomy['Feature ID']
        self.map_taxo(self.cols)
        self.generate_colors()

    def map_taxo(self,cols):
        #terminals = tree.get_terminals()
        #feature_names = [node.name for node in terminals]
        feature_names = cols
        feature_name_count_dict = {}
        for feature_name in feature_names:
            # feature_count: the number of seq in one feature(otu)
            #print(self.feature_table.loc[feature_name])
            feature_count = 0
            if len(self.feature_table.loc[feature_name])==0:
                continue
            else:
                feature_count = np.mean(list(self.feature_table.loc[feature_name]))
            unassigned = ['Unassigned',' p__unassigned',' c__unassigned',' o__unassigned',' f__unassigned'
                         ,' g__unassigned',' s__unassigned']
            if feature_count == 0:
                continue
            taxo_of_feature = self.taxonomy.loc[feature_name]['Taxon'].split(';')
            while len(taxo_of_feature)<len(unassigned):
                taxo_of_feature.append(unassigned[len(taxo_of_feature)])
            levels = {}
            for i in range(7):
                levels['level'+str(i)]={}
            for i in range(len(taxo_of_feature)):
                if taxo_of_feature[i] in levels['level'+str(i)]:
                    levels['level'+str(i)][taxo_of_feature[i]] += feature_count
                else:
                    levels['level'+str(i)][taxo_of_feature[i]] = feature_count
            
            #for i in range(len(levels)):
                #if levels['level'+str(i)] == {}:
                    #levels['level'+str(i)] = unassigned[i]
            #while len(levels) < len(unassigned):
                #levels['level'+str(len(levels))] = unassigned[len(levels)]    
            feature_name_count_dict[feature_name]=levels
        self.barplot_dict = feature_name_count_dict

    def generate_colors(self):
        colors = [
            'rgb(66,212,244)','rgb(230,25,75)','rgb(245,130,49)',
            'rgb(60,180,75)','rgb(67,99,216)','rgb(145,30,180)','rgb(240,50,230)',
            'rgb(31,119,180)','rgb(255,127,14)','rgb(44,160,44)','rgb(214,39,40)',
            'rgb(148,103,189)','rgb(140,86,75)','rgb(227,119,194)','rgb(127,127,127)',
            'rgb(188,189,34)','rgb(23,190,207)'
        ]
        self.colors = colors

    def plot_annotation(self):
        mapped_level={'level0':'Kingdom','level1':'Phylum','level2':'Class','level3':'Order',
                 'level4':'Family','level5':'Genus','level6':'Species','level7':'OTU'}
        data = []
        level_appeard_name = {}
        color_index = 0
        for i in range(7):
            level_appeard_name['level'+str(i)]={}
        np.random.seed(1)
        for otu in self.barplot_dict:
            otu_data = []
            phylum_colored = False # flag used to color level under phylum
            phylum_color_index = 0 # default phylumn color
            level_num = 0
            for level in self.barplot_dict[otu]:
                level_num += 1
                for ele in self.barplot_dict[otu][level]:
                    temp_index = 0
                    not_appeared = True
                    if ele in level_appeard_name[level]:
                        temp_index = level_appeard_name[level][ele]
                        not_appeared = False
                    else:
                        if phylum_colored:
                            temp_index = phylum_color_index
                        else:
                            temp_index = (int(level[-1])+len(level_appeard_name[level]))%len(self.colors)
                            level_appeard_name[level][ele]=temp_index
                    temp_color = self.colors[temp_index]
                    if phylum_colored:# modified(temp_color)
                        rgb_2_num = lambda color_rgb:[int(ele) for ele in color_rgb[4:-1].split(',')]
                        nums_2_rgb = lambda nums: 'rgb('+str(nums[0])+','+str(nums[1])+','+str(nums[2])+')'
                        index = np.random.randint(3)
                        nums = rgb_2_num(temp_color)
                        nums[index] += (255-nums[index])*(0.1*level_num)
                        temp_color = nums_2_rgb(nums)\

                    if ele =='Unassigned' or ele[4:]=='unassigned':
                        temp_color = 'rgb(0,0,0)'
                    filt_legend=['level1']
                    filt_result=False
                    #print(ele[0])
                    if level in filt_legend:
                        filt_result=True
                    trace=go.Bar(y=[mapped_level[level]],
                                     x = [self.barplot_dict[otu][level][ele]],
                                     orientation='h',
                                     name = ele,
                                     showlegend = filt_result,
                                     legendgroup = mapped_level[level],
                                     marker = dict(color=temp_color)
                        )
                    otu_data.append(trace)
                if level == 'level1':
                    phylum_colored = True
                    phylum_color_index = temp_index
            if len(data)>0:
                last_otu_data = copy.copy(data[-1])
                to_be_del=[]
                for i in range(7):
                    #print(min(len(otu_data),len(last_otu_data)))
                    #to_be_del = []
                    if i < min(len(otu_data),len(data[-1])):
                        if otu_data[i].name == data[-1][i].name:
                            to_be_del.append(i)
                            otu_data[i].x=tuple((data[-1][i].x[0]+otu_data[i].x[0],))
                            data[-1][i].x=tuple((0,))
            else:
                pass
            data.append(otu_data)
        #for i
        self.mapped_phylum_colors = level_appeard_name['level1']
        result_data = []
        for i in range(7):
            trace = go.Bar(y=[mapped_level['level'+str(6-i)]],
                           x=[0],
                           orientation='h',
                           name=mapped_level['level'+str(6-i)],
                           showlegend=False
                          )
            result_data.append(trace)
        #print(data[0])
        for i in range(7):
            for ele in data:
                if i<len(ele):
                    if ele[i].x[0]>0:
                        result_data.append(ele[i])
        #print(result_data)
        layout = go.Layout(
            #autosize =False,
            #height = 500,
            #width = 1000,
            barmode = 'stack',
            xaxis=dict(
                autorange=True,
                 showgrid=False,
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False
                ),
            hovermode='closest'
        )
        fig = go.Figure(data=result_data,layout=layout)
        div_str = plotly.offline.plot(fig,filename='stack_bar.html',output_type='div')
        return div_str