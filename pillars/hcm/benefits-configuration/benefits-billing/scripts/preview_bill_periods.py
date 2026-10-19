"""Build a local calendar preview. No network, file writes, or loader calls."""
import argparse
from calendar import monthrange
from datetime import date, timedelta
import json


MONTHS = ('January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December')


def build_preview(calendar_name, payment_due_day, days_overdue, start_year, end_year):
    if not isinstance(calendar_name, str) or not calendar_name.strip():
        raise ValueError('Calendar Name is required.')
    for label, value in (('Payment Due Day', payment_due_day),
                         ('Days Overdue', days_overdue),
                         ('Start Year', start_year), ('End Year', end_year)):
        if type(value) is not int:
            raise ValueError(label + ' must be an integer.')
    if not 1 <= start_year <= end_year <= 9999:
        raise ValueError('Years must satisfy 1 <= Start Year <= End Year <= 9999.')
    if not 1 <= payment_due_day <= 31:
        raise ValueError('Payment Due Day must be between 1 and 31.')
    if days_overdue < 0:
        raise ValueError('Days Overdue must not be negative.')
    periods = []
    for year in range(start_year, end_year + 1):
        for month, month_name in enumerate(MONTHS, 1):
            try:
                due = date(year, month, payment_due_day)
            except ValueError as exc:
                raise ValueError('Payment Due Day {} does not exist in {} {}; '
                                 'ask for a valid day or alternative handling.'
                                 .format(payment_due_day, month_name, year)) from exc
            try:
                overdue = due + timedelta(days=days_overdue)
            except (OverflowError, ValueError) as exc:
                raise ValueError('Payment Overdue Date exceeds the supported date range.') from exc
            periods.append({
                'Billing Period': '{}_{}_{}'.format(calendar_name, year, month_name),
                'Year': year,
                'Period Start Date': date(year, month, 1).isoformat(),
                'Period End Date': date(year, month, monthrange(year, month)[1]).isoformat(),
                'Payment Due Date': due.isoformat(),
                'Payment Overdue Date': overdue.isoformat(),
            })
    return {
        'Calendar Name': calendar_name,
        'Payment Due Day': payment_due_day,
        'Days Overdue': days_overdue,
        'Period Type': 'Calendar',
        'Billing Frequency': 'Monthly',
        'Period Count': len(periods),
        'Periods': periods,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--calendar-name', required=True)
    parser.add_argument('--payment-due-day', required=True, type=int)
    parser.add_argument('--days-overdue', required=True, type=int)
    parser.add_argument('--start-year', required=True, type=int)
    parser.add_argument('--end-year', required=True, type=int)
    args = parser.parse_args()
    try:
        preview = build_preview(args.calendar_name, args.payment_due_day,
                                args.days_overdue, args.start_year, args.end_year)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(preview, indent=2))


if __name__ == '__main__':
    main()
