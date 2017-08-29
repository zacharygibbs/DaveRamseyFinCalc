import zach
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pdb

#
import matplotlib
matplotlib.rc_params({'font.size':14})

def min_ignorezero(array):
    newarray = []
    for i in array:
        if i <= 0:
            newarray.append(np.nan)
        else:
            newarray.append(i)
    #pdb.set_trace()
    return np.nanmin(newarray)

def whichone_debtfun(case1, i):
    whichone =[case1['debt']['cc'][i], case1['debt']['student'][i], case1['debt']['auto'][i]].index(min_ignorezero([case1['debt']['cc'][i], case1['debt']['student'][i], case1['debt']['auto'][i]]))
    whichone_debt = ['cc','student','auto'][whichone]
    return whichone_debt

def cc_minpayment(debt, interestrate, princpct):
    #monthly cc payment
    return debt*(princpct/100/12 + interestrate/100./12.)
def loan_monthlypayment(debt0, yearstopay, interestrate):
    totaldebt=0.
    remainingbalance = debt0
    c = debt0*(1+interestrate/100./12.)**(yearstopay*12) / (((1+interestrate/100./12.)**(yearstopay*12) - 1.) / (interestrate/100./12.))
    #self.P0*(1+self.r/12.)**(t*12.) - self.c*((1+self.r/12.)**(t*12.)-1.)/(self.r/12.)
    return c
def loan_balance(month):
    return loan_amount*((1.+mortgage_interest/100./12)**(loan_term*12)-(1.+mortgage_interest/100./12)**(month) )/ ((1+mortgage_interest/100./12)**(loan_term*12)-1.)
def equity_balance(month):
    ans = loan_amount - loan_balance(month) + mortgage_downpayment
    if ans > loan_amount + mortgage_downpayment:
        ans = loan_amount + mortgage_downpayment
    else:
        pass
    return ans

