import { DEFAULT_TAX_RATE } from './config'
import type { CalculatorResults } from './interfaces';

export const Calculator = class {
    debt_list: typeof Debt[];
    asset_list: typeof Asset[];
    results: CalculatorResults[];

    constructor(debt_list: typeof Debt[], asset_list: typeof Asset[]) {
        this.debt_list = debt_list;
        this.asset_list = asset_list;
        this.results = {
            t: [],
            debts: [],
            assets_debt_secured: [],
            assets: [],
        }
        this.append_results()
    }

    append_results = () => {
        this.results.t.push(this.results.t.length) // if Zero, push 1, .. always pushes next value
        this.results.debts.push(
            {
                total: this.debt_list.reduce((total, debt) => {return total + debt.value}, 0),
                /// tack on aggregated by "type" ? as well?
            }
        )
        this.results.assets_debt_secured.push(
            {
                total: this.debt_list.reduce((total, debt) => {return total + (debt.asset == null ? 0 : debt.asset.value)}, 0)
                /// tack on aggregated by "type" ? as well?
            }
        )
        this.results.assets.push(
            {
                total: this.asset_list.reduce((total, asset) => {return total + asset.value}, 0)
            }
        )
    }

    forward() {
        this.debt_list.forEach(debt => {
            debt.forward();
        });

        this.asset_list.forEach(asset => {
            asset.forward();
        });
        this.append_results();
    }
};

export const Asset = class {// like your car..
    type: string; // car, real_estate, house?..."roth", "pretax", "taxable", null..
    rate: number;// can be positive or negative; negative meaning depreciation
    value: number;
    operating_cost: number; //monthly cost if applicable (insurance taxes etc?)
    constructor(
        type: string,
        rate: number,
        value: number,
        operating_cost: number,
    ){
        this.type = type;
        this.rate = rate;
        this.value = value;
        this.operating_cost = operating_cost;
    }

    get_interest = () => {
        return this.value * this.rate / 12; //monthly..
    }

    get_payment = () => {
        return this.operating_cost;
    }

    get_post_tax_value = (tax_rate: number | null = null) => {
        tax_rate = tax_rate == null ? DEFAULT_TAX_RATE : tax_rate;
        if(this.type=="pretax" || this.type == "taxable"){
            return this.value * (1 - tax_rate);
        }
        else{
            return this.value;
        }
    }

    pay = () => {
        let a = 1;
    } // since operating cost, won't actually do anything to the value..

    apply_interest = () => {
        this.value += this.get_interest();
    }

    forward = () => { //positive = more debt..
        this.apply_interest();
        this.pay();
    }
}

export const Debt = class {
    type: string; // cc, auto, student, ...
    rate: number; // interest rate monthly %
    value: number; // how much debt at a given time step
    min_payment: number; // how much you are required to pay
    asset: typeof Asset | null;
    constructor(type: string, rate: number, value: number, min_payment: number, asset: typeof Asset | null){
        this.type = type;
        this.rate = rate; // APR
        this.value = value;
        this.min_payment = min_payment; // ignored if cc; calculated at 2% of value
        this.asset = asset
    }

    get_interest = () => {
        return this.rate / 12 * this.value;
    }

    get_payment = (payment: number | null = null) => { // if null, will use min payment..
        let payment_principle: number;
        let payment_interest: number;
        let operating_cost: number;

        operating_cost = this.asset != null ? this.asset.get_payment(): 0;
        
        // 2% of balance according to nerdwallet - https://www.nerdwallet.com/article/credit-cards/credit-card-issuer-minimum-payment
        let min_payment = this.type == 'cc' ? 0.02 * this.value : this.min_payment + operating_cost;
        payment = payment == null ? min_payment : payment;
        
        payment_interest = this.get_interest() > payment ? payment : this.get_interest();
        payment_principle = payment - payment_interest - operating_cost;
        return {
            interest: payment_interest,
            principle: payment_principle,
            operating_cost: operating_cost,
            total: payment_interest + payment_principle + operating_cost,
        }
    }
    pay = (payment: number | null = null) => { //positive = more debt..
        let payObj = this.get_payment(payment);

        payObj.principle
        this.value -= (payObj.total - payObj.operating_cost);
    }

    apply_interest = () => {
        this.value += this.get_interest();
    }
    forward = (payment: number | null = null) => { //positive = more debt..
        this.apply_interest();
        this.pay(payment);
        if(this.asset != null){
            this.asset.forward()
        }
    }
        
}

export const Debts = class {
    constructor(user: string) {
        this.user = user;
    }

    my_func = (x: number): number => {
        return x * 2;
    }

    get_user = () => {
        return this.user;
    }
};