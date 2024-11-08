<script lang="ts">
	import IconButton, { Icon } from '@smui/icon-button';
	import { mdiClose, mdiNoteEdit } from '@mdi/js';
	import { Debt } from '../lib/calculator';
	export let debtList: (typeof Debt)[] = [];

	let newDebt = () => {
		debtList = [...debtList, new Debt()];
		console.log(debtList);
	};

	let removeDebt = (e: Event) => {
		let ind = e.srcElement.id.replace('debt-remove-', '');
		debtList = debtList.filter((v, index) => {
			return ind != index;
		});
	};
</script>

<div id="debts-container">
	<div style="display: flex; align-items: center;">
		<IconButton class="material-icons" on:click={() => newDebt()}>add_small</IconButton> Add Debt
	</div>
	<div>
		<table style="align-items: center;">
			<tr>
				<th>Type</th>
				<th>Initial Value</th>
				<th>Interest Rate</th>
				<th>Min Payment</th>
				<th>Asset</th>
				<th>Actions</th>
			</tr>
			{#each debtList as debt, i}
				<tr>
					<!--type: string; // cc, auto, student, ... rate: number; // interest rate monthly % value:
					number; // how much debt at a given time step min_payment: number; // how much you are
					required to pay asset: typeof Asset | null;-->
					<td>{debt.type}</td>
					<td>{'$' + debt.value.toFixed(2)}</td>
					<td>{debt.rate * 100 + ' %'}</td>
					<td>{debt.min_payment}</td>
					<td>{debt.asset?.type}</td>

					<td>
						<IconButton
							class="material-icons"
							on:click={() => console.log('Clicked..')}
							size="button"
						>
							<Icon tag="svg" viewBox="0 0 24 24">
								<path fill="currentColor" d={mdiNoteEdit} />
							</Icon>
						</IconButton>
						<IconButton
							id={'debt-remove-' + i}
							class="material-icons"
							on:click={(e) => removeDebt(e)}
							size="button"
						>
							<Icon tag="svg" viewBox="0 0 24 24">
								<path fill="currentColor" d={mdiClose} />
							</Icon>
						</IconButton>
					</td>
				</tr>
			{/each}
		</table>
	</div>
</div>

<style>
	@import '/_Typography.scss';
	#debts-container {
		border-width: 1px;
		background-color: gray;
	}
</style>
