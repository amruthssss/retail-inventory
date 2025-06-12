import unittest
from db import validate_sales_data

class TestValidation(unittest.TestCase):
    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            validate_sales_data([{"product_id": 1, "quantity_sold": -5, "sale_date": "2025-06-01"}])

    def test_missing_product_id(self):
        with self.assertRaises(ValueError):
            validate_sales_data([{"product_id": None, "quantity_sold": 5, "sale_date": "2025-06-01"}])

if __name__ == "__main__":
    unittest.main()