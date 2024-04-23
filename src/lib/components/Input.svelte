<script>
	export let val;
	export let label;
	export let units;
	export let min = 0;
	export let max = 100;
	export let readonly = false;
</script>


<label>
	 <input readonly={readonly} type=number bind:value={val} min={min} max={max}> 
	 {#if units}
	 ({units}) 
	 {/if}
	 
	 {label} 
</label>
<br>