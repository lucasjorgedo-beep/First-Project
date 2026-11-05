"""TaskFlow: gerenciador simples de tarefas com armazenamento JSON."""
import argparse, json
from datetime import datetime
from pathlib import Path
DEFAULT_FILE = Path(__file__).with_name("tasks.json")
def load_tasks(path=DEFAULT_FILE):
    if not path.exists(): return []
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc: raise ValueError("Arquivo de tarefas inválido.") from exc
    if not isinstance(data,list): raise ValueError("O arquivo precisa conter uma lista de tarefas.")
    return data
def save_tasks(tasks,path=DEFAULT_FILE):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(tasks,ensure_ascii=False,indent=2),encoding="utf-8")
def add_task(title,path=DEFAULT_FILE):
    title=title.strip()
    if not title: raise ValueError("O título não pode ficar vazio.")
    tasks=load_tasks(path); next_id=max((t.get("id",0) for t in tasks),default=0)+1
    task={"id":next_id,"title":title,"done":False,"created_at":datetime.now().isoformat(timespec="seconds")}
    tasks.append(task); save_tasks(tasks,path); return task
def complete_task(task_id,path=DEFAULT_FILE):
    tasks=load_tasks(path)
    for task in tasks:
        if task.get("id")==task_id:
            task["done"]=True; save_tasks(tasks,path); return task
    raise ValueError(f"Tarefa {task_id} não encontrada.")
def delete_task(task_id,path=DEFAULT_FILE):
    tasks=load_tasks(path); remaining=[t for t in tasks if t.get("id")!=task_id]
    if len(remaining)==len(tasks): raise ValueError(f"Tarefa {task_id} não encontrada.")
    save_tasks(remaining,path)
def main():
    parser=argparse.ArgumentParser(description="Gerenciador de tarefas TaskFlow")
    parser.add_argument("--file",type=Path,default=DEFAULT_FILE); sub=parser.add_subparsers(dest="command",required=True)
    add=sub.add_parser("add"); add.add_argument("title")
    sub.add_parser("list")
    done=sub.add_parser("done"); done.add_argument("id",type=int)
    rem=sub.add_parser("delete"); rem.add_argument("id",type=int)
    args=parser.parse_args()
    try:
        if args.command=="add":
            task=add_task(args.title,args.file); print(f"Tarefa #{task['id']} adicionada.")
        elif args.command=="list":
            tasks=load_tasks(args.file)
            if not tasks: print("Nenhuma tarefa cadastrada.")
            for t in tasks: print(f"[{'x' if t['done'] else ' '}] #{t['id']} - {t['title']}")
        elif args.command=="done": complete_task(args.id,args.file); print(f"Tarefa #{args.id} concluída.")
        elif args.command=="delete": delete_task(args.id,args.file); print(f"Tarefa #{args.id} excluída.")
    except ValueError as error: parser.error(str(error))
if __name__=="__main__": main()
