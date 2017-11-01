#!/usr/bin/env python3
import os
import sys
import git
import subprocess
import csv
import inspect
from ground import GroundClient
from graphviz import Digraph
from shutil import copyfile

import networkx as nx


def __run_proc__(bashCommand):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return str(output, 'UTF-8')


def func(f):
    def name_func():
        return inspect.getsourcefile(f).split('/')[-1]

    def wrapped_func(in_artifacts, out_artifacts):
        f(in_artifacts, out_artifacts)
        return inspect.getsourcefile(f).split('/')[-1]
    return [name_func, wrapped_func]


def ground_client(backend):
    global __gc__
    __gc__ = GroundClient(backend)


class Artifact:

    # loc: location
    # parent: each artifact is produced by 1 action
    def __init__(self, loc, parent):
        assert 'hyperedge:' != loc[0:10]
        self.loc = loc
        self.dir = "jarvis.d"
        self.parent = parent

        # Now we bind the artifact to its parent
        self.parent.out_artifacts.append(self)

    def pull(self):
        global __visited__
        __visited__ = []

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        driverfile = module.__file__.split('/')[-1]

        loclist = list(map(lambda x: x.getLocation(), self.parent.out_artifacts))
        self.parent.__run__(loclist)
        loclist = list(set(loclist))

        # get the script names
        scriptNames = [driverfile, ]
        self.parent.__scriptNameWalk__(scriptNames)
        scriptNames = list(set(scriptNames))

        # Now the artifact exists, do git
        # We resolve the directory name by loc
        dir_name = self.dir
        gc = __gc__

        gc.graph.__scriptNames__ = scriptNames

        # If the directory not exists, need to init repo
        if not os.path.exists(dir_name):

            # Create a node for every artifact (everything in jarvis.d)
            # Create a node version for every artifact (everything in jarvis.d)
            for loc in loclist:
                nodeid = gc.createNode(loc)
                nodeversionid = gc.createNodeVersion(nodeid)

            # Roughly, actions map to edges
            # Create an edge for every artifact for every action
            # Create an edge version for every artifact for every action

            for name, action in __actions__:
                hyperSourceKey = 'hyperedge:' + name
                hyperedgenodeid = gc.createNode(hyperSourceKey)
                hyperedgenodeversionid = gc.createNodeVersion(hyperedgenodeid)
                if action.in_artifacts:
                    for in_artifact in action.in_artifacts:
                        sourceKey = in_artifact.getLocation() + '_to_' + hyperSourceKey
                        fromNodeId = gc.getNode(in_artifact.getLocation()).nodeId
                        edgeid = gc.createEdge(sourceKey, fromNodeId, hyperedgenodeid)
                        nodeLatestVersions = gc.getNodeLatestVersions(in_artifact.getLocation())
                        assert len(nodeLatestVersions) == 1 # This will fail with k-lifting, but not until then
                        nodeLatestVersion = nodeLatestVersions[0]
                        gc.createEdgeVersion(edgeid, nodeLatestVersion.nodeVersionId, hyperedgenodeversionid)
                if action.out_artifacts:
                    for out_artifact in action.out_artifacts:
                        sourceKey = hyperSourceKey + '_to_' + out_artifact.getLocation()
                        toNodeId = gc.getNode(out_artifact.getLocation()).nodeId
                        edgeid = gc.createEdge(sourceKey, hyperedgenodeid, toNodeId)
                        nodeLatestVersions = gc.getNodeLatestVersions(out_artifact.getLocation())
                        assert len(nodeLatestVersions) == 1
                        nodeLatestVersion = nodeLatestVersions[0]
                        gc.createEdgeVersion(edgeid, hyperedgenodeversionid, nodeLatestVersion.nodeVersionId)

            gc.commit(dir_name)


        #     os.makedirs(dir_name)
        #     # Move new files to the artifacts repo
        #     for loc in loclist:
        #         os.rename(loc, dir_name + "/" + loc)
        #     for script in scriptNames:
        #         copyfile(script, dir_name + "/" + script)
        #     os.chdir(dir_name)
        #     repo = git.Repo.init(os.getcwd())
        #     repo.index.add(loclist + scriptNames)
        #     repo.index.commit("initial commit")
        #     tree = repo.tree()
        #     with open('.jarvis', 'w') as f:
        #         for obj in tree:
        #             commithash = __run_proc__("git log " + obj.path).replace('\n', ' ').split()[1]
        #             if obj.path != '.jarvis':
        #                 f.write(obj.path + " " + commithash + "\n")
        #     repo.index.add(['.jarvis'])
        #     repo.index.commit('.jarvis commit')
        #     os.chdir('../')
        # else:
        #     for loc in loclist:
        #         os.rename(loc, dir_name + "/" + loc)
        #     for script in scriptNames:
        #         copyfile(script, dir_name + "/" + script)
        #     os.chdir(dir_name)
        #     repo = git.Repo(os.getcwd())
        #     repo.index.add(loclist + scriptNames)
        #     repo.index.commit("incremental commit")
        #     tree = repo.tree()
        #     with open('.jarvis', 'w') as f:
        #         for obj in tree:
        #             commithash = __run_proc__("git log " + obj.path).replace('\n', ' ').split()[1]
        #             if obj.path != '.jarvis':
        #                 f.write(obj.path + " " + commithash + "\n")
        #     repo.index.add(['.jarvis'])
        #     repo.index.commit('.jarvis commit')
        #     os.chdir('../')
            
    def plot(self, rankdir=None):
        # WARNING: can't plot before pulling.
        # Prep globals, passed through arguments
        global __nodes__
        __nodes__ = {}

        dot = Digraph()
        diagram = {"dot": dot, "counter": 0, "sha": {}}

        with open('jarvis.d/.jarvis') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for row in reader:
                ob, sha = row
                diagram["sha"][ob] = sha

        self.parent.__plotWalk__(diagram)
        
        dot.format = 'png'
        if rankdir == 'LR':
            dot.attr(rankdir='LR')
        dot.render('driver.gv', view=True)
        
    def to_graph(self, rankdir=None):
        # WARNING: can't plot before pulling.
        # Prep globals, passed through arguments
        global __nodes__
        __nodes__ = {}


        diagram = {
            "g": nx.Graph(),
            "counter": 0, 
            "sha": {}
            }

        with open('jarvis.d/.jarvis') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for row in reader:
                ob, sha = row
                diagram["sha"][ob] = sha

        self.parent.__graphWalk__(diagram)
        
        return diagram['g']
        

    def getLocation(self):
        return self.loc

    def hasChanged(self):
        pass

    """
    We will want to check the loc prefix to decide where to look
    for existence e.g. http, s3, sftp, etc.
    No pre-defined prefix, assume local filesystem.
    """
    def exists(self):
        if not os.path.isfile(self.loc):
            print(self.loc + " not found.")
            sys.exit(1)

    """
    We assume an open-ended Integrity predicate on each artifact. 
    The design of this predicate language is TBD
    """
    def isLegal(self):
        pass

    def stat(self):
        pass


