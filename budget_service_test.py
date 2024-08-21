import unittest
import datetime

from budget_service import BudgetService


class BudgetServiceTestCase(unittest.TestCase):

    def test_invalid_input(self):
        budgetService = BudgetService()
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 4, 1)
        res = budgetService.totalAmount(start, end)
        self.assertEqual(0, res)  # add assertion here

    def test_single_day(self):
        budgetService = BudgetService()
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 5, 1)
        res = budgetService.totalAmount(start, end)
        self.assertEqual(10, res)

    def test_partial_month(self):
        budgetService = BudgetService()
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 5, 10)
        res = budgetService.totalAmount(start, end)
        self.assertEqual(100, res)

    def test_whole_month(self):
        budgetService = BudgetService()
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 5, 31)
        res = budgetService.totalAmount(start, end)
        self.assertEqual

    def test_cross_month(self):
        budgetService = BudgetService()
        start = datetime.date(2024, 5, 31)
        end = datetime.date(2024, 6, 2)
        res = budgetService.totalAmount(start, end)
        self.assertEqual(30, res)

    def test_cross_three_month(self):
        budgetService = BudgetService()
        start = datetime.date(2024, 5, 31)
        end = datetime.date(2024, 7, 2)
        res = budgetService.totalAmount(start, end)
        self.assertEqual(330, res)

    def test_cross_year(self):
        budgetService = BudgetService()
        start = datetime.date(2024, 7, 31)
        end = datetime.date(2025, 8, 31)
        res = budgetService.totalAmount(start, end)
        self.assertEqual(940, res)


if __name__ == '__main__':
    unittest.main()
