"""CSV Insights: resumo exploratório de arquivos CSV usando a biblioteca padrão."""
import argparse,csv
from collections import Counter
from decimal import Decimal,InvalidOperation
from pathlib import Path
def analyze_csv(path):
 path=Path(path)
 if not path.exists(): raise FileNotFoundError(f"Arquivo não encontrado: {path}")
 with path.open("r",encoding="utf-8-sig",newline="") as file:
  reader=csv.DictReader(file)
  if not reader.fieldnames: raise ValueError("O CSV precisa ter uma linha de cabeçalho.")
  rows=list(reader); columns=reader.fieldnames
 report={"rows":len(rows),"columns":columns,"missing":{},"numeric":{},"categories":{}}
 for col in columns:
  values=[(row.get(col) or "").strip() for row in rows]; nonempty=[v for v in values if v]
  report["missing"][col]=len(values)-len(nonempty); parsed=[]; numeric=True
  for value in nonempty:
   normalized=value.replace(".","").replace(",",".") if "," in value else value
   try: parsed.append(Decimal(normalized))
   except InvalidOperation: numeric=False; break
  if nonempty and numeric:
   total=sum(parsed,Decimal("0"))
   report["numeric"][col]={"count":len(parsed),"sum":total,"min":min(parsed),"max":max(parsed),"average":total/len(parsed)}
  elif nonempty: report["categories"][col]=Counter(nonempty).most_common(5)
 return report
def print_report(report):
 print(f"Linhas: {report['rows']} | Colunas: {len(report['columns'])}")
 print("\nValores ausentes:")
 for name,count in report["missing"].items(): print(f"- {name}: {count}")
 print("\nColunas numéricas:")
 for name,s in report["numeric"].items(): print(f"- {name}: soma={s['sum']}, média={s['average']:.2f}, mínimo={s['min']}, máximo={s['max']}")
 print("\nCategorias mais frequentes:")
 for name,values in report["categories"].items(): print(f"- {name}: {values}")
def main():
 parser=argparse.ArgumentParser(description="Resumo exploratório de dados CSV")
 parser.add_argument("file",type=Path,help="Caminho do arquivo CSV"); args=parser.parse_args()
 try: print_report(analyze_csv(args.file))
 except (OSError,ValueError) as error: parser.error(str(error))
if __name__=="__main__": main()
