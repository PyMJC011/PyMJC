from __future__ import annotations
from inspect import getabsfile
from tkinter.messagebox import NO
from typing import *
from abc import abstractmethod
import sys
from typing import Set
from pymjc.back import assem, flowgraph, graph
from pymjc.front import frame, temp


class RegAlloc (temp.TempMap):
    def __init__(self, frame: frame.Frame, instr_list: assem.InstrList):
        self.frame: frame.Frame = frame
        self.instrs: assem.InstrList = instr_list
        self.preColoredNodes : List[graph.Node] 
        self.normalColoredNodes : List[graph.Node]
        self. initialNodes = List[graph.Node]
        self.spillNodes = List[graph.Node]
        self.coalesceNodes = List[graph.Node]
        self.nodeStack = List[graph.Node]
        self.simplifyWorklist = List[graph.Node]
        self.freezeWorklist = List[graph.Node]
        self.spillWorklist = List[graph.Node]
        self.coalesceMoveNodes = List[graph.Node]
        self.constrainMoveNodes = List[graph.Node]
        self.freezeMoveNodes = List[graph.Node]
        self.worklistMoveNodes = List[graph.Node]
        self.activeMoveNodes = List[graph.Node]
        self.spillCost = Dict[graph.Node, int]
        self.adjacenceSets = List[Edge]
        self.adjacenceList = Dict[graph.Node, List[graph.Node]]
        self.nodeDegreeTable = Dict[graph.Node, int]
        self.nodeAliasTable = Dict[graph.Node, graph.Node]
        self.nodeColorTable = Dict[graph.Node, graph.Node]
        self.generatedSpillTemps = List[temp.Temp]
        #TODO

    def LivenessAnalisys(self) -> None:
        self.assemFlowGraph = flowgraph.AssemFlowGraph(self.instrs)
        self.livenessOutput = Liveness(self.assemFlowGraph)

    def Init(self) -> None:
        self.preColoredNodes.clear();
        self.normalColoredNodes.clear();

        self.initialNodes.clear();
        self.spillNodes.clear();
        self.coalesceNodes.clear();

        self.nodeStack.clear();

        self.simplifyWorklist.clear();
        self.freezeWorklist.clear();
        self.spillWorklist.clear();

        self.coalesceMoveNodes.clear();
        self.constrainMoveNodes.clear();
        self.freezeMoveNodes.clear();
        self.activeMoveNodes.clear();

        self.spillCost.clear();

        self.adjacenceSets.clear();
        self.adjacenceList.clear();

        self.moveNodesList.clear();

        self.nodeAliasTable.clear();
        self.nodeColorTable.clear();
        self.nodeDegreeTable.clear();

        for counter in range(0, len(self.frame.registers())):
            temp : temp.Temp = self.frame.registers()[counter]
            node : graph.Node = self.livenessOutput.tnode(temp)

            self.preColoredNodes.append(node)
            self.spillCost[node] = "inf"

            self.nodeColorTable[node] = node
            self.nodeDegreeTable[node] = 0
        nodes : graph.NodeList = self.livenessOutput.nodes()
        next = nodes.head
        while next!=None:
            if next not in self.preColoredNodes:
                self.initialNodes.append(next)

                if self.livenessOutput.gtemp(next) in self.generatedSpillTemps:
                    self.spillCost[next] = "inf"
                elif next not in self.preColoredNodes:
                    self.spillCost[next] = 1
            self.nodeDegreeTable[next] = 0
            next = nodes.tail.head
    
    def Build(self) -> None:
        nodeList : graph.NodeList = self.assemFlowGraph.nodes()
        node = nodeList.head
        while node!=None:
            live : List[temp.Temp] = self.livenessOutput.out_node_table[node][:]
            isMoveInstruction : bool = self.assemFlowGraph.isMove(node)

            if isMoveInstruction:
                useslst : temp.TempList = self.assemFlowGraph.use(node).head
                uses = useslst.head
                while uses!=None:
                    live.remove(uses)
                    uses = useslst.tail.head
                useslst : temp.TempList = self.assemFlowGraph.use(node).head
                uses = useslst.head
                while uses!=None:
                    self.moveNodesList(self.livenessOutput.tnode(uses)).add(node);
                    uses = useslst.tail.head

                defslst : temp.TempList = self.assemFlowGraph.deff(node).head
                defs =defslst.head
                while defs!=None:
                    self.moveNodesList(self.livenessOutput.tnode(defs)).add(node);
                    defs = defslst.tail.head
                self.worklistMoveNodes.append(node)

            defslst : temp.TempList = self.assemFlowGraph.deff(node).head
            defs =defslst.head
            while defs!=None:
                live.append(defs)
                defs = defslst.tail.head
            
            defslst : temp.TempList = self.assemFlowGraph.deff(node).head
            defs =defslst.head
            while defs!=None:
                for liveTemp in live:
                    AddEdge(liveTemp,defs)
                defs = defslst.tail.head

    def MakeWorkList(self) -> None:
        K : int = len(self.preColoredNodes)
        for n in self.initialNodes:
            self.initialNodes.remove(n)
            if self.nodeDegreeTable(n) >=K:
                self.spillWorklist.append(n)
            elif MoveRelated(n):
                self.freezeWorklist.append(n)
            else:
                self.simplifyWorklist.append(n)

    def temp_map(self, temp: temp.Temp) -> str:
        #TODO
        return temp.to_string()
    
    def Simplify(self) -> None:
        n : graph.Node = self.simplifyWorklist[0]
        self.simplifyWorklist.remove(n)
        self.nodeStack.append(n)
        for m in Adjacent(n):
            DecrementDegree(m)

    def Coalesce(self) -> None:
        m : graph.Node = None
        if(self.worklistMoveNodes[0]!=None):
            m = self.worklistMoveNodes[0]
            self.worklistMoveNodes.remove(m)
        
        x : graph.Node = GetAlias(self.livenessOutput.tnode(self.assemFlowGraph.instr(m).deff().head))
        y : graph.Node = GetAlias(self.livenessOutput.tnode(self.assemFlowGraph.instr(m).use().head))

        u : graph.Node
        v : graph.Node

        if y in self.preColoredNodes:
            u=y
            v=x
        else:
            u=x
            v=y
        
        e : Edge=Edge.get_edge(u,v)
        self.worklistMoveNodes.remove(m)

        if u==v:
            self.coalesceMoveNodes.append(m)
            AddWorklist(u)
        elif v in self.preColoredNodes or e in self.adjacenceSets:
            self.constrainMoveNodes.appennd(m)
            AddWorklist(u)
            AddWorklist(v)

        elif CoalesceAuxiliarFirstChecking(u, v) or CoalesceAuxiliarSecondChecking(u, v):
            self.coalesceMoveNodes.append(m)
            Combine(u,v)
            AddWorklist(u)
        else:
            self.activeMoveNodes.append(m)
    
    def CoalesceAuxiliarFirstChecking(self,u : graph.Node, v : graph.Node) -> bool:
        if u not in self.preColoredNodes:
            return False
        for t in Adjacent(v):
            if not self.OK(t,u):
                return False
        return True

    def OK(self, t : graph.Node, r : graph.Node) -> bool:
        K : int = len(self.preColoredNodes)
        result : bool = t in self.preColoredNodes or nodeDegreeTable(t) < K or Edge.get_edge(t, r) in self.adjacenceSets
        return result
    
    def CoalesceAuxiliarSecondChecking(self, u : graph.Node, v : graph.Node) -> bool:
        if(u in self.preColoredNodes):
            return False
        adjacent : List[graph.Node] = Adjacent(u)
        for adj in Adjacent(v):
            adjacent.append(adj)
        return Conservative(adjacent)

    def Freeze(self) -> None:
        u : graph.Node = self.freezeWorklist[0]
        self.freezeWorklist.remove(u)
        self.simplifyWorklist.append(u)
        self.FreezeMoves(u)

    def FreezeMoves(self, u : graph.Node) -> None:
        K : int = len(self.preColoredNodes)
        for m in NodeMoves(u):
            x : graph.Node = self.livenessOutput.tnode(self.assemFlowGraph.deff(m).head)
            y : graph.Node = self.livenessOutput.tnode(self.assemFlowGraph.use(m).head)

            v : graph.Node

            if GetAlias(u) == GetAlias(y):
                v = GetAlias(x)
            
            else:
                v = GetAlias(y)
            
            self.activeMoveNodes.remove(m)
            self.freezeMoveNodes.append(m)

            if len(NodeMoves(v)) == 0 and nodeDegreeTable(v) < K:
                self.freezeWorklist.remove(v)
                self.simplifyWorklist.append(v)

    def SelectSpill(self) -> None:
        m : graph.Node = self.spillWorklist[0]
        v : int = self.spillCost[m]

        for a in self.spillWorklist:
            if self.spillCost[a] < v:
                m = a

        self.spillWorklist.remove(m)
        self.simplifyWorklist.append(m)
        FreezeMoves(m)

    
