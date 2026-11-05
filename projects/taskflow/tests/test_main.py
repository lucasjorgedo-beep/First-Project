import tempfile,unittest
from pathlib import Path
from main import add_task,complete_task,delete_task,load_tasks
class TaskFlowTests(unittest.TestCase):
 def setUp(self): self.temp=tempfile.TemporaryDirectory(); self.path=Path(self.temp.name)/"tasks.json"
 def tearDown(self): self.temp.cleanup()
 def test_add_load(self):
  task=add_task("Estudar Python",self.path); self.assertEqual(task["id"],1); self.assertEqual(load_tasks(self.path)[0]["title"],"Estudar Python")
 def test_empty_title(self):
  with self.assertRaises(ValueError): add_task("  ",self.path)
 def test_complete(self):
  add_task("Revisar código",self.path); self.assertTrue(complete_task(1,self.path)["done"])
 def test_delete(self):
  add_task("Temporária",self.path); delete_task(1,self.path); self.assertEqual(load_tasks(self.path),[])
 def test_missing(self):
  with self.assertRaises(ValueError): complete_task(99,self.path)
if __name__=="__main__": unittest.main()
