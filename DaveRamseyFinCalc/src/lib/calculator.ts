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