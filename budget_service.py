import calendar
import datetime
from typing import List

from dateutil.relativedelta import relativedelta


class Budget:
    year_month: str
    amount: int

    def __init__(self, year_month, amount):
        self.year_month = year_month
        self.amount = amount

    def get_days(self):
        first_day = self.first_day()
        return calendar.monthrange(first_day.year, first_day.month)[1]

    def daily_amount(self):
        return self.amount / self.get_days()

    def last_day(self):
        first_day = self.first_day()
        return datetime.date(first_day.year, first_day.month, self.get_days())

    def first_day(self):
        return datetime.datetime.strptime(self.year_month, '%Y%m').date()

    def create_period(self):
        return Period(self.first_day(), self.last_day())

    def overlapping_amount(self, period):
        return self.daily_amount() * period.overlapping_days(self.create_period())


class BudgetRepo:
    def get_all(self) -> List[Budget]:
        return [
            Budget("202405", 310),
            Budget("202406", 300),
            Budget("202407", 310),
            Budget("202408", 310),
            Budget("202505", 310),
            Budget("202508", 310),
        ]


class Period:

    def __init__(self, start: datetime.date, end: datetime.date):
        super().__init__()
        self.end = end
        self.start = start

    def overlapping_days(self, another):
        if self.end < another.start or self.start > another.end:
            return 0
        overlapping_start = self.start if self.start > another.start else another.start
        overlapping_end = self.end if self.end < another.end else another.end
        return (overlapping_end - overlapping_start).days + 1


class BudgetService:
    def get_single_day_amount(self, year, month):
        start_year_month = "{:04d}{:02d}".format(year, month)
        records = BudgetRepo().get_all()
        for record in records:
            if record.year_month == start_year_month:
                month_total_days = self.get_days_in_month(year, month)
                return record.amount / month_total_days

        return 0

    def get_days_in_month(self, year, month):
        return calendar.monthrange(year, month)[1]

    def total_amount(self, start: datetime.date, end: datetime.date):

        if start > end:
            return 0

        # total_amount = 0

        budgets = BudgetRepo().get_all()
        period = Period(start, end)
        return sum(map(lambda b: b.overlapping_amount(period), budgets))
        # for budget in budgets:
        #     total_amount += budget.overlapping_amount(period)
        #
        # return total_amount
