import unittest
import datetime
from dateutil.relativedelta import relativedelta
import calendar


def getDaysInMonth(year, month):
    return calendar.monthrange(year, month)[1]


def getSingleDayAmount(year, month):
    startYearMonth = "{:04d}{:02d}".format(year, month)
    records = BudgetRepo().getAll()
    for record in records:
        if record.YearMonth == startYearMonth:
            monthTotoldays = getDaysInMonth(year, month)
            return record.Amount / monthTotoldays

    return 0


class BudgetService:
    def totalAmount(self, start, end):

        if start > end:
            return 0

        if start.year == end.year and start.month == end.month:
            return getSingleDayAmount(start.year, start.month) * (end.day - start.day + 1)

        total = getSingleDayAmount(start.year, start.month) * (
                getDaysInMonth(start.year, start.month) - start.day + 1) + getSingleDayAmount(end.year,
                                                                                              end.month) * end.day
        current_date = start + relativedelta(months=1)
        end_month = datetime.date(end.year, end.month, 1)
        while current_date < end_month:
            total += getSingleDayAmount(current_date.year, current_date.month) * getDaysInMonth(current_date.year,
                                                                                                current_date.month)
            current_date += relativedelta(months=1)

        return total


class Budget:
    YearMonth: str
    Amount: int

    def __init__(self, YearMonth, Amount):
        self.YearMonth = YearMonth
        self.Amount = Amount


class BudgetRepo:
    def getAll(self):
        return [
            Budget("202405", 310),
            Budget("202406", 300),
            Budget("202407", 310),
            Budget("202408", 310),
            Budget("202505", 310),
            Budget("202508", 310),
        ]


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
