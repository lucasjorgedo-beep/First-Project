import unittest
from sample_app import calculate_discount,normalize_product_name,validate_email
class DiscountTests(unittest.TestCase):
 def test_discount(self): self.assertEqual(calculate_discount(100,15),85.0)
 def test_limits(self):
  self.assertEqual(calculate_discount(80,0),80.0); self.assertEqual(calculate_discount(80,100),0.0)
 def test_invalid(self):
  for price,pct in [(-1,10),(100,-1),(100,101),("100",10)]:
   with self.subTest(price=price,pct=pct),self.assertRaises(ValueError): calculate_discount(price,pct)
class EmailTests(unittest.TestCase):
 def test_valid(self): self.assertTrue(validate_email("teste@example.com"))
 def test_invalid(self):
  for value in ["","teste@","@example.com","teste.example.com",None]:
   with self.subTest(value=value): self.assertFalse(validate_email(value))
class ProductNameTests(unittest.TestCase):
 def test_normalize(self): self.assertEqual(normalize_product_name("  caderno   universitário "),"Caderno Universitário")
 def test_empty(self):
  with self.assertRaises(ValueError): normalize_product_name("   ")
if __name__=="__main__": unittest.main()