class Color(temp.TempMap):
    def __init__(self, ig: InterferenceGraph, initial: temp.TempMap, registers: temp.TempList):
        #TODO
        pass
    
    def spills(self) -> temp.TempList:
        #TODO
        return None

    def temp_map(self, temp: temp.Temp) -> str:
        #TODO
        return temp.to_string()

class InterferenceGraph(graph.Graph):
    
    @abstractmethod
    def tnode(self, temp:temp.Temp) -> graph.Node:
        pass

    @abstractmethod
    def gtemp(self, node: graph.Node) -> temp.Temp:
        pass

    @abstractmethod
    def moves(self) -> MoveList:
        pass
    
    def spill_cost(self, node: graph.Node) -> int:
      return 1


class Liveness (InterferenceGraph):

    def __init__(self, flow: flowgraph.FlowGraph):
        self.live_map = {}
        
        #Flow Graph
        self.flowgraph: flowgraph.FlowGraph = flow
        
        #IN, OUT, GEN, and KILL map tables
        #The table maps complies with: <Node, Set[Temp]>
        self.in_node_table = {}
        self.out_node_table = {}
        self.gen_node_table = {}
        self.kill_node_table = {}

        #Util map tables
        #<Node, Temp>
        self.rev_node_table = {}
        #<Temp, Node>
        self.map_node_table = {}
        
        #Move list
        self.move_list: MoveList = None

        self.build_gen_and_kill()
        self.build_in_and_out()
        self.build_interference_graph()
    
    def add_ndge(self, source_node: graph.Node, destiny_node: graph.Node):
        if (source_node is not destiny_node and not destiny_node.comes_from(source_node) and not source_node.comes_from(destiny_node)):
            super.add_edge(source_node, destiny_node)

    def show(self, out_path: str) -> None:
        if out_path is not None:
            sys.stdout = open(out_path, 'w')   
        node_list: graph.NodeList = self.nodes()
        while(node_list is not None):
            temp: temp.Temp = self.rev_node_table.get(node_list.head)
            print(temp + ": [ ")
            adjs: graph.NodeList = node_list.head.adj()
            while(adjs is not None):
                print(self.rev_node_table.get(adjs.head) + " ")
                adjs = adjs.tail

            print("]")
            node_list = node_list.tail
    
    def get_node(self, temp: temp.Temp) -> graph.Node:
      requested_node: graph.Node = self.map_node_table.get(temp)
      if (requested_node is None):
          requested_node = self.new_node()
          self.map_node_table[temp] = requested_node
          self.rev_node_table[requested_node] = temp

      return requested_node

    def node_handler(self, node: graph.Node):
        def_temp_list: temp.TempList = self.flowgraph.deff(node)
        while(def_temp_list is not None):
            got_node: graph.Node  = self.get_node(def_temp_list.head)

            for live_out in self.out_node_table.get(node):
                current_live_out = self.get_node(live_out)
                self.add_edge(got_node, current_live_out)

            def_temp_list = def_temp_list.tail

  
    def move_handler(self, node: graph.Node):
        source_node: graph.Node  = self.get_node(self.flowgraph.use(node).head)
        destiny_node: graph.Node = self.get_node(self.flowgraph.deff(node).head)

        self.move_list = MoveList(source_node, destiny_node, self.move_list)
    
        for temp in self.out_node_table.get(node):
            got_node: graph.Node = self.get_node(temp)
            if (got_node is not source_node ):
                self.addEdge(destiny_node, got_node)


    def out(self, node: graph.Node) -> Set[temp.Temp]:
        temp_set = self.out_node_table.get(node)
        return temp_set


    def tnode(self, temp:temp.Temp) -> graph.Node:
        node: graph.Node = self.map_node_table.get(temp)
        if (node is None ):
            node = self.new_node()
            self.map_node_table[temp] = node
            self.rev_node_table[node] = temp
        
        return node

    def gtemp(self, node: graph.Node) -> temp.Temp:
        temp: temp.Temp = self.rev_node_table.get(node)
        return temp

    def moves(self) -> MoveList:
        return self.move_list

    def build_gen_and_kill(self):
        #TODO
        pass

    def build_in_and_out(self):
        #TODO
        pass

    def build_interference_graph(self):
        #TODO
        pass

class Edge():

    edges_table = {}

    def __init__(self):
        super.__init__()
    
    def get_edge(self, origin_node: graph.Node, destiny_node: graph.Node) -> Edge:
        
        origin_table = Edge.edges_table.get(origin_node)
        destiny_table = Edge.edges_table.get(destiny_node)
        
        if (origin_table is None):
            origin_table = {}
            Edge.edges_table[origin_node] = origin_table

        if (destiny_table is None):
            destiny_table = {}
            Edge.edges_table[destiny_node] = destiny_table
        
        requested_edge: Edge  = origin_table.get(destiny_node)

        if(requested_edge is None):
            requested_edge = Edge()
            origin_table[destiny_node] = requested_edge
            destiny_table[origin_node] = requested_edge

        return requested_edge



class MoveList():

   def __init__(self, s: graph.Node, d: graph.Node, t: MoveList):
      self.src: graph.Node = s
      self.dst: graph.Node = d
      self.tail: MoveList = t
