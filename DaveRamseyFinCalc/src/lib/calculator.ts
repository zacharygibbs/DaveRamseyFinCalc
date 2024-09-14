import { DEFAULT_TAX_RATE } from './config';
import type { CalculatorResults } from './interfaces';

/*
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
*/

export const Income = class {
	gross_income: number;
	tax_percent: number;
	raise_percent: number;
	constructor(
		gross_income: number,
		tax_percent: number,
		raise_perent: number,
		retirement_match: number
	) {
		self.gross_income = gross_income;
		self.tax_percent = tax_percent;
		self.raise_percent = raise_perent;
		self.retirement_match = retirement_match;
	}
};

export const Calculator = class {
	debt_list: (typeof Debt)[];
	asset_list: (typeof Asset)[];
	results: CalculatorResults[];

	constructor(debt_list: (typeof Debt)[], asset_list: (typeof Asset)[]) {
		this.debt_list = debt_list;
		this.asset_list = asset_list;
		this.results = {
			t: [],
			debts: [],
			assets_debt_secured: [],
			assets: []
		};
		this.append_results();
	}

	append_results = () => {
		this.results.t.push(this.results.t.length); // if Zero, push 1, .. always pushes next value
		this.results.debts.push({
			total: this.debt_list.reduce((total, debt) => {
				return total + debt.value;
			}, 0)
			/// tack on aggregated by "type" ? as well?
		});
		this.results.assets_debt_secured.push({
			total: this.debt_list.reduce((total, debt) => {
				return total + (debt.asset == null ? 0 : debt.asset.value);
			}, 0)
			/// tack on aggregated by "type" ? as well?
		});
		this.results.assets.push({
			total: this.asset_list.reduce((total, asset) => {
				return total + asset.value;
			}, 0)
		});
	};

	forward() {
		this.debt_list.forEach((debt) => {
			debt.forward();
		});

		this.asset_list.forEach((asset) => {
			asset.forward();
		});
		this.append_results();
	}
};

export const Asset = class {
	// like your car..
	type: string; // car, real_estate, house?..."roth", "pretax", "taxable", null..
	rate: number; // can be positive or negative; negative meaning depreciation
	value: number;
	operating_cost: number; //monthly cost if applicable (insurance taxes etc?)
	constructor(type: string, rate: number, value: number, operating_cost: number) {
		this.type = type;
		this.rate = rate;
		this.value = value;
		this.operating_cost = operating_cost;
	}

	get_interest = () => {
		return (this.value * this.rate) / 12; //monthly..
	};

	get_payment = () => {
		return this.operating_cost;
	};

	get_post_tax_value = (tax_rate: number | null = null) => {
		tax_rate = tax_rate == null ? DEFAULT_TAX_RATE : tax_rate;
		if (this.type == 'pretax' || this.type == 'taxable') {
			return this.value * (1 - tax_rate);
		} else {
			return this.value;
		}
	};

	pay = () => {
		let a = 1;
	}; // since operating cost, won't actually do anything to the value..

	apply_interest = () => {
		this.value += this.get_interest();
	};

	forward = () => {
		//positive = more debt..
		this.apply_interest();
		this.pay();
	};
};

export const Debt = class {
	type: string; // cc, auto, student, ...
	rate: number; // interest rate monthly %
	value: number; // how much debt at a given time step
	min_payment: number; // how much you are required to pay
	asset: typeof Asset | null;
	constructor(
		type: string = 'cc',
		rate: number = 0.25,
		value: number = 0,
		min_payment: number = 0,
		asset: typeof Asset | null
	) {
		this.type = type;
		this.rate = rate; // APR
		this.value = value;
		this.min_payment = min_payment; // ignored if cc; calculated at 2% of value
		this.asset = asset;
	}

	get_interest = () => {
		return (this.rate / 12) * this.value;
	};

	get_payment = (payment: number | null = null) => {
		// if null, will use min payment..
		let payment_principle: number;
		let payment_interest: number;
		let operating_cost: number;

		operating_cost = this.asset != null ? this.asset.get_payment() : 0;

		// 2% of balance according to nerdwallet - https://www.nerdwallet.com/article/credit-cards/credit-card-issuer-minimum-payment
		let min_payment = this.type == 'cc' ? 0.02 * this.value : this.min_payment + operating_cost;
		payment = payment == null ? min_payment : payment;

		payment_interest = this.get_interest() > payment ? payment : this.get_interest();
		payment_principle = payment - payment_interest - operating_cost;
		return {
			interest: payment_interest,
			principle: payment_principle,
			operating_cost: operating_cost,
			total: payment_interest + payment_principle + operating_cost
		};
	};
	pay = (payment: number | null = null) => {
		//positive = more debt..
		let payObj = this.get_payment(payment);

		payObj.principle;
		this.value -= payObj.total - payObj.operating_cost;
	};

	apply_interest = () => {
		this.value += this.get_interest();
	};
	forward = (payment: number | null = null) => {
		//positive = more debt..
		this.apply_interest();
		this.pay(payment);
		if (this.asset != null) {
			this.asset.forward();
		}
	};
};

export const Debts = class {
	constructor(user: string) {
		this.user = user;
	}

	my_func = (x: number): number => {
		return x * 2;
	};

	get_user = () => {
		return this.user;
	};
};
