<script lang="ts">
	import IconButton, { Icon } from '@smui/icon-button';
	import { mdiClose, mdiNoteEdit } from '@mdi/js';
	import { Asset } from '../lib/calculator';
	export let assetList: (typeof Asset)[] = [];

	let newAsset = () => {
		assetList = [...assetList, new Asset()];
		console.log(assetList);
	};

	let removeAsset = (e: Event) => {
		let ind = e.srcElement.id.replace('asset-remove-', '');
		assetList = assetList.filter((v, index) => {
			return ind != index;
		});
	};
</script>

<div id="assets-container">
	<div style="display: flex; align-items: center;">
		<IconButton class="material-icons" on:click={() => newAsset()}>add_small</IconButton> Add Asset
	</div>
	<div>
		<table style="align-items: center;">
			<tr>
				<th>Type</th>
				<th>Initial Value</th>
				<th>Interest Rate</th>
				<th>Operating Cost</th>
				<th>Actions</th>
			</tr>
			{#each assetList as asset, i}
				<tr>
					<!--type: string; // cc, auto, student, ... rate: number; // interest rate monthly % value:
					number; // how much asset at a given time step min_payment: number; // how much you are
					required to pay asset: typeof Asset | null;-->
					<td>{asset.type}</td>
					<td>{'$' + asset.value.toFixed(2)}</td>
					<td>{asset.rate * 100 + ' %'}</td>
					<td>{asset.operating_cost + '$/month'} </td>
					<td>
						<!-- <IconButton
							class="material-icons"
							on:click={() => console.log('Clicked..')}
							size="button"
						>
							<Icon tag="svg" viewBox="0 0 24 24">
								<path fill="currentColor" d={mdiNoteEdit} />
							</Icon>
						</IconButton> -->
						<IconButton
							id={'asset-remove-' + i}
							class="material-icons"
							on:click={(e) => removeAsset(e)}
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
	#assets-container {
		border-width: 1px;
		background-color: teal;
	}
</style>
