import importlib.util,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location('x',Path(__file__).parents[1]/'src/travel_packing_audit.py');x=importlib.util.module_from_spec(s);s.loader.exec_module(x)
class T(unittest.TestCase):
 def test_domain_workflow(self):
  r=x.run([{'category':'документы','item':'паспорт','packed':True},{'category':'одежда','item':'куртка','packed':False}],'2026-08-18',7); self.assertTrue(r=={'одежда':['куртка']})
if __name__=='__main__':unittest.main()
