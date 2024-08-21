import calendar
import datetime

from dateutil.relativedelta import relativedelta


class BudgetService:
    def getSingleDayAmount(self, year, month):
        startYearMonth = "{:04d}{:02d}".format(year, month)
        records = BudgetRepo().getAll()
        for record in records:
            if record.YearMonth == startYearMonth:
                monthTotoldays = self.getDaysInMonth(year, month)
                return record.Amount / monthTotoldays

        return 0

    def getDaysInMonth(self, year, month):
        return calendar.monthrange(year, month)[1]

    def totalAmount(self, start, end):

        if start > end:
            return 0

        if start.year == end.year and start.month == end.month:
            return self.getSingleDayAmount(start.year, start.month) * (end.day - start.day + 1)

        total = self.getSingleDayAmount(start.year, start.month) * (
                self.getDaysInMonth(start.year, start.month) - start.day + 1) + self.getSingleDayAmount(end.year,
                                                                                                        end.month) * end.day
        current_date = start + relativedelta(months=1)
        end_month = datetime.date(end.year, end.month, 1)
        while current_date < end_month:
            total += self.getSingleDayAmount(current_date.year, current_date.month) * self.getDaysInMonth(
                current_date.year,
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
