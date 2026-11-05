"""Funções de exemplo para praticar testes de qualidade de software."""
import re
def calculate_discount(price,percentage):
 if not isinstance(price,(int,float)) or isinstance(price,bool) or price<0: raise ValueError("Preço deve ser um número não negativo.")
 if not isinstance(percentage,(int,float)) or isinstance(percentage,bool): raise ValueError("Percentual deve ser numérico.")
 if not 0<=percentage<=100: raise ValueError("Percentual deve estar entre 0 e 100.")
 return round(price*(1-percentage/100),2)
def validate_email(email):
 if not isinstance(email,str): return False
 return bool(re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+",email.strip()))
def normalize_product_name(name):
 if not isinstance(name,str): raise TypeError("Nome do produto deve ser texto.")
 normalized=" ".join(name.split())
 if not normalized: raise ValueError("Nome do produto não pode ficar vazio.")
 return normalized.title()
