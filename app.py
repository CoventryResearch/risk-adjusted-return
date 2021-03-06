'''
financial markets dominated by randomness
with some anomalies e.g. momentum

most ML is optimization and for most of finance this means risk-adjusted return
risk-adjusted return is units of return per unit of risk
excess return is rate of return over a benchmark

popular risk measures:
beta
vol
shortfall risk
draw-down risk
lower partial moments

generally, prob of loss (and magnitude)

portfolio optz

mean-variance optimization seeks to maximize the return for any given level of risk (or vice versa)

inputs are expected returns on assets, correlation between assets, risk of each asset
set of optimal portfolios is efficient frontier

portfolio can have multiple sources of return e.g. interest on fixed income, dividends on shares
capital gains from disposal of securities (fixed income and equities)

to value, can use discounted cashflow, statistical valuation, neural networks etc
'''

'''
volatility assumes the riskiness of a security is how much is moves around
most common measure is std dev of historical returns

expected shortfall = dollar value which could reasonably be expected to be lost over a specified period
of time given a pre-specified confidence interval
most popular measure is value at risk

lower partial moments argue that risk is only captured in the downside of the historical volatility
of a portfolio
e.g. std dev of negative returns

drawdown risk is the max historical drawdown of the portfolio
percentage loss between peak and trough
'''

'''
beta = cov(rs, rm) / var(rm)
'''
import numpy as np
import numpy.random as nrand

def vol(returns):
    return np.std(returns)

def beta(returns, market):
    # matrix of returns, market
    m = np.matrix([returns, market])
    # cov of m  / std dev of market returns
    return np.cov(m)[0][1] / np.std(market)

r = rnand.uniform(-1, 1, 50)
m = nrand.uniform(-1, 1, 50)

print('vol=', vol(r))
print('beta=', beta(r, m))

'''
var is most popular measure of expected shortfall
maximum probable loss over a time period i.e. prob 1-alpha

3 approaches to var calculation
- historical sim VaR
- delta normal VaR
- Monte Carlo VaR

historical sim var takes t historical returns, orders them, and takes the loss at the point
in the list which corresponds to alpha

delta-normal var assumes returns generated by assets follow a predefined dist
e.g. normal (though this isn't true!)
with this assumption its possible to calculate the returns and std dev of portfolio as a whole

monte carlo var works by simulating portfolio using stochastic processes
either calibrate to each asset in the portfolio, simulate return paths and combine in 
correlation matrix using e.g. cholesky decomp
or a stochastic process is calibrated to historical returns of the portfolio and return paths
for portfolio are simulated

var has many problems including
- it violated sub-additive rule - requires that the risk of a portfolio cannot exceed the risk
of its consituent assets i.e. no negative diversification
- so variants e.g. conditional VaR and extreme VaR have been proposed
'''

'''
for some metrics the absolute value is returns. this is because if the risk (loss) is higher
we want to discount the expected excess return from the portfolio by a higher amount, 
therefore risk should be positive
'''

def var(returns, alpha):
    # calculates the historical simulation var of the returns
    sorted_returns = np.sort(returns)
    # calc index associated with alpha
    index = int(alpha * len(sorted_returns))
    # var should be positive
    return abs(sorted_returns[index])

def cvar(returns, alpha):
    # calculates the condition VaR of the returns
    sorted_returns = np.sort(returns)
    # calculate the index associated with alpha
    index = int(alpha * len(sorted_returns))
    # calculate total var beyond alpha
    sum_var = sorted_returns[0]
    for i in range(1, index):
        sum_var += sorted_returns[i]
    
    # return average VaR
    # CVaR should be positive
    return abs(sum_var / index)

# example usage
r = nrand.uniform(-1, 1, 50)
print('var(0.05) = ', var(r, 0.05))
print('cvar(0.05) = ', cvar(r, 0.05))


'''
lower partial moments

measures of risk-adjusted return based on vol treat all deviations from the mean as risk

whereas measures of risk-adjusted return based on lower partial moments 
consider only deviations below some predefined minimum return threshold, t as risk
i.e. positive deviations aren't risky

var is a more probabilistic view of loss as the risk of a portfolio
'''

