import {CC_MIN_PAYMENT_PRINCIPLE_RATE} from './config'

export const Calculator = class {
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

export const Asset = class {// like your car..
    type: string;
    value: number;
    depreciation: number; // number of years
    constructor(type: string, value: number, depreciation: number = 10){
        this.type = type;
        this.value = value;
        this.depreciation = depreciation
    }

    calc_depreciation = () => {
        return this.value * this.depreciation
    }

    depreciate = () => {
        this.value -= this.calc_depreciation()
    }
    
    increment = (amount: number) => {
        this.value += amount
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
        this.min_payment = min_payment;
        this.asset = asset
    }

    calc_monthly_interest = () => {
        return this.rate / 12 * this.value;
    }

    calc_monthly_payment = (payment: number | null = null) => { // if null, will use min payment..
        let payment_principle: number;
        let payment_interest: number;
        if(this.type == 'cc'){// principle increases asset value
            payment_principle = payment == null ? this.value*(CC_MIN_PAYMENT_PRINCIPLE_RATE/100/12) : payment
            payment_interest = payment == null ? this.value*(this.rate/100./12.) : payment
        }
        else{
            payment_principle = payment == null ? this.min_payment : payment
            payment_interest = payment == null ? this.value*(this.rate/100./12.) : payment
            return payment == null ? this.min_payment : payment
        }
    }

    step = (payment: number | null = null) => {
        this.value += this.calc_monthly_interest() - 
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