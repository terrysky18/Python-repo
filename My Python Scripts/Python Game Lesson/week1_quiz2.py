"""
This script is to implement question 6 of week 1 quiz
It is to calculate future value of invested money with compound interest
"""

def future_val(present_val, annual_rate, periods_p_year, years):
	"""
	FV = PV (1 + rate)^period
	"""
	# cast int in float for calculation precision
	present_val = float(present_val)
	periods_p_year = float(periods_p_year)
	years = float(years)

	rate_p_period = annual_rate / periods_p_year
	periods = periods_p_year * years

	future_val = present_val*(1.0 + rate_p_period)**periods
	return future_val

# end of function definition

PV = 1000		# present value
rate = 0.02		# nominal interest rate per period
Period_p_Year = 365	# periods per year
years = 3		# number of years

FV = future_val(PV, rate, Period_p_Year, years)		# future value

print "%d at %.2f per cent compounded daily for %d years yield %.6f" % (PV,
		rate, years, FV)

