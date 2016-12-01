import datetime
from collections import defaultdict
import random
#example data
data = [
 {'closing_price': 102.06,
 'date': datetime.datetime(2014, 8, 29, 0, 0),
 'symbol': 'AAPL'},
 # ...
]


"""case1
know the highest-ever closing price for each stock"""
# group rows by symbol
by_symbol = defaultdict(list)
for row in data:
    by_symbol[row['symbol']].append(row)

# use a dict comprehension to find the max for each symbol
max_price_by_symbol = {symbol: max(row['closing_price']
                                  for row in grouped_rows)
                                  for symbol, grouped_rows in by_symbol.iteritems()}

print max_price_by_symbol


# to pick a field out of a dict
def picker(field_name):
    """returns a function that picks a field out of a dict"""
    return lambda row: row[field_name]


def pluck(field_name, rows):
    """turn a list of dicts into the list of field_name values"""
    return map(picker(field_name), rows)


# or you can do this
def group_by(grouper, rows, value_transform=None):
    grouped = defaultdict(list)
    for row in rows:
        grouped[grouper(row)].append(row)

    if value_transform is None:
        return grouped
    else:
        return {key: value_transform(rows)
                for key, rows in grouped.iteritems()}

# example
max_price_by_symbol = group_by(picker("symbol"),
                               data,
                               lambda rows: max(pluck('closing_price', rows)))


"""CASE 2
know the largest and smallest one-day percent changes: today price/ yesterday price - 1"""


def percent_change(yesterday, today):
    return today['closing_price']/yesterday['closing_price'] - 1


def day_over_day_changes(grouped_rows):
    # sort the rows by date
    ordered = sorted(grouped_rows, key=picker('date'))

    # use zip to get pairs(current, past)
    # zip with an offset to get pairs of consecutive days
    return [{'symbol': today['symbol'],
             'date': today['date'],
             'change': percent_change(yesterday, today)}
            for yesterday, today in zip(ordered, ordered[1:])]


# key is a symbol, value is list of changes
changes_by_symbol = group_by(picker('symbol'), data, day_over_day_changes)

# collect all the "change" dicts into one big list
all_changes = [change
               for changes in changes_by_symbol.values()
               for change in changes]

# find the smallest and largest change
max(all_changes, key=picker('change'))
min(all_changes, key=picker('change'))

# to combine percent changes, we add 1 to each, multiply them, and subtract 1
# for instance, if we combine +10% and -20%, the overall change is
# (1 + 10%) * (1 - 20%) - 1 = 1.1 * .8 - 1 = -12%
def combine_pct_change(pct_ch1, pct_ch2):
    return (pct_ch1+1)*(pct_ch2+1)-1
def overall_change(changes):
    return reduce(combine_pct_change, pluck('change', changes))
overall_change_by_month = group_by(lambda row: row['date'].month,
                                   all_changes,
                                   overall_change)

def split_data(data, prob):

    """split data into fractions [prob, 1 - prob]"""
    results = [], []
    for row in data:
        results[0 if random.random() < prob else 1].append(row)
        print results
    return results