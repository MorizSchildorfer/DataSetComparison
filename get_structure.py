#Python code to illustrate parsing of XML files 
# importing the required modules 
import csv 
from io import StringIO
import requests 
import xml.etree.ElementTree as ET 
from os import listdir
from os.path import isfile, isdir, join
import pandas
import igraph
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
from treelib import Node, Tree
import plotly.express as px

cogs_dir = "download"
default_entry = {"EU" : 0, "Germany" : 0, "ClinicalTrials" : 0, "Australia": 0}

def search_tree(root):
    dic = {}
    for child in root:
        if "}" in child.tag:
            child.tag = child.tag.split("}")[1]
        dic[child.tag] = search_tree(child)
        
    return dic

def collect_structure(struct, root):
    for child in root:
        if child.tag in struct:
            collect_structure(struct[child.tag], child)
        else:
            
           print(child.tag)
           struct[child.tag] = search_tree(child)
    return struct


def parseXML(tracker, origin, location): 
    print(origin, location)
    
    errors = 0
    counts = 0
    structure = {}
    for xmlfile in [f"{location}/{f}" for f in listdir(location) if isfile(join(location, f)) and f.split(".")[1]=="xml"]:
        
        # create element tree object 
        tree = ET.parse(xmlfile) 
        # it = ET.iterparse(StringIO(xmlfile))
        # root = it.root
        # get root element 
        root = tree.getroot() 
        for el in tree.iter():
            _, _, el.tag = el.tag.rpartition('}') 
        trial_name = "Non-existant"
        if origin == "Germany":
            trial_names = root.findall('./description/title/contents/localizedContent')
            for trial in trial_names:
                if trial.attrib["locale"] == "en":
                    trial_name = trial.text
                    break
                else:
                    trial_name = trial.text
            pass
        elif origin == "ClinicalTrials":
            trial_names = root.findall('./official_title')
            # print(trial_names.tag)
            if trial_names:
                trial_name = trial_names[0].text
                
            elif root.findall('./brief_title'):
                trial_names = root.findall('./official_title')
            else:
                
                print("error:", xmlfile)
                errors += 1
            pass
            
        elif origin == "Australia":
            trial_names = root.findall('./trial_identification/studytitle')
            # print(trial_names.tag)
            if trial_names:
                trial_name = trial_names[0].text
                
            elif root.findall('./trial_identification/scientifictitle'):
                trial_names = root.findall('./trial_identification/scientifictitle')
            else:
                
                print("error:", xmlfile)
                errors += 1
            pass
            
        trial_name = trial_name.strip().lower().replace(" ", "")
        # print("Name", trial_name)
        if trial_name not in tracker:
            tracker[trial_name] = default_entry.copy()
        # print(tracker[trial_name])
        tracker[trial_name][origin] += 1
        
        structure = collect_structure( structure, [root])
        counts += 1
        # if counts > 100:
            # print(errors)
            # break
        
    # return news items list 
    return structure 
    