def lpm(returns, threshold, order):
    # this method returns a lower partial moment of the returns
    # create an array the same length as returns containing the minimum return threshold
    threshold_array = numpy.empty(len(returns))
    threshold_array.fill(threshold)
    # calculate the difference between the threshold and the returns
    diff = threshold_array - returns
    # set the minimum of each to 0
    diff = diff.clip(min=0)

    # return the sum of the different to the power of order
    return np.sum(diff ** order) / len(returns)

def hpm(returns, threshold, order):
    # returns a higher partial moment of the returns
    # create an array the same length as returns containing hte minimum return threshold
    threshold_array = np.empty(len(returns))
    threshold_array.fill(threshold)
    # calc the diff between the returns and the threshold
    diff = returns - threshold_array
    # set min of each to 0
    diff = diff.clip(min=0)
    # return sum of the different to the power of order
    return np.sum(diff ** order) / len(returns)

# example usage
r = nrand.uniform(-1,1,50)
print('hpm(0.0)_1 = ', hpm(r, 0.0, 1))
print('lpm(0.0)_1 = ', lpm(r, 0.0, 1))


''' 
drawdown 
maximum decrease in the value of the portfolio over a specific period of time
D(t) = max(0, max(St, St-1))
'''

def dd(returns, tau):
    # returns the draw-down fiven time period tau
    values = prices(returns, 100)
    pos = len(values) - 1
    pre = pos - tau
    drawdown = float('+inf')
    # find max drawdown given tau
    while pre >= 0:
        dd_i = (values[pos] / values[pre]) - 1
        if dd_i < drawdown:
            drawdown = dd_i

        pos, pre = pos - 1, pre - 1
    # drawdown should be pos
    return abs(drawdown)

def max_dd(returns):
    # returns the max draw-down for any tau in (0, T), where T is the length of the return series
    max_drawdown = float('-inf')
    for i in range(0, len(returns)):
        drawdown_i = dd(returns, i)
        if drawdown_i > max_drawdown:
            max_drawdown = drawdown_i
    # max draw-down should be positive
    return abs(max_drawdown)

def average_dd(returns, periods):
    # average drawdown over n periods
    for i in range(0, len(returns)):
        drawdown_i = dd(returns, i)
        drawdowns.append(drawdown_i)
    drawdowns = sorted(drawdowns)
    total_dd = abs(drawdowns[0])
    
    for i in range(1, periods):
        total_dd += abs(drawdowns[i])
    
    return total_dd / periods

def average_dd_squared(returns, periods):
    # returns the average maximum
    drawdowns = []
    for i in range(0, len(returns)):
        drawdown_i = math.pow(dd(returns, i), 2.0)
        drawdowns.append(drawdown_i)
    drawdowns = sorted(drawdowns)
    total_dd = abs(drawdowns[0])

    for i in range(1, periods):
        total_dd += abs(drawdowns[i])
    return total_dd / periods

r = nrand.uniform(-1, 1, 50)
print('drawdown(5) = ', dd(r, 5))
print('max drawdown = ', max_dd(r))


# end of risk measures

'''
measures of risk-adjusted return

discount expected return generated from valuation model by different quantities of risk
to get measures of risk-adjusted return. 

Treynor ratio - one of the first measures. 
metric for rating performance of investment funds. 
Treynor calculates the excess returns generated by a portfolio E(r) - rf
and discounts it by portfolio beta: (E(r) - rd )/ beta

sharpe ratio - extension of Traynor - discounts expected excess returns by vol
(E(r) - rd ) / sigma

information ratio is extension of Sharpe ratio - replaces risk-free rate of return with
the scalar expected return of a benchmark portfolio E(rb)

IR = E(re) / E(sigma e) = (E(r) - E(rb)) / var(E(r) - E(rb)) ^ 0.5

Modigliani ratio - combination of the Sharpe and info ratios
- adjusts the expected excess returns of the portfolio above the risk free rate by the 
expected excess returns of a benchmark portfolio, above the risk free rate

M2  = E(re) * E(sigma b) / E(sigma e) + rf
'''