class DaveRamsey():
    def __init__(self):
        pass#self.debt = {'cc': 0., 'student': 0., 'auto':0.}
        #self.

    def setup(self, debt, rate, income0, raisepercent, taxes, 
        Emergency_FundMonths, rice_beans, utils, percent_housing,  maxhousing, 
        investment_return, capital_gains, retirement0, investments0, company_match, percent_retirement, amount_of_lifestyle_increase, inflation,
        mortgage_value, mortgage_downpayment, mortgage_interest, loan_term, home_taxes_insurance):
        self.debt = debt
        self.rate = rate
        self.income0 = income0
        self.raisepercent = raisepercent
        self.taxes = taxes
        self.Emergency_FundMonths = Emergency_FundMonths
        self.rice_beans = rice_beans
        self.utils = utils
        self.percent_housing = percent_housing
        self.maxhousing = maxhousing
        self.investment_return = investment_return
        self.capital_gains = capital_gains
        self.retirement0 = retirement0
        self.investments0 = investments0
        self.company_match = company_match
        self.percent_retirement = percent_retirement
        self.amount_of_lifestyle_increase = amount_of_lifestyle_increase
        self.inflation = inflation
        self.mortgage_value = mortgage_value# = 200000. #
        self.mortgage_downpayment = mortgage_downpayment# = 0.2*mortgage_value
        self.mortgage_interest = mortgage_interest
        self.loan_term = loan_term# = 30.0 #yrs
        self.loan_amount = (mortgage_value-mortgage_downpayment)
        self.monthly_payment = loan_amount * (mortgage_interest/100./12*(1.+mortgage_interest/100./12)**(loan_term*12))/((1.+mortgage_interest/100./12)**(loan_term*12)-1)
        self.home_taxes_insurance = home_taxes_insurance #= 0.02 * mortgage_value/12. #monthly payment

        #Average - 16,061$ cc debt, $49042 - Student Loan, $28535 auto
        #https://www.nerdwallet.com/blog/average-credit-card-debt-household/
        #debt = {"cc":16061., "student":49042, "auto":28535}

        #rate = {"cc":15.07, "student":6.8, "auto": 4.3}
        self.studentloanpayment = loan_monthlypayment(debt['student'], 10, rate['student'])
        self.autoloanpayment = loan_monthlypayment(debt['auto'], 5, rate['auto'])
        #ccrate - http://www.creditcards.com/credit-card-news/interest-rate-report-100114-up-2121.php
        #student loan rate - https://www.credible.com/blog/what-are-average-student-loan-interest-rates/
        #auto - 4.3%
    def calc(self, number_of_years, retirement_match=False, pay_house_first=True, verbose=True):
        self.number_of_years = number_of_years
        self.case1 = {'debt':{"cc":[], "student":[], "auto":[]}, 'savings':[], 'investments':[], 'investment_return':[], 
                        'retirement':[], 'mortgage':[], "rent":[], "income":[], "expenses":[], "networth":[], 'networth_taxed':[]}
        #case1_
        self.case1['retirement'].append(self.retirement0)
        self.case1['investments'].append(self.investments0)
        self.case1['investment_return'].append(0.)
        try:
            del self.month_networth_pos
            del self.month_networth_taxed_pos
        except:
            pass
        debt_free_yet = False

        for i in range(number_of_years*12):
            if i==0:
                self.case1["income"].append(self.income0)
            elif i%12==0:
                self.case1['income'].append(self.case1['income'][i-1]*(1+self.raisepercent/100.))
            else:
                self.case1['income'].append(self.case1['income'][i-1])
            #payments out
            self.case1["rent"].append(np.min([(1.-self.taxes/100.)*self.case1['income'][i]/12*self.percent_housing/100, self.maxhousing]))
            if i== 0:
                self.case1['mortgage'].append(0.)
                self.case1["expenses"].append((self.rice_beans + self.case1["rent"][i]+self.utils)*(1.+self.inflation/100.)**(i/12.))
            elif np.sum([j[-1] for j in self.case1['debt'].values()])>0.01:
                self.case1['mortgage'].append(self.case1['mortgage'][i-1])
                if self.case1['mortgage'][i-1]>0.01:
                    if self.case1['mortgage'][i-1] == self.mortgage_downpayment+self.loan_amount:
                        self.case1['rent'][i] =  0.
                    else:
                        self.case1['rent'][i] = self.monthly_payment+self.home_taxes_insurance
                    self.case1["expenses"].append((self.rice_beans +self.utils)*(1.+self.inflation/100.)**(i/12.)+ self.case1["rent"][i])
                else:
                    self.case1["expenses"].append((self.rice_beans + self.case1["rent"][i]+self.utils)*(1.+self.inflation/100.)**(i/12.))
            else:
               self.case1['mortgage'].append(self.case1['mortgage'][i-1])
               if self.case1['mortgage'][i-1]>0.01:
                    if self.case1['mortgage'][i-1] == self.mortgage_downpayment+self.loan_amount:
                        self.case1['rent'][i] =  0.
                    else:
                        self.case1['rent'][i] = self.monthly_payment+self.home_taxes_insurance
                    self.case1["expenses"].append((self.rice_beans * (1.+self.amount_of_lifestyle_increase/100) + self.utils)*(1.+self.inflation/100.)**(i/12.)+ self.case1["rent"][i])
               else:
                    self.case1["expenses"].append((self.rice_beans * (1.+self.amount_of_lifestyle_increase/100)+ self.case1["rent"][i]+self.utils)*(1.+self.inflation/100.)**(i/12.))
               #self.case1['expenses'].append((self.rice_beans*(1.+self.amount_of_lifestyle_increase/100) + self.case1["rent"][i]+self.utils)*(1+self.inflation/100.)**(i/12.))
            #Baby Step 1: Save $1000
                #assume this is done already
            #Baby Step 2: Debts
            totaldebtpaid = 0
            extra_money = 0
            ################# Pay Debts - minimum payments on debt
            for (j,k) in self.case1['debt'].items():
                    if j=='cc':
                        if i>0:
                            if self.case1['debt'][j][i-1]>0:
                                paydebt = cc_minpayment(self.case1['debt']['cc'][-1], self.rate['cc'], 1.0)
                            else:
                                paydebt = 0
                        else:
                            if self.case1['debt'][j]>0:
                                paydebt = cc_minpayment(self.debt['cc'], self.rate['cc'], 1.0)
                            else:
                                paydebt = 0
                    elif j=='student':
                        if i>0:
                            if self.case1['debt'][j][i-1]>0:
                                paydebt = self.studentloanpayment
                            else:
                                paydebt = 0
                        else:
                            if self.case1['debt'][j]>0:
                                paydebt = self.studentloanpayment
                            else:
                                paydebt = 0
                    elif j=='auto':
                        if i>0:
                            if self.case1['debt'][j][i-1]>0:
                                paydebt = self.autoloanpayment
                            else:
                                paydebt = 0
                        else:
                            if self.case1['debt'][j]>0:
                                paydebt = self.autoloanpayment
                            else:
                                paydebt = 0
                    if i==0:
                        #print self.case1['debt']
                        self.case1['debt'][j].append(self.debt[j]*(1.+self.rate[j]/100./12.)-paydebt)    
                    else:
                        self.case1['debt'][j].append(self.case1['debt'][j][i-1]*(1.+self.rate[j]/100./12.)-paydebt)
                    totaldebtpaid = totaldebtpaid + paydebt 
                    if self.case1['debt'][j][i] < 0:
                        extra_money = extra_money + -1*self.case1['debt'][j][i]
                        totaldebtpaid = totaldebtpaid + extra_money
            #print totaldebtpaid
            if self.case1['income'][i]*(1.-self.taxes/100.)/12-self.case1['expenses'][i] - totaldebtpaid + extra_money < 0:
                    print "OH NO, wespent all the $$ - not enough $$ to cover minimum expenses + debt"
            else:
                if retirement_match and (self.case1['debt']['cc'] >0 or self.case1['debt']['auto'] >0 or self.case1['debt']['student'] >0):
                    if self.company_match/100.*self.case1['income'][i]/12. < (self.case1['income'][i]*(1.-self.taxes/100.)/12-self.case1['expenses'][i] - totaldebtpaid)/(1.-self.taxes/100.):
                        self.case1['retirement'].append(self.case1['retirement'][i-1]*(1+self.investment_return/100./12.)+ (2.0 * self.company_match/100.)*self.case1['income'][i]/12.)
                        totaldebtpaid = totaldebtpaid + self.company_match/100.*self.case1['income'][i]/12. * (1-self.taxes/100.)
                    else:
                        self.case1['retirement'].append(self.case1['retirement'][i-1]*(1+self.investment_return/100./12.)+ 2.0*(self.case1['income'][i]*(1.-self.taxes/100.)/12-self.case1['expenses'][i] - totaldebtpaid)/(1.-self.taxes/100.))
                        totaldebtpaid = totaldebtpaid + (self.case1['income'][i]*(1.-self.taxes/100.)/12-self.case1['expenses'][i] - totaldebtpaid)/(1.-self.taxes/100.)
                    if i==0:
                        self.case1['retirement'] = [self.case1['retirement'][-1]]
                else:
                    pass


            #pdb.set_trace()
            if i==0:
                whichone_debt = whichone_debtfun(self.case1, i)
            elif not np.isnan(min_ignorezero([self.case1['debt']['cc'][i-1], self.case1['debt']['student'][i-1], self.case1['debt']['auto'][i-1]])):
                whichone_debt = whichone_debtfun(self.case1, i-1)
            else:
                whichone_debt = 10000
            if i>=0:
                for (j,k) in self.case1['debt'].items():
                    if whichone_debt==j:
                        
                        paydebt = self.case1['income'][i]/12*(1.-self.taxes/100.)-self.case1['expenses'][i] - totaldebtpaid
                        self.case1['debt'][j][i] = self.case1['debt'][j][i] - paydebt
                        totaldebtpaid = totaldebtpaid + paydebt 
                    else:
                        paydebt = 0.
                        self.case1['debt'][j][i] = self.case1['debt'][j][i] - paydebt
                    if self.case1['debt'][j][i] < 0:
                        extra_money = extra_money + -1*self.case1['debt'][j][i]
                        self.case1['debt'][j][i] = 0

                if extra_money >0:
                    if not np.isnan(min_ignorezero([self.case1['debt']['cc'][i], self.case1['debt']['student'][i], self.case1['debt']['auto'][i]])):
                        whichone_debt = whichone_debtfun(self.case1, i)
                        paydebt = extra_money
                        self.case1['debt'][whichone_debt][i] = self.case1['debt'][whichone_debt][i] - extra_money
                        extra_money = 0
                    if self.case1['debt'][whichone_debt][i]<0:
                        print "I hope this never happens!", extra_money, self.case1['debt'][whichone_debt][i]
            #Baby Step 3 - 3-6 months of expenses
            #Baby Step 3b - save up a down payment, mortgage?

            #Baby Step 4 - 15% of your income into retirement
            #baby step 5 - College Retirement
            #Baby Step 6 - Pay off House
            #Baby Step 7 - give
            #
            if (self.case1['debt']['cc'][i] + self.case1['debt']['auto'][i] + self.case1['debt']['student'][i]<0.01) and not debt_free_yet:
                if verbose:
                    print 'Debt free after %i months!' %(i)

                debt_free_yet = True
                self.month_debt_free=i

            if i==0:
                self.case1["savings"].append(1000.) #assume $1000 emergency fund in place already
                self.case1['networth'].append(self.case1['savings'][i] + -1*(self.case1["debt"]["cc"][i]+self.case1["debt"]["student"][i] + self.case1["debt"]["auto"][i]))
                self.case1['networth_taxed'].append(self.case1['savings'][i] + -1*(self.case1["debt"]["cc"][i]+self.case1["debt"]["student"][i] + self.case1["debt"]["auto"][i]))
            else:
                #self.case1["retirement"].append(0.15*self.case1["income"][i]+match)
                months_extra_money = self.case1['income'][i]*(1.-self.taxes/100.)/12-self.case1['expenses'][i] - totaldebtpaid + extra_money
                
                if self.case1["savings"][i-1] < self.Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid):
                    self.case1["savings"].append(self.case1['savings'][i-1] + np.min([months_extra_money, self.Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid) - self.case1['savings'][i-1] ] ))
                    #months_extra_money0=months_extra_money
                    months_extra_money = months_extra_money - (self.case1['savings'][i] - self.case1['savings'][i-1])
                    #print months_extra_money0, months_extra_money#extra income goes to retirement
                    #val = np.min([self.case1["savings"][i] - Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid), percent_retirement*self.case1['income'][i]])
                else:
                    self.case1['savings'].append(self.case1['savings'][i-1])
                #print 'a', months_extra_money, self.case1['mortgage'][i]
                if months_extra_money>0.01 and self.case1['mortgage'][i]<0.10:
                    #baby step 3b - save for down payment

                    if self.case1["savings"][i] < (self.Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid) + self.mortgage_downpayment ):
                        #if you haven't saved enough for the down payment, then put it in the account!
                        import copy
                        prev = copy.deepcopy(self.case1['savings'][i])

                        self.case1['savings'][i] = self.case1['savings'][i] + np.min([months_extra_money,self.Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid) + self.mortgage_downpayment - self.case1['savings'][i]])
                        #prev2 = copy.deepcopy(months_extra_money)
                        months_extra_money = months_extra_money - (self.case1['savings'][i]-prev)
                        #print months_extra_money, self.case1['savings'][i], prev
                        #print i,prev, self.case1['savings'][i], np.min([prev2,Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid) + mortgage_downpayment - self.case1['savings'][i]]), Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid) + mortgage_downpayment
                        if months_extra_money>0.01: 
                            #purchase the house
                            if verbose:
                                print 'bought the house with %g down, %i yr term, %g pct: interest rate at month: %i'%(mortgage_downpayment,loan_term, mortgage_interest, i)
                                #print self.case1['savings'][i], self.Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid) + self.mortgage_downpayment, months_extra_money, self.mortgage_downpayment
                            self.mortgage_startdate = i
                            self.case1['mortgage'][i] = self.mortgage_downpayment
                            self.case1['savings'][i] = self.case1['savings'][i] - self.mortgage_downpayment
                elif self.case1['mortgage'][i] > 0.01:
                    #### Cost of the mortgage already came out in the expenses portion. This is to tabulate the equity in the home
                    interest_paid = (self.mortgage_interest/100./12) * (self.mortgage_value- self.case1['mortgage'][i-1])
                    if self.case1['rent']>0:
                        ans = self.case1['mortgage'][i-1] +  self.case1['rent'][i] - interest_paid  - self.home_taxes_insurance# equity_balance(i - mortgage_startdate) #already calculated this!
                    else:
                        ans = self.loan_amount + self.mortgage_downpayment

                    #print ans
                    if ans > self.loan_amount + self.mortgage_downpayment:
                        #print i, ans
                        months_extra_money = months_extra_money + ans - (self.loan_amount + self.mortgage_downpayment)
                        ans = self.loan_amount + self.mortgage_downpayment

                    self.case1['mortgage'][i] = ans#self.case1['mortgage'][i-1] +  monthly_payment - interest_paid# equity_balance(i - mortgage_startdate) #already calculated this!
                    #could calculate mortgage interest paid if I wanted to?
                if months_extra_money>0.01:
                    #pdb.set_trace()
                    if retirement_match:
                        if months_extra_money / self.case1['income'][i]*12.*100. > (self.percent_retirement/100. - self.company_match/100.)*(1.-self.taxes/100.):#*self.case1['income'][i]/12:
                            self.case1['retirement'][i] = self.case1['retirement'][i] + (self.percent_retirement/100. - self.company_match/100.)*self.case1['income'][i]/12.#company match already added in previous code, so just add the remaining amount
                            months_extra_money = months_extra_money - (self.percent_retirement/100. - self.company_match/100.)*self.case1['income'][i]/12.*(1.-self.taxes/100.) # this will break down if negative?
                           # print self.case1['retirement'][i], months_extra_money, i
                            #these are post-tax investments, correct?

                        else:
                            self.case1['retirement'][i] = self.case1['retirement'][i] + months_extra_money / (1. - self.taxes/100.)
                            months_extra_money =  0.

                    else:
                        if months_extra_money / self.case1['income'][i]*12*100 > self.percent_retirement*(1. - self.taxes/100.):
                            self.case1['retirement'].append(self.case1['retirement'][i-1]*(1+self.investment_return/100./12.)+ (self.percent_retirement/100. + self.company_match/100.)*self.case1['income'][i]/12.)
                            months_extra_money = months_extra_money - self.percent_retirement/100. * self.case1['income'][i]/12 * (1. - self.taxes/100.)
                            #these are post-tax investments, correct?
                        else:
                            self.case1['retirement'].append(self.case1['retirement'][i-1]*(1.+self.investment_return/100./12.)+months_extra_money/(1. - self.taxes/100.))
                            months_extra_money =  0.
                else:
                     if retirement_match:
                        pass
                     else:
                        self.case1['retirement'].append(self.case1['retirement'][i-1]*(1.+self.investment_return/100./12.))
                #self.case1['savings'][i] = self.case1['savings'][i] + 
                if months_extra_money<-0.01:
                    self.case1['retirement'][i] = self.case1['retirement'][i] + months_extra_money
                    print 'retirement took all my money on %i month, i had %g left' %(i, months_extra_money)
                    months_extra_money = 0
                ##### Save for a house? Either after 3-6 months or 
                if months_extra_money>0.01:
                    # if there's still $$ after retirement, dump money into the house!
                    # 
                    if pay_house_first:
                        if self.case1['mortgage'][i] < mortgage_value-5:
                            self.case1['mortgage'][i] = self.case1['mortgage'][i] + months_extra_money
                            if self.case1['mortgage'][i] > mortgage_value:
                                months_extra_money = self.case1['mortgage'][i]- mortgage_value
                                self.case1['mortgage'][i] = mortgage_value
                            else:
                                months_extra_money = 0.
                        else:
                            pass
                if months_extra_money>0.01:
                        self.case1['investments'].append(self.case1['investments'][i-1]*(1.+self.investment_return/100./12.)+months_extra_money)
                else:
                    self.case1['investments'].append(self.case1['investments'][i-1]*(1.+investment_return/100./12.))
                    #taxable investment accounts
                self.case1['investment_return'].append(self.case1['investment_return'][i-1] + self.case1['investments'][i] - self.case1['investments'][i-1] - months_extra_money)
                months_extra_money = 0.#months_extra_money - self.case1['investments'][i] - self.case1['investments'][i-1]

                if months_extra_money>0:
                    self.case1['savings'][i] = self.case1['savings'][i]+ months_extra_money


                #print val / self.case1['income'][i]*12*100,"%"
                
                self.case1["networth"].append(self.case1['investments'][i] + self.case1['retirement'][i] + self.case1['savings'][i] +self.case1['mortgage'][i]+ -1*(self.case1["debt"]["cc"][i]+self.case1["debt"]["student"][i] + self.case1["debt"]["auto"][i]) )
                if self.case1['networth'][i]>0 and not hasattr(self,'month_networth_pos'):
                    self.month_networth_pos = i
                self.case1['networth_taxed'].append(self.case1['investments'][i] - self.case1['investment_return'][i] * self.capital_gains/100.+ self.case1['retirement'][i] * (1. - self.taxes/100.) + self.case1['savings'][i] +self.case1['mortgage'][i]+ -1*(self.case1["debt"]["cc"][i]+self.case1["debt"]["student"][i] + self.case1["debt"]["auto"][i]) )
                if self.case1['networth_taxed'][i]>0 and not hasattr(self,'month_networth_taxed_pos'):
                    self.month_networth_taxed_pos = i
            ###### ADD Interest paid monthly calculator
            ###### Sensitivity of monthly expenses?
            self.months = np.arange(self.number_of_years*12)

    def adjust_var_to_zero_networth_taxed(self, var_to_adjust, month_to_set):
        
        #var_to_adjust = 'rice_beans'
        #month_to_set = test2.month_networth_taxed_pos
        def optfun(frac):
            #test3 = DaveRamsey()
            orig_value = getattr(self, var_to_adjust)
            # self.setup(self.debt, self.rate, self.income0, self.raisepercent, self.taxes, 
            # self.Emergency_FundMonths, self.rice_beans, self.utils, self.percent_housing,  self.maxhousing,
            # self.investment_return, self.capital_gains, self.retirement0, self.investments0, self.company_match, self.percent_retirement, self.amount_of_lifestyle_increase, self.inflation, 
            # self.mortgage_value, self.mortgage_downpayment, self.mortgage_interest, self.loan_term, self.home_taxes_insurance)
            setattr(self, var_to_adjust, getattr(self, var_to_adjust)*frac)
            del self.month_networth_taxed_pos
            del self.month_networth_pos
            self.calc(number_of_years, retirement_match=False, pay_house_first=True, verbose=False)
            setattr(self, var_to_adjust, orig_value)
            return self.month_networth_taxed_pos- month_to_set
        a = np.arange(0, .99, .01).tolist()
        a.reverse()
        solution = -1
        for i in a:
            ans = optfun(i)
            #print ans
            if ans > 0:
                pass
            else:
                solution = i
            if solution > -1:
                break

        if solution == -1:
            print "no way to reduce rice and beans enough"
        
        return solution

    def plot_wealth(self,fignum):
        
        plt.figure(fignum)
        plt.plot(self.months, self.case1['networth'], 'k-', lw=3)
        plt.plot(self.months, np.zeros(len(self.months)), 'k:', lw=1)
        plt.fill_between(self.months, -1.*(np.array(self.case1['debt']['cc'])+ np.array(self.case1['debt']['student'])+np.array(self.case1['debt']['auto'])), color='r',alpha=1, lw=3)
        plt.fill_between(self.months, np.array(self.case1['retirement'])+np.array(self.case1['investments'])+np.array(self.case1['savings'])+np.array(self.case1['mortgage']), np.array(self.case1['retirement'])+np.array(self.case1['mortgage'])+np.array(self.case1['savings']), color='b', lw=3)
        plt.fill_between(self.months, np.array(self.case1['retirement'])+np.array(self.case1['savings'])+np.array(self.case1['mortgage']), np.array(self.case1['savings'])+np.array(self.case1['mortgage']),color='g',lw=3, alpha=1)
        plt.fill_between(self.months, np.array(self.case1['savings'])+np.array(self.case1['mortgage']), self.case1['savings'], color='c', lw=3, alpha=1)
        plt.fill_between(self.months, self.case1['savings'], np.zeros(len(self.months)), color='m', lw=3, alpha=1)
        plt.plot([self.month_networth_pos], 0., 'kx', ms=8)
        plt.plot([self.month_debt_free], 0., 'rs', ms=8)
        plt.plot([self.month_networth_taxed_pos], 0., 'bs', ms=8)

        plt.xlabel('months')
        plt.ylabel('wealth')




