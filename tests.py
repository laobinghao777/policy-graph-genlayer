import sys,types,json,unittest,importlib.util
from pathlib import Path
class E(Exception):pass
class Contract:
    def __new__(cls):
        x=super().__new__(cls);x.collections={};x.cases={};return x
sender=types.SimpleNamespace(as_hex='owner');answer={}
gl=types.ModuleType('genlayer');gl.contract=types.SimpleNamespace(Contract=Contract);gl.storage=types.SimpleNamespace(TreeMap=dict)
gl.message=types.SimpleNamespace(sender_address=sender);gl.vm=types.SimpleNamespace(UserError=E)
gl.public=types.SimpleNamespace(write=lambda f:f,view=lambda f:f)
gl.nondet=types.SimpleNamespace(exec_prompt=lambda *a,**k:answer)
gl.eq_principle=types.SimpleNamespace(prompt_comparative=lambda f,p:f())
gt=types.ModuleType('genlayer.types');gt.u256=int
sys.modules['genlayer']=gl;sys.modules['genlayer.types']=gt
def load(name,cls):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).parent/'contract.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return getattr(m,cls)
Graph=load('policy-graph','PolicyGraph')
class Tests(unittest.TestCase):
    def setUp(self):sender.as_hex='owner'
    def graph(self):
        c=Graph();c.create_case('Both rules apply to all public support tickets without exceptions.',json.dumps(['Publish every ticket immediately after creation.','Never publish any ticket before review is complete.']));return c
    def test_conflict_graph_and_finality(self):
        global answer;answer={'pairs':[{'relation':'conflict','reason':'Immediate publication precedes completed review.','witness':'A newly created ticket has not been reviewed; publishing it immediately violates rule two.'}]};c=self.graph();c.analyze('1');r=json.loads(c.get_case('1'));self.assertEqual(r['analysis']['conflict_edges'],[[1,2]]);self.assertEqual(r['analysis']['conflict_degree'],[1,1])
        with self.assertRaises(E):c.analyze('1')
    def test_no_witness_rejected(self):
        global answer;answer={'pairs':[{'relation':'conflict','reason':'Some reason','witness':''}]};c=self.graph()
        with self.assertRaises(E):c.analyze('1')
    def test_unknown_not_consistent(self):
        global answer;answer={'pairs':[{'relation':'unknown','reason':'Scope unclear','witness':''}]};c=self.graph();c.analyze('1');self.assertEqual(json.loads(c.get_case('1'))['analysis']['summary'],'unresolved_pairs')
    def test_duplicate_rules_rejected(self):
        c=Graph()
        with self.assertRaises(E):c.create_case('Scope covering all tickets and all users.',json.dumps(['Always publish all tickets.']*2))
if __name__=='__main__':unittest.main()
