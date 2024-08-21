import calendar
import datetime
from typing import List

from dateutil.relativedelta import relativedelta


class Period:

    def __init__(self, start: datetime.date, end: datetime.date):
        super().__init__()
        self.end = end
        self.start = start


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

        if start.year == end.year and start.month == end.month:
            return self.get_single_day_amount(start.year, start.month) * (end.day - start.day + 1)

        # total_amount_of_end = self.get_single_day_amount(end.year, end.month) * end.day
        # total_amount = total_amount_of_end
        total_amount = 0

        current_date = start
        end_month = datetime.date(end.year, end.month, 1) + relativedelta(months=+1)
        budgets = BudgetRepo().get_all()
        while current_date < end_month:
            budget = next(filter(lambda b: b.year_month == current_date.strftime('%Y%m'), budgets), None)
            if budget is not None:
                overlapping_days = self.overlapping_days(budget, start, end)
                total_amount += budget.daily_amount() * overlapping_days
            current_date += relativedelta(months=1)

        return total_amount

    def overlapping_days(self, budget, start, end):
        period = Period(start, end)
        if budget.year_month == period.start.strftime('%Y%m'):
            overlapping_end = budget.last_day()
            overlapping_start = period.start
        elif budget.year_month == period.end.strftime('%Y%m'):
            overlapping_end = period.end
            overlapping_start = budget.first_day()
        else:
            overlapping_end = budget.last_day()
            overlapping_start = budget.first_day()
        return (overlapping_end - overlapping_start).days + 1


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