class Action:

    def __init__(self, func, in_artifacts=None):
        self.name = func[0]()
        self.func = func[1]
        self.out_artifacts = []
        self.in_artifacts = in_artifacts

        name_repeats = len([name for name in __action_names__ if name == self.name])
        __action_names__.append(self.name)
        edge_name = self.name
        if name_repeats:
            edge_name += '_' + str(name_repeats)
        __actions__.append((edge_name, self))


    def __run__(self, loclist):
        outNames = ''
        for out_artifact in self.out_artifacts:
            outNames += out_artifact.getLocation()
        if self.name+outNames in __visited__:
            return
        if self.in_artifacts:
            for artifact in self.in_artifacts:
                loclist.append(artifact.loc)
                artifact.parent.__run__(loclist)
        self.script = self.func(self.in_artifacts, self.out_artifacts)
        __visited__.append(self.script+outNames)


    def produce(self, loc):
        return Artifact(loc, self)

    def __scriptNameWalk__(self, scriptNames):
        scriptNames.append(self.script)
        if self.in_artifacts:
            for artifact in self.in_artifacts:
                artifact.parent.__scriptNameWalk__(scriptNames)
                
    def __plotWalk__(self, diagram):
        dot = diagram["dot"]
        
        # Create nodes for the children
        
        to_list = []
        
        # Prepare the children nodes
        for child in self.out_artifacts:
            node_diagram_id = str(diagram["counter"])
            dot.node(node_diagram_id, child.loc + "\n" + diagram["sha"][child.loc][0:6] + "...", shape="box")
            __nodes__[child.loc] = node_diagram_id
            to_list.append((node_diagram_id, child.loc))
            diagram["counter"] += 1
        
        # Prepare this node
        node_diagram_id = str(diagram["counter"])
        dot.node(node_diagram_id, self.script.split('.')[0], shape="ellipse")
        __nodes__[self.script] = node_diagram_id
        diagram["counter"] += 1
        
        # Add the script artifact
        node_diagram_id_script = str(diagram["counter"])
        dot.node(node_diagram_id_script, self.script + "\n" + diagram["sha"][self.script][0:6] + "...", shape="box")
        diagram["counter"] += 1
        dot.edge(node_diagram_id_script, node_diagram_id)

        for to_node, loc in to_list:
            dot.edge(node_diagram_id, to_node)
        
        if self.in_artifacts:
            for artifact in self.in_artifacts:
                if artifact.getLocation() in __nodes__:
                    dot.edge(__nodes__[artifact.getLocation()], node_diagram_id)
                else:
                    from_nodes = artifact.parent.__plotWalk__(diagram)
                    for from_node, loc in from_nodes:
                        if loc in [art.getLocation() for art in self.in_artifacts]:
                            dot.edge(from_node, node_diagram_id)
        
        return to_list


    def __graphWalk__(self, diagram):
        g = diagram['g']
        # Create nodes for the children
        
        to_list = []
        
        # Prepare the children nodes
        for child in self.out_artifacts:
            node_diagram_id = str(diagram["counter"])
            g.add_node(node_diagram_id, 
                {
                    "text": child.loc + "\n" + diagram["sha"][child.loc][0:6] + "...",
                    "shape": "box"
                })
            __nodes__[child.loc] = node_diagram_id
            to_list.append((node_diagram_id, child.loc))
            diagram["counter"] += 1
        
        # Prepare this node
        node_diagram_id = str(diagram["counter"])
        g.add_node(node_diagram_id, 
            {
                    "text": self.script.split('.')[0],
                    "shape": "ellipse"
            }
        )
        __nodes__[self.script] = node_diagram_id
        diagram["counter"] += 1
        
        # Add the script artifact
        node_diagram_id_script = str(diagram["counter"])
        g.add_node(node_diagram_id_script, 
            {
                    "text": self.script + "\n" + diagram["sha"][self.script][0:6] + "...",
                    "shape": "box"
            }
        )
        diagram["counter"] += 1
        g.add_edge(node_diagram_id_script, node_diagram_id)

        for to_node, loc in to_list:
            g.add_edge(node_diagram_id, to_node)
        
        if self.in_artifacts:
            for artifact in self.in_artifacts:
                if artifact.getLocation() in __nodes__:
                    dot.add_edge(__nodes__[artifact.getLocation()], node_diagram_id)
                else:
                    from_nodes = artifact.parent.__graphWalk__(diagram)
                    for from_node, loc in from_nodes:
                        if loc in [art.getLocation() for art in self.in_artifacts]:
                            g.add_edge(from_node, node_diagram_id)
        
        return to_list

__visited__ = []
__nodes__ = {}
__actions__ = []
__action_names__ = []
__gc__ = None