if __name__ == "__main__":
    print "Hello World"

    #Student Loans
    #Credit Card Debt
    #Car Loan
    #Debt Snowball
    #Quantify Risk?
    #delay 401K
    #15% of income for the rest of your life
    #how does time fit into it? Gazelle Intensity? - What if you don't follow exactly
    #Rice & Beans - how much can you live on?
    #All of the things w/ motors are less than 1/2?? your annual income
    #Mortage @ 15 year (less than 1/4 of your monthly income)
    

    #ideas - emergencies @ random?
    # Tornado plot/sensitivity analysis on some stuff, monte carlo on investment return?


    #Do as % of income?

    #Average - 16,061$ cc debt, $49042 - Student Loan, $28535 auto
    #https://www.nerdwallet.com/blog/average-credit-card-debt-household/
    #debt = {"cc":16061., "student":49042, "auto":28535}
    debt = {"cc":2000., "student":49042, "auto":12000}

    rate = {"cc":15.07, "student":6.8, "auto": 4.3}
    studentloanpayment = loan_monthlypayment(debt['student'], 10, rate['student'])
    autoloanpayment = loan_monthlypayment(debt['auto'], 5, rate['auto'])
    #ccrate - http://www.creditcards.com/credit-card-news/interest-rate-report-100114-up-2121.php
    #student loan rate - https://www.credible.com/blog/what-are-average-student-loan-interest-rates/
    #auto - 4.3%

    income0 = 50000 #at time = 0
    raisepercent = 3. #percentage raise per year
    taxes = 25. #percentage of income paid to taxes
    Emergency_FundMonths = 4
    inflation = 1.5#percent

    #expenses
    rice_beans = 150.*4.333 # dollars per week 
    
    

    #housing
    percent_housing = 25 #percentage of income paid to housing
    maxhousing = 1500#
    utils = 200#
    mortgage_interest = 4 #percent
    mortgage_value = 200000. #
    mortgage_downpayment = 0.2*mortgage_value
    loan_term = 15 #yrs
    loan_amount = (mortgage_value-mortgage_downpayment)
    monthly_payment = loan_amount * (mortgage_interest/100./12*(1.+mortgage_interest/100./12)**(loan_term*12))/((1.+mortgage_interest/100./12)**(loan_term*12)-1)
    home_taxes_insurance = 0.02 * mortgage_value/12. #monthly payment
    def loan_balance(month):
        return loan_amount*((1.+mortgage_interest/100./12)**(loan_term*12)-(1.+mortgage_interest/100./12)**(month) )/ ((1+mortgage_interest/100./12)**(loan_term*12)-1.)
    def equity_balance(month):
        ans = loan_amount - loan_balance(month) + mortgage_downpayment
        if ans > loan_amount + mortgage_downpayment:
            ans = loan_amount + mortgage_downpayment
        else:
            pass
        return ans
    #P = L[c(1 + c)n]/[(1 + c)n - 1]
    #B = L[(1 + c)n - (1 + c)p]/[(1 + c)n - 1]
    #https://www.mtgprofessor.com/formulas.htm
    #mortgage payment



    ## Retirement/Investment
    investment_return = 7. #percent
    capital_gains = 10 #percent
    retirement0 = 0.
    investments0 = 0. # how much do you have initally?
    company_match = 5. #percent
    percent_retirement = 15.
    amount_of_lifestyle_increase = 25. #25%
    #consider increasing cost of living over time


    #test parameters
    number_of_years = 10


    test = DaveRamsey()
    test.setup(debt, rate, income0, raisepercent, taxes, 
        Emergency_FundMonths, rice_beans, utils, percent_housing,  maxhousing,
        investment_return, capital_gains, retirement0, investments0, company_match, percent_retirement, amount_of_lifestyle_increase, inflation, 
        mortgage_value, mortgage_downpayment, mortgage_interest, loan_term, home_taxes_insurance)
    test.calc(number_of_years, retirement_match=False, pay_house_first=False)
    test.plot_wealth(1)


    test2 = DaveRamsey()
    test2.setup(debt, rate, income0, raisepercent, taxes, 
        Emergency_FundMonths, rice_beans, utils, percent_housing,  maxhousing,
        investment_return, capital_gains, retirement0, investments0, company_match, percent_retirement, amount_of_lifestyle_increase, inflation, 
        mortgage_value, mortgage_downpayment, mortgage_interest, loan_term, home_taxes_insurance)
    test2.calc(number_of_years, retirement_match=True, pay_house_first=False)
    test2.plot_wealth(2)
    ax = plt.gca()
    ylim = ax.get_axes().get_ylim()
    plt.figure(1)
    plt.gca().get_axes().set_ylim(ylim)
    



    plt.figure(3)
    plt.plot(test.months, test.case1['networth'], 'c-')
    plt.plot(test2.months, test2.case1['networth'], 'k-')
    plt.plot(test.months, test.case1['networth_taxed'], 'c--')
    plt.plot(test2.months, test2.case1['networth_taxed'], 'k--')
    plt.plot([0, max(test.months)], [0, 0], 'k-', lw=5)

    plt.figure(4)
    # plt.plot(test.months, (np.array(test2.case1['networth_taxed']) - np.array(test.case1['networth_taxed'])), 'k-')
    plt.plot(test.months[:-1], (np.diff(test2.case1['networth'])), 'k-')
    plt.plot(test.months[:-1], (np.diff(test.case1['networth'])), 'c-')
    plt.xlabel('months')
    plt.ylabel(r'Difference in Taxed Net Worth')

    #Computethe degree of gazelle intensity required to reach zero net worth at the 
    #same month as if you had invested the $$$
    

    test3 = DaveRamsey()
    test3.setup(debt, rate, income0, raisepercent, taxes, 
        Emergency_FundMonths, rice_beans, utils, percent_housing,  maxhousing,
        investment_return, capital_gains, retirement0, investments0, company_match, percent_retirement, amount_of_lifestyle_increase, inflation, 
        mortgage_value, mortgage_downpayment, mortgage_interest, loan_term, home_taxes_insurance)
    test3.calc(number_of_years, retirement_match=False, pay_house_first=False)

    company_matches = np.arange(0,11,1)
    frac_rice_beans = []
    months_zero_taxed_networth_with_match = []
    months_debt_free_with_match = []
    month_zero_taxed_networth_nomatch = test.month_networth_taxed_pos
    total_expenses_nomatch = []
    total_expenses_match = []
    end_time_networth_taxed_withmatch = []
    end_time_networth_taxed_nomatch = []
    for i in range(len(company_matches)):
        test2.company_match = company_matches[i]
        test2.calc(number_of_years, retirement_match=True, pay_house_first=False, verbose=False)
        test.company_match = company_matches[i]
        test.calc(number_of_years, retirement_match=False, pay_house_first=False, verbose=False)
        end_time_networth_taxed_nomatch.append(test.case1['networth_taxed'][-1])
        months_zero_taxed_networth_with_match.append(test2.month_networth_taxed_pos)
        months_debt_free_with_match.append(test2.month_debt_free)
        end_time_networth_taxed_withmatch.append(test2.case1['networth_taxed'][-1])
        bleh = test3.adjust_var_to_zero_networth_taxed('rice_beans', test2.month_networth_taxed_pos)
        frac_rice_beans.append(bleh)
        total_expenses_nomatch.append(test3.case1['expenses'][0])
        total_expenses_match.append(test2.case1['expenses'][0])
        print  company_matches[i], bleh, test2.month_networth_taxed_pos
    test.company_match = company_match
    test.calc(number_of_years, retirement_match=False, pay_house_first=False, verbose=False)
    plt.figure(6)
    l1 = plt.plot(company_matches, [test.month_networth_taxed_pos]*len(company_matches), 'co-')[0]
    l2 = plt.plot(company_matches, months_zero_taxed_networth_with_match, 'ko-')[0]
    l3 = plt.plot(company_matches, months_debt_free_with_match, 'ko-', mfc='None')[0]
    plt.axis([0, max(company_matches), 0, 1.1*max(months_debt_free_with_match)])

    #plt.annotate('With Company Match - net worth taxed positive', (4, .9*months_zero_taxed_networth_with_match[-1]), size=6)
    #plt.annotate('With Company Match - debt free', (6, .8*months_debt_free_with_match[-1]), size=6)
    #plt.annotate('Without Company Match', (4, .95*test.month_networth_taxed_pos), size=6, color=l1.get_color())
    plt.xlabel('% 401K Match')
    plt.ylabel('Months')


    plt.figure(5)
    plt.plot(company_matches, total_expenses_match, 'ko-')
    l2 = plt.plot(company_matches, total_expenses_nomatch, 'co-')[0]
    plt.xlabel('% 401K Match')
    plt.ylabel('Total Expenses')
    plt.title('Expenses Reduction Required For Zero Net Worth @ Same Month', size=8)
    plt.axis([0, max(company_matches), 0, max(total_expenses_match)*1.1])
    #plt.annotate('With Company Match', (4, 1.025*total_expenses_match[0]), size=10)
    #plt.annotate('Without Company Match', (4, .95*total_expenses_nomatch[-1]), size=10, color=l2.get_color())
    #expenses to income ratio - or just raw expenses. (may want to include)

    plt.figure(7)
    plt.plot(company_matches, end_time_networth_taxed_withmatch, 'ko-')
    l2 = plt.plot(company_matches, end_time_networth_taxed_nomatch, 'co-')[0]
    plt.xlabel('% 401K Match')
    plt.ylabel('%i Yr Net Worth' % (number_of_years))
    plt.axis([0, max(company_matches), 0, 1.2*max(end_time_networth_taxed_withmatch)])
    


    zach.exportpdffigs('ramsey_test5.pdf')
    #debt to income ratio



    # import scipy.optimize as opt
    # var_to_adjust = 'rice_beans'
    # month_to_set = test2.month_networth_taxed_pos
    # def optfun(frac):
    #     test3 = DaveRamsey()
    #     test3.setup(debt, rate, income0, raisepercent, taxes, 
    #     Emergency_FundMonths, rice_beans, utils, percent_housing,  maxhousing,
    #     investment_return, capital_gains, retirement0, investments0, company_match, percent_retirement, amount_of_lifestyle_increase, inflation, 
    #     mortgage_value, mortgage_downpayment, mortgage_interest, loan_term, home_taxes_insurance)
    #     setattr(test3, var_to_adjust, getattr(test3, var_to_adjust)*frac)
    #     test3.calc(number_of_years, retirement_match=False, pay_house_first=True)
    #     return test3.month_networth_taxed_pos- month_to_set
    # a = np.arange(0, .99, .01).tolist()
    # a.reverse()
    # solution = -1
    # for i in a:
    #     ans = optfun(i)
    #     if ans > 0:
    #         pass
    #     else:
    #         solution = i
    #     if solution > -1:
    #         break
    # if solution == -1:
    #     print "no way to reduce rice and beans enough"