def treynor_ratio(er, returns, market, rf):
    return (er - ef) / beta(returns, market)

def sharpe_ratio(er, returns, rf):
    return (er - ef) / vol(returns)

def information_ratio(returns, benchmark):
    diff = returns - benchmark
    return np.mean(diff) / vol(diff)

def modigliani_ratio(er, returns, benchmark, rf):
    np_rf = np.empty(len(returns))
    np_rf.fill(rf)
    rdiff = returns - np_rf
    bdiff = benchmark - np_rf
    return (er - rf) * (vol(rdiff) / vol(bdiff)) + rf


'''
measures of risk-adjusted return based on value at risk
excess return on value at risk discounts the excess return of the portfolio above
the risk-free rate by the value at risk of the portfolio

EVaR = E(re) / VaRf

conditional sharpe ratio - discounts the excess return of the portfolio above the 
risk-free rate by the conditional VaR of the portfolio

CSR = E(re) / CVaRr
'''

def excess_var(er, returns, rf, alpha):
    return (er - rf) / var(returns, alpha)

def conditional_sharpe_ratio(er, returns, rf, alpha):
    return (er - rf) / cvar(returns, alpha)


'''
omega ratio discounts the excess returns of a portfolio above the target threshold
(usually risk-free rate), by the first-order lower partial moment of the returns.
first-order lower partial moment corresponds to the average expeceted loss aka
downside risk

omega(t) = E(r) - t / LPM1(t)

sortino ratio 
modification of sharpe - only uses downside vol (delta)

SOR(t) = E(re) / delta^2 = (E(r) - t) / delta^2

kappa ratio - generalization of omega and sortino ratios
if j = 1, kappa is omega, j = 2, kappa is sortino

Kj(t) = E(re) / ith root of (LPMj(t))

gain-loss ratio - discounts first order higher partial moment of a portfolio's returns,
upside potential, by the first-order lower partial moment of a portfolio's returns, 
downside risk

GLR(t) = HPM1(t) / LPM1(t)

upside-potential ratio
discounts first order higher partial moment of a portfolio's returns, upside potential,
by the second-order lower partial moment of a portfolio's returns, downside variation

UPR(t) = HPM1(t) / LPM2(t) ^ 0.5
'''

def omega_ratio(er, returns, rf, target=0):
    return (er - rf) / lpm(returns, target, 1)

def sortino_ratio(er, returns, rf, target=0):
    return (er -rf) / math.sqrt(lpm(returns, target, 2))

def kappa_three_ratio(er, returns, rf, target=0):
    return (er - rf) / math.pow(lpm(returns, target, 3), float(1/3))

def gain_loss_ratio(returns, target=0):
    return hpm(returns, target, 1) / lpm(returns, target, 1)

def upside_potential_ratio(returns, target=0):
    return hpm(returns, target, 1) / math.sqrt(lpm(returns, target, 2))

'''
measures of risk-adjusted return based on drawdown risk

calmar ratio - discounts expected excess return of a portfolio by the 
worst expected maximum draw down for that portfolio

CR = E(re)/MD1 = (E(r) - rf) / MD1

Sterling ratio
discounts the expected excess return of a portfolio by the average of the N worst
expected maximum drawdowns for that portfolio

CR = E(re) / (1/N)(sum MDi)

Burke Ratio
similar to sterling, but less sensitive to outliers
discounts the expected excess return of a portfolio by the square root of the average
of the N worst expected maximum drawdowns for that portfolio

BR = E(re) / ((1/N)(sum MD^2))^0.5
---> smoothing, can take roots, logs etc
'''

def calmar_ratio(er, returns, rf):
    return (er-rf) / max_dd(returns)

def sterling_ratio(er, returns, rf, periods):
    return (er - ef) / average_dd(returns, periods)

def burke_ratio(er, returns, rf, periods)
    return (er - ef) / math.sqrt(average_dd_squared(returns, periods))















