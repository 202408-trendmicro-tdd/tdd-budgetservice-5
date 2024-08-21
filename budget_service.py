import calendar
import datetime

from dateutil.relativedelta import relativedelta


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