############# Sort out tax issues w/ retirement and company match... it seems that I'm using income, which isn't taxed. But then i'm taking after tax $$!
############# 
    ### Time to debt free?
        #as a function of total debt/income ratio?
    ### Time to 0 net worth
        #as a function of?
    ### Time to $1 mill? Time to 2 mill?

    ### Additional monthly income you could have had? Or, the larger house you could have bought?, etc.


# Tornado plot/sensitivity analysis on some stuff, monte carlo on investment return?
#####################Plots - different debts over time
#####################Tables - debt pay off time for different cases, 
#####################   Net worth after # of yearstopay
#####################   Total interest paid, total investment income, total mortgage balance



### Dave's time to complete baby step 2 - pay off debts?
### dave has said on several occasions that you don't want to spend
### more than 2 or 3 years in this step
### Other considerations - Investing now vs. Investing later?
### Quantifying Risk - varying?
### Quantifying Gazelle Intensity vs. slugishness?
### Quantifying time to zero net worth?
### Quantifying interest paid vs interest earned
### people with spending problems?
### Quantifying the suggestion to not put $$ into 401K to get match
### Quantifying housing cost and wealth distribution
### NEXT - needs to put into class form and add the ability to change the order! (do retirement investment during debt payoff?)


### Monte Carlo for certain factors - amount of debt, income
### credit card vs other debt? Assumed investment interest rate?
### 401K matching %?





    ### Case 1 ###
    #Dave Ramsey Method - Rice and Beans
    # case1 = {'debt':{"cc":[], "student":[], "auto":[]}, 'savings':[], 'investments':[], 'retirement':[], 'mortgage':[], "rent":[], "income":[], "expenses":[], "networth":[]}
    # #case1_
    # case1['retirement'].append(retirement0)
    # case1['investments'].append(investments0)

    # for i in range(number_of_years*12):
    #     if i==0:
    #         case1["income"].append(income0)
    #     elif i%12==0:
    #         case1['income'].append(case1['income'][i-1]*(1+raisepercent/100.))
    #     else:
    #         case1['income'].append(case1['income'][i-1])
    #     #payments out
    #     case1["rent"].append(np.min([(1.-taxes/100.)*case1['income'][i]/12*percent_housing/100, maxhousing]))
    #     if i== 0:
    #         case1['mortgage'].append(0.)
    #         case1["expenses"].append((rice_beans + case1["rent"][i]+utils)*(1+inflation/100.)**(i/12.))
    #     elif np.sum([j[-1] for j in case1['debt'].values()])>0:
    #         case1['mortgage'].append(case1['mortgage'][i-1])
    #         if case1['mortgage'][i-1]>0.:
    #             if case1['mortgage'][i-1] == mortgage_downpayment+loan_amount:
    #                 case1['rent'].append(0.)
    #             else:
    #                 case1['rent'].append(monthly_payment+home_taxes_insurance)
    #         case1["expenses"].append((rice_beans + case1["rent"][i]+utils)*(1+inflation/100.)**(i/12.))
    #     else:
    #        case1['mortgage'].append(case1['mortgage'][i-1])
    #        if case1['mortgage'][i-1]>0.:
    #             if case1['mortgage'][i-1] == mortgage_downpayment+loan_amount:
    #                 case1['rent'].append(0.)
    #             else:
    #                 case1['rent'].append(monthly_payment+home_taxes_insurance)
    #        case1['expenses'].append((rice_beans*(1.+amount_of_lifestyle_increase/100) + case1["rent"][i]+utils)*(1+inflation/100.)**(i/12.))
    #     #Baby Step 1: Save $1000
    #         #assume this is done already
    #     #Baby Step 2: Debts
    #     totaldebtpaid = 0
    #     extra_money = 0
    #     ################# Pay Debts - minimum payments on debt
    #     for (j,k) in case1['debt'].items():
    #             if j=='cc':
    #                 if i>0:
    #                     if case1['debt'][j][i-1]>0:
    #                         paydebt = cc_minpayment(case1["debt"]['cc'][-1], rate['cc'], 1.0)
    #                     else:
    #                         paydebt = 0
    #                 else:
    #                     if debt[j]>0:
    #                         paydebt = cc_minpayment(debt['cc'], rate['cc'], 1.0)
    #                     else:
    #                         paydebt = 0
    #             elif j=='student':
    #                 if i>0:
    #                     if case1['debt'][j][i-1]>0:
    #                         paydebt = studentloanpayment
    #                     else:
    #                         paydebt = 0
    #                 else:
    #                     if debt[j]>0:
    #                         paydebt = studentloanpayment
    #                     else:
    #                         paydebt = 0
    #             elif j=='auto':
    #                 if i>0:
    #                     if case1['debt'][j][i-1]>0:
    #                         paydebt = autoloanpayment
    #                     else:
    #                         paydebt = 0
    #                 else:
    #                     if debt[j]>0:
    #                         paydebt = autoloanpayment
    #                     else:
    #                         paydebt = 0
    #             if i==0:
    #                 case1['debt'][j].append(debt[j]*(1.+rate[j]/100./12.)-paydebt)    
    #             else:
    #                 case1['debt'][j].append(case1['debt'][j][i-1]*(1.+rate[j]/100./12.)-paydebt)
    #             totaldebtpaid = totaldebtpaid + paydebt 
    #             if case1['debt'][j][i] < 0:
    #                 extra_money = extra_money + -1*case1['debt'][j][i]
    #                 totaldebtpaid = totaldebtpaid + extra_money
    #     #pdb.set_trace()
    #     if i==0:
    #         whichone_debt = whichone_debtfun(case1, i)
    #     elif not np.isnan(min_ignorezero([case1['debt']['cc'][i-1], case1['debt']['student'][i-1], case1['debt']['auto'][i-1]])):
    #         whichone_debt = whichone_debtfun(case1, i-1)
    #     else:
    #         whichone_debt = 10000
    #     if i>=0:
    #         for (j,k) in case1['debt'].items():
    #             if whichone_debt==j:
                    
    #                 paydebt = case1['income'][i]/12*(1.-taxes/100.)-case1['expenses'][i] - totaldebtpaid
    #                 case1['debt'][j][i] = case1['debt'][j][i] - paydebt
    #                 totaldebtpaid = totaldebtpaid + paydebt 
    #             else:
    #                 paydebt = 0.
    #                 case1['debt'][j][i] = case1['debt'][j][i] - paydebt
    #             if case1['debt'][j][i] < 0:
    #                 extra_money = extra_money + -1*case1['debt'][j][i]
    #                 case1['debt'][j][i] = 0

    #         if extra_money >0:
    #             if not np.isnan(min_ignorezero([case1['debt']['cc'][i], case1['debt']['student'][i], case1['debt']['auto'][i]])):
    #                 whichone_debt = whichone_debtfun(case1, i)
    #                 paydebt = extra_money
    #                 case1['debt'][whichone_debt][i] = case1['debt'][whichone_debt][i] - extra_money
    #                 extra_money = 0
    #             if case1['debt'][whichone_debt][i]<0:
    #                 print "I hope this never happens!", extra_money, case1['debt'][whichone_debt][i]
    #     #Baby Step 3 - 3-6 months of expenses
    #     #Baby Step 3b - save up a down payment, mortgage?

    #     #Baby Step 4 - 15% of your income into retirement
    #     #baby step 5 - College Retirement
    #     #Baby Step 6 - Pay off House
    #     #Baby Step 7 - give
    #     #
    #     if i==0:
    #         case1["savings"].append(1000.) #assume $1000 emergency fund in place already
    #         case1['networth'].append(case1['savings'][i] + -1*(case1["debt"]["cc"][i]+case1["debt"]["student"][i] + case1["debt"]["auto"][i]))
    #     else:
    #         #case1["retirement"].append(0.15*case1["income"][i]+match)
    #         months_extra_money = case1['income'][i]*(1.-taxes/100.)/12-case1['expenses'][i] - totaldebtpaid + extra_money
            
    #         if case1["savings"][i-1] < Emergency_FundMonths*(case1['expenses'][i] + totaldebtpaid):
    #             case1["savings"].append(case1['savings'][i-1] + np.min([months_extra_money, Emergency_FundMonths*(case1['expenses'][i] + totaldebtpaid) - case1['savings'][i-1] ] ))
    #             #months_extra_money0=months_extra_money
    #             months_extra_money = months_extra_money - (case1['savings'][i] - case1['savings'][i-1])
    #             #print months_extra_money0, months_extra_money#extra income goes to retirement
    #             #val = np.min([case1["savings"][i] - Emergency_FundMonths*(case1['expenses'][i] + totaldebtpaid), percent_retirement*case1['income'][i]])
    #         else:
    #             case1['savings'].append(case1['savings'][i-1])
            
    #         if months_extra_money>0.01 and case1['mortgage'][i]==0:
    #             #baby step 3b - save for down payment
    #             if case1["savings"][i] < (Emergency_FundMonths*(case1['expenses'][i] + totaldebtpaid) + mortgage_downpayment ):
    #                 #if you haven't saved enough for the down payment, then put it in the account!
    #                 prev = case1['savings'][i]

    #                 case1['savings'][i] = case1['savings'][i] + np.min([months_extra_money,Emergency_FundMonths*(case1['expenses'][i] + totaldebtpaid) + mortgage_downpayment - case1['savings'][i]])
    #                 #prev2 = copy.deepcopy(months_extra_money)
    #                 months_extra_money = months_extra_money - (case1['savings'][i]-prev)
    #                 #print months_extra_money
    #                 #print i,prev, case1['savings'][i], np.min([prev2,Emergency_FundMonths*(case1['expenses'][i] + totaldebtpaid) + mortgage_downpayment - case1['savings'][i]]), Emergency_FundMonths*(case1['expenses'][i] + totaldebtpaid) + mortgage_downpayment
    #                 if months_extra_money>0.01: 
    #                     #purchase the house
    #                     print 'bought the house with %g down, %i yr term, %g pct: interest rate at month: %i'%(mortgage_downpayment,loan_term, mortgage_interest, i)
    #                     mortgage_startdate = i
    #                     case1['mortgage'][i] = mortgage_downpayment
    #                     case1['savings'][i] = case1['savings'][i] - mortgage_downpayment
    #         elif case1['mortgage'][i] > 0:
    #             #### Cost of the mortgage already came out in the expenses portion. This is to tabulate the equity in the home
    #             interest_paid = (mortgage_interest/100./12) * (mortgage_value- case1['mortgage'][i-1])
    #             ans = case1['mortgage'][i-1] +  monthly_payment - interest_paid# equity_balance(i - mortgage_startdate) #already calculated this!
    #             if ans > loan_amount + mortgage_downpayment:
    #                 ans = loan_amount + mortgage_downpayment
    #             case1['mortgage'][i] = ans#case1['mortgage'][i-1] +  monthly_payment - interest_paid# equity_balance(i - mortgage_startdate) #already calculated this!
    #             #could calculate mortgage interest paid if I wanted to?
    #         if months_extra_money>0:
    #             if months_extra_money / case1['income'][i]*12*100 > percent_retirement:
    #                 case1['retirement'].append(case1['retirement'][i-1]*(1+investment_return/100./12.)+ (percent_retirement/100. + company_match/100.)*case1['income'][i]/12.)
    #                 months_extra_money = months_extra_money - percent_retirement/100. * case1['income'][i]/12
    #                 #these are post-tax investments, correct?
    #             else:
    #                 case1['retirement'].append(case1['retirement'][i-1]*(1+investment_return/100./12.)+months_extra_money)
    #                 months_extra_money =  0.
    #         else:
    #             case1['retirement'].append(case1['retirement'][i-1]*(1+investment_return/100./12.))
    #         #case1['savings'][i] = case1['savings'][i] + 
            
    #         ##### Save for a house? Either after 3-6 months or 
    #         if months_extra_money>0:
    #             # if there's still $$ after retirement, dump money into the house!
    #             # 
    #             if case1['mortgage'][i] < mortgage_value:
    #                 case1['mortgage'][i] = case1['mortgage'][i] + months_extra_money
    #                 months_extra_money = 0.
    #             else:
    #                 pass
    #         if months_extra_money>0.01:
    #                 case1['investments'].append(case1['investments'][i-1]*(1.+(1.-taxes/100.)*investment_return/100./12.)+months_extra_money)
    #         else:
    #             case1['investments'].append(case1['investments'][i-1]*(1.+(1.-taxes/100.)*investment_return/100./12.))
    #             #taxable investment accounts
    #         months_extra_money = months_extra_money - case1['investments'][i] - case1['investments'][i-1]

    #         if months_extra_money>0:
    #             case1['savings'][i] = case1['savings'][i]+ months_extra_money


    #         #print val / case1['income'][i]*12*100,"%"
            
    #         case1["networth"].append(case1['investments'][i] + case1['retirement'][i] + case1['savings'][i] +case1['mortgage'][i]+ -1*(case1["debt"]["cc"][i]+case1["debt"]["student"][i] + case1["debt"]["auto"][i]) )
    #     ###### ADD Interest paid monthly calculator
    #     ###### Sensitivity of monthly expenses?
    #     months = np.arange(number_of_years*12)


    # plt.figure(2)
    # plt.plot(months, case1['networth'], 'k-', lw=3)
    # plt.plot(months, np.zeros(len(months)), 'k:', lw=1)
    # plt.fill_between(months, -1.*(np.array(case1['debt']['cc'])+ np.array(case1['debt']['student'])+np.array(case1['debt']['auto'])), color='r',alpha=1, lw=3)
    # plt.fill_between(months, np.array(case1['retirement'])+np.array(case1['investments'])+np.array(case1['savings'])+np.array(case1['mortgage']), np.array(case1['retirement'])+np.array(case1['mortgage'])+np.array(case1['savings']), color='b', lw=3)
    # plt.fill_between(months, np.array(case1['retirement'])+np.array(case1['savings'])+np.array(case1['mortgage']), np.array(case1['savings'])+np.array(case1['mortgage']),color='g',lw=3, alpha=1)
    # plt.fill_between(months, np.array(case1['savings'])+np.array(case1['mortgage']), case1['savings'], color='c', lw=3, alpha=1)
    # plt.fill_between(months, case1['savings'], np.zeros(len(months)), color='m', lw=3, alpha=1)

    ### Case 2 ### - Avalanche Method, investing as you go


