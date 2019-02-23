<template>
		<div class="messageBox">
				welcome to pinball 50000
		</div>
</template>
<script>
export default {
	name: 'homePage',
	data: function() {
		return {
			timeString: '00:00:00'
		}
	},
	mounted: function() {
		window.console.log()
	},
	methods: {},

	props: {
		message: String,

	}
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>