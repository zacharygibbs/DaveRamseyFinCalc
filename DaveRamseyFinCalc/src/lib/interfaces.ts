export interface ControlParams {
    [key: string]: any
};

export interface CalculatorResults {
    t: number[],
    debts: DebtAssetValues[],
    assets_debt_secured: DebtAssetValues[],
    assets: DebtAssetValues[],
};

export interface DebtAssetValues {
    [key: string]: any
};

export interface CalculatorParams {
    name: string,
    [key: string]: any
};
