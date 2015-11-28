import re
import datetime


DATE_PATTERN = re.compile("([0-9]{4})([0-9]{2})([0-9]{2})")
def date_range(from_date, to_date):

  def split_by_date(some_date):
    return [int(x) for x in DATE_PATTERN.split(some_date) if x and x.strip()]

  start = split_by_date(from_date)
  end = split_by_date(to_date)

  assert (len(start) == 3 and len(end) == 3), "from_date and/or to_date is malformed. Use YYYYMMDD (e.g. 20150711) only! input: {} {}".format( start, end )

  year, month, day = start
  start_date = datetime.date(year, month, day)
  year, month, day = end
  end_date = datetime.date(year, month, day)

  r = ( end_date + datetime.timedelta(days=1) - start_date ).days
  times = [start_date + datetime.timedelta(days=i) for i in range(r)]

  without_dash = [str(date).replace("-", "") for date in times]
  return without_dash

