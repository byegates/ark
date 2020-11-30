import pandas_market_calendars as mcal

# Show available calendars
# print(mcal.get_calendar_names())

# Create a calendar

def main(start_date='2020-01-01', end_date='2020-10-15', cal='NYSE')
nyse = mcal.get_calendar(cal)

nyse2020 = nyse.schedule(start_date=start_date, end_date=end_date)

l = [ dt.strftime("%Y-%m-%d")  for dt in nyse2020.index]

return l

if __name__ == "__main__":
    main()