<script lang="ts">

    
    import { onMount } from 'svelte';
    import { Calculator, Asset, Debt } from   '../lib/calculator';
    import { create_chart } from '../lib/charts';
    import Slider from '../components/Slider.svelte'
    import Debts from '../components/Debts.svelte'

    onMount(() => {
        create_chart();
    });

    1/0;

    let debtList = [
        new Debt('house', 0.0375, 114000, 1100, new Asset('house', +0.01, 200000, 500)),
        new Debt('car', 0.06, 30000, 400, new Asset('car', -0.1, 25000, 200)),
    ];

    let assetList = [
        new Asset('stock', 0.1, 10000, 0),
    ];

    let calculator = new Calculator(debtList, assetList);


    [0, 1, 2,3,4].forEach((i)=> {
        console.log(i);
        calculator.forward()
        console.log(calculator.results)
        // // console.log('Asset', ass1.type);
        // // console.log(ass1.value);

        // // console.log(debt1.type);
        // // console.log(debt1.value);
        
        // // console.log(debt1.get_interest())
        // // console.log(debt1.get_payment())
        // // debt1.forward()
        // // ass1.forward()
        // console.log('Debts')
        // debt_list.forEach(debt => {
        //     let payObj = debt.get_payment();
        //     console.log(payObj);
        //     console.log(debt.value);
        //     debt.forward();
        //     console.log(debt.value);
        //     console.log(debt.asset.value);
        // });

        // console.log('Assets')
        // asset_list.forEach(asset => {
        //     console.log(asset.value);
        //     asset.forward();
        //     console.log(asset.value);
        // });

        // console.log('Total Debt: ', debt_list.reduce((total, debt) => {return total + debt.value}, 0))
        // console.log('Total Debt Secured Assets: ', debt_list.reduce((total, debt) => {return total + (debt.asset == null ? 0 : debt.asset.value)}, 0))
        // console.log('Total Assets: ', asset_list.reduce((total, asset) => {return total + asset.value}, 0))
        
    });



    
</script>

<!--
    <h1>Dave Ramsey Cool Sciencey</h1>
    <p>This page is intending to create a financial calculator based on Dave's good ole advice.</p>
    

    <Slider min={0} max={100} value={50}></Slider>
-->
<container id='chart-container'>
    <svg id="chart-svg"></svg>
</container>

<Debts debtList={debtList}/>

<style>
    svg {
        width: 100%;
        height: 500px;
    }

    
</style>