plt.show()

class RedditPF():
    def __init__(self):
        pass#self.debt = {'cc': 0., 'student': 0., 'auto':0.}
        #self.

    def setup(self, debt, rate, income0, raisepercent, taxes, 
        Emergency_FundMonths, rice_beans, utils, percent_housing,  maxhousing, 
        investment_return, retirement0, investments0, company_match, percent_retirement, amount_of_lifestyle_increase, inflation,
        mortgage_value, mortgage_downpayment, mortgage_interest, loan_term, home_taxes_insurance):
        self.debt = debt
        self.rate = rate
        self.income0 = income0
        self.raisepercent = raisepercent
        self.taxes = taxes
        self.Emergency_FundMonths = Emergency_FundMonths
        self.rice_beans = rice_beans
        self.utils = utils
        self.percent_housing = percent_housing
        self.maxhousing = maxhousing
        self.investment_return = investment_return
        self.retirement0 = retirement0
        self.investments0 = investments0
        self.company_match = company_match
        self.percent_retirement = percent_retirement
        self.amount_of_lifestyle_increase = amount_of_lifestyle_increase
        self.inflation = inflation
        self.mortgage_value = mortgage_value# = 200000. #
        self.mortgage_downpayment = mortgage_downpayment# = 0.2*mortgage_value
        self.mortgage_interest = mortgage_interest
        self.loan_term = loan_term# = 30.0 #yrs
        self.loan_amount = (mortgage_value-mortgage_downpayment)
        self.monthly_payment = loan_amount * (mortgage_interest/100./12*(1.+mortgage_interest/100./12)**(loan_term*12))/((1.+mortgage_interest/100./12)**(loan_term*12)-1)
        self.home_taxes_insurance = home_taxes_insurance #= 0.02 * mortgage_value/12. #monthly payment

        #Average - 16,061$ cc debt, $49042 - Student Loan, $28535 auto
        #https://www.nerdwallet.com/blog/average-credit-card-debt-household/
        #debt = {"cc":16061., "student":49042, "auto":28535}

        #rate = {"cc":15.07, "student":6.8, "auto": 4.3}
        self.studentloanpayment = loan_monthlypayment(debt['student'], 10, rate['student'])
        self.autoloanpayment = loan_monthlypayment(debt['auto'], 5, rate['auto'])
        #ccrate - http://www.creditcards.com/credit-card-news/interest-rate-report-100114-up-2121.php
        #student loan rate - https://www.credible.com/blog/what-are-average-student-loan-interest-rates/
        #auto - 4.3%
    def calc(self, number_of_years):
        self.number_of_years = number_of_years
        self.case1 = {'debt':{"cc":[], "student":[], "auto":[]}, 'savings':[], 'investments':[], 'retirement':[], 'mortgage':[], "rent":[], "income":[], "expenses":[], "networth":[]}
        #case1_
        self.case1['retirement'].append(self.retirement0)
        self.case1['investments'].append(self.investments0)


        for i in range(number_of_years*12):
            if i==0:
                self.case1["income"].append(self.income0)
            elif i%12==0:
                self.case1['income'].append(self.case1['income'][i-1]*(1+self.raisepercent/100.))
            else:
                self.case1['income'].append(self.case1['income'][i-1])
            #payments out
            self.case1["rent"].append(np.min([(1.-self.taxes/100.)*self.case1['income'][i]/12*self.percent_housing/100, self.maxhousing]))
            if i== 0:
                self.case1['mortgage'].append(0.)
                self.case1["expenses"].append((self.rice_beans + self.case1["rent"][i]+self.utils)*(1+self.inflation/100.)**(i/12.))
            elif np.sum([j[-1] for j in self.case1['debt'].values()])>0:
                self.case1['mortgage'].append(self.case1['mortgage'][i-1])
                if self.case1['mortgage'][i-1]>0.:
                    if self.case1['mortgage'][i-1] == self.mortgage_downpayment+self.loan_amount:
                        self.case1['rent'].append(0.)
                    else:
                        self.case1['rent'].append(self.monthly_payment+self.home_taxes_insurance)
                self.case1["expenses"].append((self.rice_beans + self.case1["rent"][i]+self.utils)*(1.+self.inflation/100.)**(i/12.))
            else:
               self.case1['mortgage'].append(self.case1['mortgage'][i-1])
               if self.case1['mortgage'][i-1]>0.:
                    if self.case1['mortgage'][i-1] == self.mortgage_downpayment+self.loan_amount:
                        self.case1['rent'].append(0.)
                    else:
                        self.case1['rent'].append(self.monthly_payment+self.home_taxes_insurance)
               self.case1['expenses'].append((self.rice_beans*(1.+self.amount_of_lifestyle_increase/100) + self.case1["rent"][i]+self.utils)*(1+self.inflation/100.)**(i/12.))
            #Baby Step 1: Save $1000
                #assume this is done already
            #Baby Step 2: Debts
            totaldebtpaid = 0
            extra_money = 0
            ################# Pay Debts - minimum payments on debt
            for (j,k) in self.case1['debt'].items():
                    if j=='cc':
                        if i>0:
                            if self.case1['debt'][j][i-1]>0:
                                paydebt = cc_minpayment(self.case1['debt']['cc'][-1], self.rate['cc'], 1.0)
                            else:
                                paydebt = 0
                        else:
                            if debt[j]>0:
                                paydebt = cc_minpayment(self.debt['cc'], self.rate['cc'], 1.0)
                            else:
                                paydebt = 0
                    elif j=='student':
                        if i>0:
                            if self.case1['debt'][j][i-1]>0:
                                paydebt = self.studentloanpayment
                            else:
                                paydebt = 0
                        else:
                            if debt[j]>0:
                                paydebt = self.studentloanpayment
                            else:
                                paydebt = 0
                    elif j=='auto':
                        if i>0:
                            if self.case1['debt'][j][i-1]>0:
                                paydebt = self.autoloanpayment
                            else:
                                paydebt = 0
                        else:
                            if debt[j]>0:
                                paydebt = self.autoloanpayment
                            else:
                                paydebt = 0
                    if i==0:
                        #print self.case1['debt']
                        self.case1['debt'][j].append(self.debt[j]*(1.+self.rate[j]/100./12.)-paydebt)    
                    else:
                        self.case1['debt'][j].append(self.case1['debt'][j][i-1]*(1.+self.rate[j]/100./12.)-paydebt)
                    totaldebtpaid = totaldebtpaid + paydebt 
                    if self.case1['debt'][j][i] < 0:
                        extra_money = extra_money + -1*self.case1['debt'][j][i]
                        totaldebtpaid = totaldebtpaid + extra_money
            #pdb.set_trace()    
            ###########Pay to get retirement match
            print totaldebtpaid, extra_money, case1
            months_extra_money = extra_money
            if months_extra_money>0:
                    if months_extra_money / self.case1['income'][i]*12*100 > self.percent_retirement:
                        self.case1['retirement'].append(self.case1['retirement'][i-1]*(1+self.investment_return/100./12.)+ (2 * self.company_match/100.)*self.case1['income'][i]/12.)
                        months_extra_money = months_extra_money - self.company_match/100. * self.case1['income'][i]/12
                        #these are post-tax investments, correct?
                    else:
                        self.case1['retirement'].append(self.case1['retirement'][i-1]*(1.+self.investment_return/100./12.)+months_extra_money)
                        months_extra_money =  0.
            else:
                self.case1['retirement'].append(self.case1['retirement'][i-1]*(1.+self.investment_return/100./12.))



            ############# Pay off higher interest rate debt (>10%); 
            if months_extra_money>0:
                if self.case1['debt']['cc'][i] > 0:
                    paydebt = months_extra_money
                    self.case1['debt']['cc'][i] = self.case1['debt']['cc'][i] - paydebt
                    months_extra_money = 0.
                if self.case1['debt']['cc'][i] < 0:
                    months_extra_money = months_extra_money + -1*self.case1['debt'][j][i]
                    self.case1['debt']['cc'][i] = 0
            

            ################# 3 months expenses! emergency fund
            if i==0:
                self.case1["savings"].append(1000.) #assume $1000 emergency fund in place already
                self.case1['networth'].append(self.case1['savings'][i] + -1*(self.case1["debt"]["cc"][i]+self.case1["debt"]["student"][i] + self.case1["debt"]["auto"][i]))
            else:
                #self.case1["retirement"].append(0.15*self.case1["income"][i]+match)
                months_extra_money = self.case1['income'][i]*(1.-self.taxes/100.)/12-self.case1['expenses'][i] - totaldebtpaid + extra_money
                
                if self.case1["savings"][i-1] < self.Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid):
                    self.case1["savings"].append(self.case1['savings'][i-1] + np.min([months_extra_money, self.Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid) - self.case1['savings'][i-1] ] ))
                    #months_extra_money0=months_extra_money
                    months_extra_money = months_extra_money - (self.case1['savings'][i] - self.case1['savings'][i-1])
                    #print months_extra_money0, months_extra_money#extra income goes to retirement
                    #val = np.min([self.case1["savings"][i] - Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid), percent_retirement*self.case1['income'][i]])
                else:
                    self.case1['savings'].append(self.case1['savings'][i-1])

            ############# By the book it says to pay off >5% debt, which would include student loans


            ########### /r/personalfinance
            #according to reddit flow chart:

            #pay off utils, housing etc. 
            # First, save 1000 emergency fund.
            #minimum payments on debts
            # Contribute to employer matching 401K funds to the match
            # Pay off high interest (>10%, i.e., credit cards)
            # 3-6 month emergency fund
            # pay off moderate interest rate debts. (4-5%, would be higher than my car?)
            # save for near term (house down payment, college, new car to get to work)
            # contribute up to 15% to retirement
            # max out HSA
            # child college savings
            # Step 6: additional to taxable investments/House/retire early
