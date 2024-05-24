<script>
	export let style = '';
</script>

<div class="box" {style}>
	<slot>
		<em>no content was provided</em>
	</slot>
</div>

<style>
	.box {
		min-width: 250px;
		border: 1px solid #aaa;
		border-radius: 2px;
		box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
		padding: 1em;
		margin: 0.5rem;
		margin-top: 0rem;
		background-color: #ffffffe4;
	}
</style>
