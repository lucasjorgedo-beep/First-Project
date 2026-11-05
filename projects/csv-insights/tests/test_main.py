import tempfile,unittest
from pathlib import Path
from main import analyze_csv
class CSVInsightsTests(unittest.TestCase):
 def test_analysis(self):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/"sample.csv"; path.write_text("produto,valor,categoria\nCaneta,2,papelaria\nCaderno,10,papelaria\nLápis,,escrita\n",encoding="utf-8")
   report=analyze_csv(path); self.assertEqual(report["rows"],3); self.assertEqual(report["missing"]["valor"],1)
   self.assertEqual(report["numeric"]["valor"]["sum"],12); self.assertEqual(report["categories"]["categoria"][0][0],"papelaria")
 def test_missing_file(self):
  with self.assertRaises(FileNotFoundError): analyze_csv("arquivo-que-nao-existe.csv")
 def test_header_only(self):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/"empty.csv"; path.write_text("nome,idade\n",encoding="utf-8")
   report=analyze_csv(path); self.assertEqual(report["rows"],0); self.assertEqual(report["missing"]["nome"],0)
if __name__=="__main__": unittest.main()
