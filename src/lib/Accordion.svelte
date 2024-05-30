<script>
	export let open = false;
	import { slide } from 'svelte/transition';
	const handleClick = () => (open = !open);
</script>

<div class="accordion">
	<div class="header">
		<div class="text">
			<slot name="head"></slot>
		</div>

		<button on:click={handleClick}> +/- </button>
	</div>

	{#if open}
		<div class="details" transition:slide>
			<slot name="details"></slot>
		</div>
	{/if}
</div>

<style>
	div.accordion {
		min-width: 250px;
		border: 1px solid #aaa;
		border-radius: 2px;
		box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
		padding: 0.5rem;
		margin: 0.0rem;
		margin-top: 0rem;
		background-color: #ffffff44;
	}

	div.header {
		display: flex;
		width: 100%;
	}

	div.header .text {
		flex: 1;
		margin-right: 5px;
		display: inline-block;
        line-height: 24px;
        font-size: larger;
	}

	div.details {
		/* background-color: #cecece; */
		/* padding: 1rem; */
	}
</style>