########### Retirement 401K Match



                
                if months_extra_money>0.01 and self.case1['mortgage'][i]==0:
                    #baby step 3b - save for down payment
                    if self.case1["savings"][i] < (self.Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid) + self.mortgage_downpayment ):
                        #if you haven't saved enough for the down payment, then put it in the account!
                        prev = self.case1['savings'][i]

                        self.case1['savings'][i] = self.case1['savings'][i] + np.min([months_extra_money,self.Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid) + self.mortgage_downpayment - self.case1['savings'][i]])
                        #prev2 = copy.deepcopy(months_extra_money)
                        months_extra_money = months_extra_money - (self.case1['savings'][i]-prev)
                        #print months_extra_money
                        #print i,prev, self.case1['savings'][i], np.min([prev2,Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid) + mortgage_downpayment - self.case1['savings'][i]]), Emergency_FundMonths*(self.case1['expenses'][i] + totaldebtpaid) + mortgage_downpayment
                        if months_extra_money>0.01: 
                            #purchase the house
                            print 'bought the house with %g down, %i yr term, %g pct: interest rate at month: %i'%(mortgage_downpayment,loan_term, mortgage_interest, i)
                            self.mortgage_startdate = i
                            self.case1['mortgage'][i] = self.mortgage_downpayment
                            self.case1['savings'][i] = self.case1['savings'][i] - self.mortgage_downpayment
                elif self.case1['mortgage'][i] > 0:
                    #### Cost of the mortgage already came out in the expenses portion. This is to tabulate the equity in the home
                    interest_paid = (self.mortgage_interest/100./12) * (self.mortgage_value- self.case1['mortgage'][i-1])
                    ans = self.case1['mortgage'][i-1] +  self.monthly_payment - interest_paid# equity_balance(i - mortgage_startdate) #already calculated this!
                    if ans > self.loan_amount + self.mortgage_downpayment:
                        ans = self.loan_amount + self.mortgage_downpayment
                    self.case1['mortgage'][i] = ans#self.case1['mortgage'][i-1] +  monthly_payment - interest_paid# equity_balance(i - mortgage_startdate) #already calculated this!
                    #could calculate mortgage interest paid if I wanted to?
                if months_extra_money>0:
                    if months_extra_money / self.case1['income'][i]*12*100 > self.percent_retirement:
                        self.case1['retirement'].append(self.case1['retirement'][i-1]*(1+self.investment_return/100./12.)+ (self.percent_retirement/100. + self.company_match/100.)*self.case1['income'][i]/12.)
                        months_extra_money = months_extra_money - self.percent_retirement/100. * self.case1['income'][i]/12
                        #these are post-tax investments, correct?
                    else:
                        self.case1['retirement'].append(self.case1['retirement'][i-1]*(1.+self.investment_return/100./12.)+months_extra_money)
                        months_extra_money =  0.
                else:
                    self.case1['retirement'].append(self.case1['retirement'][i-1]*(1.+self.investment_return/100./12.))
                #self.case1['savings'][i] = self.case1['savings'][i] + 
                
                ##### Save for a house? Either after 3-6 months or 
                if months_extra_money>0:
                    # if there's still $$ after retirement, dump money into the house!
                    # 
                    if self.case1['mortgage'][i] < mortgage_value:
                        self.case1['mortgage'][i] = self.case1['mortgage'][i] + months_extra_money
                        months_extra_money = 0.
                    else:
                        pass
                if months_extra_money>0.01:
                        self.case1['investments'].append(self.case1['investments'][i-1]*(1.+(1.-self.taxes/100.)*self.investment_return/100./12.)+months_extra_money)
                else:
                    self.case1['investments'].append(self.case1['investments'][i-1]*(1.+(1.-taxes/100.)*investment_return/100./12.))
                    #taxable investment accounts
                months_extra_money = months_extra_money - self.case1['investments'][i] - self.case1['investments'][i-1]

                if months_extra_money>0:
                    self.case1['savings'][i] = self.case1['savings'][i]+ months_extra_money


                #print val / self.case1['income'][i]*12*100,"%"
                
                self.case1["networth"].append(self.case1['investments'][i] + self.case1['retirement'][i] + self.case1['savings'][i] +self.case1['mortgage'][i]+ -1*(self.case1["debt"]["cc"][i]+self.case1["debt"]["student"][i] + self.case1["debt"]["auto"][i]) )
            ###### ADD Interest paid monthly calculator
            ###### Sensitivity of monthly expenses?
            self.months = np.arange(self.number_of_years*12)

    def plot_wealth(self,fignum):
        
        plt.figure(fignum)
        plt.plot(self.months, self.case1['networth'], 'k-', lw=3)
        plt.plot(self.months, np.zeros(len(self.months)), 'k:', lw=1)
        plt.fill_between(self.months, -1.*(np.array(self.case1['debt']['cc'])+ np.array(self.case1['debt']['student'])+np.array(self.case1['debt']['auto'])), color='r',alpha=1, lw=3)
        plt.fill_between(self.months, np.array(self.case1['retirement'])+np.array(self.case1['investments'])+np.array(self.case1['savings'])+np.array(self.case1['mortgage']), np.array(self.case1['retirement'])+np.array(self.case1['mortgage'])+np.array(self.case1['savings']), color='b', lw=3)
        plt.fill_between(self.months, np.array(self.case1['retirement'])+np.array(self.case1['savings'])+np.array(self.case1['mortgage']), np.array(self.case1['savings'])+np.array(self.case1['mortgage']),color='g',lw=3, alpha=1)
        plt.fill_between(self.months, np.array(self.case1['savings'])+np.array(self.case1['mortgage']), self.case1['savings'], color='c', lw=3, alpha=1)
        plt.fill_between(self.months, self.case1['savings'], np.zeros(len(self.months)), color='m', lw=3, alpha=1)
        plt.xlabel('months')
        plt.ylabel('wealth')