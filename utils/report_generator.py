from collections import defaultdict
from datetime import datetime

def generate_report(records, by='student', start_date=None, end_date=None):
    """
    Generates attendance reports.

    Args:
      records (list of dict): List of attendance records with keys:
        - student_id
        - subject
        - date (YYYY-MM-DD)
        - time (HH:MM)
        - status (present, absent, late)
      by (str): 'student' or 'class' - report grouping type
      start_date (str): filter start date 'YYYY-MM-DD'
      end_date (str): filter end date 'YYYY-MM-DD'

    Returns:
      dict: Aggregated attendance report.
    """

    # Filter by date range if given
    def in_date_range(date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        if start_date:
            if date_obj < datetime.strptime(start_date, "%Y-%m-%d").date():
                return False
        if end_date:
            if date_obj > datetime.strptime(end_date, "%Y-%m-%d").date():
                return False
        return True

    filtered = [r for r in records if in_date_range(r['date'])]

    report = defaultdict(lambda: {'present': 0, 'absent': 0, 'late': 0, 'total': 0})

    if by == 'student':
        for rec in filtered:
            key = rec['student_id']
            status = rec['status'].lower()
            report[key]['total'] += 1
            if status in report[key]:
                report[key][status] += 1
        return dict(report)

    elif by == 'class':
        # Class level report grouped by subject
        for rec in filtered:
            key = rec['subject']
            status = rec['status'].lower()
            report[key]['total'] += 1
            if status in report[key]:
                report[key][status] += 1
        return dict(report)

    else:
        # If unknown group, just return raw filtered data
        return filtered
