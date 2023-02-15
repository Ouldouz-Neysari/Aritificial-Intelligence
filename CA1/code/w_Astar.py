import copy
import time
import heapq

class Node:
  def __init__(self,nodename):
    self.name=nodename
    self.adjs=[]
    self.rcps=[]
    self.needed_time=0
    self.diff=False
  def add_adj(self,N):
    self.adjs.append(N)
  def add_rcp(self,rcpnode):
    self.rcps.append(rcpnode)

class Graph:
  def __init__(self):
    self.nodes=[]
    self.diff_nodes=[]
    self.morids=[]
    self.morid_rcp={}
    self.rcps=[]
  def add_node(self,N):
    self.nodes.append(N)
  def add_diff_node(self,N):
    self.diff_nodes.append(N)
  def add_morid(self,N):
    self.morids.append(N.name)
    self.morid_rcp.update({N.name:[]})
  def add_rcp(self,N,M):
    self.rcps.append(N.name)
    self.morid_rcp[M.name].append(N.name)

class State():
  def __init__(self,start_node,_path,node_time,rcp_dict,morid_dict,_cost,ps_num,heuristic):
    self.position=start_node
    self.path=_path
    self.needed_time=node_time
    self.visited_recp=rcp_dict
    self.visited_morid=morid_dict
    self.cost=_cost
    self.pass_number=ps_num
    self.h=heuristic
  def __lt__(self, other):
    return self.cost < other.cost
  

def create_ns_path(cur_state):
  ns_path=[]
  for S in cur_state.path:
    ns_path.append(S)
  return ns_path




def apply_state_changes(cur_state,G):
  cur_node=cur_state.position
  if (cur_state.needed_time==0):
    if(cur_node.name in G.rcps):
        cur_state.visited_recp[cur_node.name]=True 
    if(cur_node.name in G.morids):
        visit_count=0
        for the_rcp in G.morid_rcp[cur_node.name]:
            if(cur_state.visited_recp[the_rcp]==True):
                visit_count+=1

        if (len(G.morid_rcp[cur_node.name])==visit_count):
            cur_state.visited_morid[cur_node.name]=True

def det_morid_visit(cur_state):
  counter=0
  for m in cur_state.visited_morid:
    if(cur_state.visited_morid[m]==True):
      counter+=1
  if(counter==len(cur_state.visited_morid.keys())):
    return True
  else:
    return False


def det_Function(S,alpha):
  left_morids=0
  left_rcps=0
  _cost=copy.deepcopy(S.cost)
  _h=copy.deepcopy(S.h)
  return _cost+(_h*alpha)

def Astar_add_children(cur_state,frontier,visited,G,alpha):
  cur_node=cur_state.position
  
  for nd in cur_node.adjs :

    if(cur_state.path==[] or cur_state.path==None):
      ns_path=[cur_state]

    
    else:

      ns_path=create_ns_path(cur_state)
      ns_path.append(cur_state)
      if(ns_path==None):
        pass
    ns_vis_rcp=copy.deepcopy(cur_state.visited_recp)
    ns_vis_mrd=copy.deepcopy(cur_state.visited_morid)
    ns_cost=copy.deepcopy(cur_state.cost)+1
    ns_h=copy.deepcopy(cur_state.h)
    if((nd in G.rcps) or (nd in G.morids )):
      ns_h-=1

    if(nd.diff==True):
        ps_num=0
        for pr_st in cur_state.path:
            if(pr_st.position.name==nd.name):
                ps_num+=1
        ns_pass=ps_num 
        _ns_time=copy.deepcopy(ns_pass)
    else:
      _ns_time=0
      ns_pass=0
    ns=State(nd,ns_path,_ns_time,ns_vis_rcp,ns_vis_mrd,ns_cost,ns_pass,ns_h)
    ns_F=det_Function(ns,alpha)
    current_visited=False
    for st in visited:
      if(st.position.name ==ns.position.name and st.visited_recp==ns.visited_recp and st.visited_morid==ns.visited_morid ):
        current_visited=True
    for st1 in frontier:
      if(st1[1].position.name ==ns.position.name and st1[1].visited_recp==ns.visited_recp and st1[1].visited_morid==ns.visited_morid ):
        current_visited=True
    if(current_visited==False):
      heapq.heappush(frontier,(ns_F,ns))

def w_A_star(S,G,alpha):
  visited = []

  explored=[]
  path_cost=0
  cur_heuristic=det_Function(S,alpha)
  frontier=[(cur_heuristic,S)]
  heapq.heapify(frontier)
  visited_states=0

  failure=0
  a=0
  current_state=None
  while True:
    visited_states+=1
    a+=1
    if(len(frontier)==0):
      failure=1
      break

    current_h,current_state= heapq.heappop(frontier)

    explored.append(current_state)



    cur_node=current_state.position


    visited.append(current_state)
    apply_state_changes(current_state,G)

    if(det_morid_visit(current_state)):

        break
    if(current_state.needed_time!=0):
        current_state.needed_time-=1
        current_state.cost+=1
        heapq.heappush(frontier,(det_Function(current_state,alpha),current_state))
    else:
        Astar_add_children(current_state,frontier,visited,G,alpha)


  return current_state.path,current_state,current_state.cost,visited_states

m,n=[int(x) for x in input().split()]

G=Graph()
for i in range(m):
  new_node=Node(i)
  G.add_node(new_node)

for j in range(n):
  u,v=[int(x) for x in input().split()]
  G.nodes[u-1].add_adj(G.nodes[v-1])
  G.nodes[v-1].add_adj(G.nodes[u-1])

h=int(input())
hard_nodes=[int(x) for x in input().split()]

for hrd in hard_nodes:
  G.nodes[hrd-1].diff=True
  G.add_diff_node(G.nodes[hrd-1])



s=int(input())

for k in range(s):
  tmp=[int(x) for x in input().split()]

  G.add_morid(G.nodes[tmp[0]-1])
  for l in tmp[2:]:

    G.add_rcp(G.nodes[l-1],G.nodes[tmp[0]-1])



v=int(input())


start_node=G.nodes[v-1]

passed_path=[]
nd_tm=0

rcps_dict={x:False for x in G.rcps}
morid_dict={x:False for x in G.morids}

init_h=len(morid_dict)+len(rcps_dict)


start_time = time.time()
Init_state=State(start_node,passed_path,nd_tm, rcps_dict,morid_dict,0,0,init_h)

alpha=1.8
Ex,final_state,total_cost,total_visited_states=w_A_star(Init_state,G,alpha)
cur_time_=time.time()

for e in Ex:
  print(e.position.name+1,end="->")
print(final_state.position.name+1)

print("cost",total_cost)
print("visited_states",total_visited_states)


print(cur_time_-start_time)