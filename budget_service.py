import calendar
import datetime

from dateutil.relativedelta import relativedelta


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

    def total_amount(self, start, end):

        if start > end:
            return 0

        if start.year == end.year and start.month == end.month:
            return self.get_single_day_amount(start.year, start.month) * (end.day - start.day + 1)

        total_amount = self.get_single_day_amount(start.year, start.month) * (
                self.get_days_in_month(start.year, start.month) - start.day + 1) + self.get_single_day_amount(end.year,
                                                                                                              end.month) * end.day
        current_date = start + relativedelta(months=1)
        end_month = datetime.date(end.year, end.month, 1)
        while current_date < end_month:
            total_amount += self.get_single_day_amount(current_date.year, current_date.month) * self.get_days_in_month(
                current_date.year,
                current_date.month)
            current_date += relativedelta(months=1)

        return total_amount


class Budget:
    year_month: str
    amount: int

    def __init__(self, year_month, amount):
        self.year_month = year_month
        self.amount = amount


class BudgetRepo:
    def get_all(self):
        return [
            Budget("202405", 310),
            Budget("202406", 300),
            Budget("202407", 310),
            Budget("202408", 310),
            Budget("202505", 310),
            Budget("202508", 310),
        ]