def parseTXT2(): 
    file = open('trials-full.txt', mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    # print(lines)
    lines.pop(0)
    print(lines.pop(0))
    key_queue = ["A", "B", "C", "D", "E", "F", "G", "N", "P"]
    dic = {}
    current_dic = []
    depth = 0
    
    shit_list = []
    current_list = []
    new_parse = 0
    print(list([x.strip() for x in lines[0:10]]))
    while lines:
        line = lines.pop(0)
        # print("Line:", line)
        if line.strip() == "Summary":
            if current_list:
                shit_list.append(current_list)
            current_list = []
            key_queue = ["A", "B", "C", "D", "E", "F", "G", "N", "P"]
            new_parse = 1
            continue
        if new_parse == 1 and line.strip() == "":
            new_parse = 0
            continue
        elif line.strip() == "":
            continue
        line_split = line.split(":", 1)
        
        if new_parse == 1:
            dic[line_split[0]] = {}
        elif new_parse == 0:
            depth_split = line_split[0].split(" ", 1)
            if len(depth_split[0])<2:
                continue
            first_letter = depth_split[0][0]
            if not (first_letter.isupper() and first_letter.isalpha()):
                # print(first_letter)
                continue
            elif not first_letter >= key_queue[0]:
                continue
            elif first_letter == key_queue[0]:
                pass
                # depth_indicators = filter(lambda x: x != "", depth_split[0][2:].split("."))
                # while len(depth_indicators)<depth):
                    
                # while len(depth_indicators)<depth):
                    # current_dic.pop(0)
                    
                # for indicator in depth_indicators:
                # key = first_letter+"$"+depth_split[1]
                # if 
                # current_dic
            else:
                key = first_letter+"$"+depth_split[1]
                key_queue.insert(0, first_letter)
                if key not in dic:
                    dic[key] = {}
                current_dic.insert(0, dic[key])
                depth = 1
            
            print("depth", depth_split[0])
        else:
            continue
        
        current_list.append(line_split[0])
        print("line split", new_parse,line_split[0])
        # line_na
        
        
    print(sorted(shit_list[0]))
def parseTXT(tracker, origin = "EU", location = "eu"): 
    
    dic = {}
    # print(listdir(location))
    for xmlfile in [f"{location}/{f}/trials-full.txt" for f in listdir(location) if isdir(join(location, f))]:
        print(xmlfile)
        file = open(xmlfile, mode = 'r', encoding = 'utf-8-sig')
        lines = file.readlines()
        # print(lines)
        lines.pop(0)
        # print(lines.pop(0))
        key_queue = ["A", "B", "C", "D", "E", "F", "G", "N", "P"]
        depth = 0
        
        shit_list = []
        current_list = []
        new_parse = 0
        while lines:
            line = lines.pop(0)
            # print("Line:", line)
            if line.strip() == "Summary":
                if current_list:
                    shit_list.append(current_list)
                current_list = []
                key_queue = ["A", "B", "C", "D", "E", "F", "G", "N", "P"]
                new_parse = 1
                continue
            if new_parse == 1 and line.strip() == "":
                new_parse = 0
                continue
            elif line.strip() == "":
                continue
            line_split = line.split(":", 1)
            if new_parse == 1:
                if line_split[0] not in dic:
                    dic[line_split[0]] = {}
            elif new_parse == 0:
                if not key_queue:
                    continue
                depth_split = line_split[0].split(" ", 1)
                if  len(depth_split[0]) < 2 or len(line_split)<2:
                    continue
                first_letter = depth_split[0][0]
                
                # print("Info: ", first_letter, key_queue[0], line_split)
                if not (first_letter.isupper() and first_letter.isalpha()):
                    # print(first_letter)
                    continue
                elif not (first_letter in key_queue and first_letter >= key_queue[0] and len(depth_split[0].split("."))> 1):
                    
                    # print("Ex: ", first_letter in key_queue, first_letter >= key_queue[0], len(depth_split[0].split("."))>1)
                    continue
                elif first_letter > key_queue[0]:
                    key_queue.pop(0)
                    pass
                    
                depth_indicators = depth_split[0].split(".")
                if len(depth_indicators[0])> 1:
                    continue
                current_dic = dic
                if len(depth_split)> 1:
                   depth_indicators.append(depth_split[1])
                depth_indicators = list(filter(lambda x: x != "", depth_indicators))
                # print("Indicators: ", list(depth_indicators))
                # print(list(depth_indicators))
                for indicator in list(depth_indicators):
                    indicator = indicator.strip()
                    # print("arg", indicator, dic)
                    if indicator == "Full title of the trial":
                        # print("Line Title:", line_split[1])
                        title = line_split[1].strip().lower().replace(" ", "")
                        if title not in tracker:
                            tracker[title] = default_entry.copy()
                        tracker[title][origin] += 1
                    if indicator in current_dic:
                        current_dic = current_dic[indicator]
                    else:
                        current_dic[indicator] = {}
                        current_dic = current_dic[indicator]
            else:
                continue
        
        # current_list.append(line_split[0])
        # print("line split", new_parse,line_split[0])
        # line_na
    # print(dic)
    return dic
    # print(sorted(shit_list[0]))
    
    
def create_tree(dic, tree, g, names, parents):
    count = -1
    for k, v in dic.items():
        count+=1
        g.add_vertices(1, {"value": [k]})
        names.append(k)
        parents.append("")
        tree.create_node(k, count)
        count = create_tree_sub(v, tree, count, g, names, parents, k)
    return count+1

def create_tree_sub(dic, tree, parent, g, names, parents, p_name): 
    count = parent
    for k, v in dic.items():
        
        count+= 1
        g.add_vertices(1, {"value": [k]})
        
        # print(g)
        # print(k, count)
        # print((parent, count))
        g.add_edges([(parent, count)])
        names.append(k)
        parents.append(p_name)
        tree.create_node(k, count, parent= parent)
        count = create_tree_sub(v, tree, count, g, names, parents, k)
    return count
  
def main(): 
    name_tracker = {}
    # location = "eu"
    # counts = {"File" : parseTXT(name_tracker, "EU", location) }
    # create_graph(counts, "EU", 5000, 1000)
    # location = "unzips/german"
    # counts = parseXML(name_tracker, "Germany", location)
    # updateTrackerFile(name_tracker, "Germany")
    # create_graph(counts, "Germany", 2500, 1000)
    location = "TrialDetails_21_04_2021 3_52_15 AM"
    counts = {"File" : parseXML(name_tracker, "Australia", location)}
    create_box(counts, "Australia", 10000, 1000)
    # create_graph(counts, "Australia", 10000, 1000)
    # create_graph(counts, "Australia", 5000, 5000, "fr")
    # updateTrackerFile(name_tracker, "Australia")
    # location = "unzips/trials"
    # counts = parseXML(name_tracker, "ClinicalTrials", location)
    # create_graph(counts, "ClinicalTrials", 2500, 1000)
    
    # print(tracker_items)
    
def updateTrackerFile(name_tracker, source) :   
    print(source)
    tracker_dataset = pandas.read_csv('tracker.csv')
    for index, row in tracker_dataset.iterrows():
        if row["Name"] in name_tracker:
            print("Update", source, row["Name"])
            row[source] = name_tracker[row["Name"]][source]
        else:
           # print("Old", source, row["Name"])
           name_tracker[row["Name"]] ={source: 0}
            
        name_tracker[row["Name"]].update({key: value for key, value in row.items() if key != "Name"}) 
            
        
        
        #"EU" : row["EU"], "Germany": row["Germany"], "ClinicalTrials": row["ClinicalTrials"]
            
    
    tracker_items = [[key]+[count for source, count in sorted(item.items())] for key, item in name_tracker.items()]
    df = pandas.DataFrame(list(tracker_items), columns=["Name"]+sorted(default_entry.keys()))
    df.to_csv('tracker.csv', index=False)
    
    
def create_box(counts, filename, width, height, layout = "rt"):
    
    names = []
    parents = []
    G = Graph() # 2 stands for children number
    tree = Tree()
    count = create_tree(counts, tree, G, names, parents)
    print("names", names)
    print("parents", parents)
    # fig = go.Figure(go.Treemap(
        # labels = names,
        # parents = parents))
    fig = px.treemap(
    names = names, #["Eve","Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    parents = parents #["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
)
    fig.write_image(f"{filename}_tree.png")
    fig.write_html(f"{filename}_tree.html")
    
def create_graph(counts, filename, width, height, layout = "rt"):
    
    names = []
    G = Graph() # 2 stands for children number
    tree = Tree()
    count = create_tree(counts, tree, G, names)
    # tree.show()
    
    nr_vertices = count
    v_label = names #list(map(str, range(nr_vertices)))
    lay = G.layout(layout)

    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = EdgeSeq(G) # sequence of edges
    E = [e.tuple for e in G.es] # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2*M-position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe+=[position[edge[0]][0],position[edge[1]][0], None]
        Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

    labels = v_label
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                       y=Ye,
                       mode='lines',
                       name='key-key relation',
                       line=dict(color='rgb(210,210,210)', width=3),
                       hoverinfo='none'
                       ))
    fig.add_trace(go.Scatter(x=Xn,
                      y=Yn,
                      mode='markers',
                      name='key',
                      marker=dict(symbol='circle-dot',
                                    size=18,
                                    color='#6175c1',    #'#DB4551',
                                    line=dict(color='rgb(50,50,50)', width=1)
                                    ),
                      text=labels,
                      hoverinfo='text',
                      opacity=0.8
                      ))
                      
    fig.update_layout(
        title= f'{filename} Structure Graph',
        autosize=False,
        width=width,
        height=height,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        paper_bgcolor="LightSteelBlue",
        yaxis = dict(scaleanchor = "x", scaleratio = 1),
        plot_bgcolor='rgb(255,255,255)',
    )

    fig.write_image(f"{filename}_{layout}.png")
    fig.write_html(f"{filename}_{layout}.html")
      
if __name__ == "__main__": 
  
    # calling main function 
    main() 