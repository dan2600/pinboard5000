<template>
	<div class="menuclass">
		<ul>
			<li v-on:click="changer('home')">Home</li>
			<li v-on:click="changer('playlist')">Playlist</li>
			<li v-on:click="changer('scenes')">Scenes</li>
			<li v-on:click="changer('segments')">Segment Display</li>
			<li v-on:click="changer('fileupload')">Add Image</li>
		</ul>
		<div class="time">
			{{timeString}}
		</div>
	</div>
</template>
<script>
export default {
	name: 'menuBar',
	data: function() {
		return {
			time: new Date(),
			timeString: '00:00:00'
		}
	},
	mounted: function() {
		this.updateTime()
	},
	methods: {
		updateTime: function() {
			const self = this;
			setInterval(function() {
				this.time = new Date();
				this.theTime = [];
				this.theTime[0] = this.time.getHours().toString();
				this.theTime[1] = this.time.getMinutes().toString();
				this.theTime[2] = this.time.getSeconds().toString();

				for (this.i = 0; this.i < 3; this.i++) {
					if (this.theTime[this.i].length < 2) {
						this.theTime[this.i] = '0' + this.theTime[this.i];
					}
				}

				self.timeString = this.theTime[0] + ':' + this.theTime[1] + ':' + this.theTime[2];



			}, 1000)

		}
	},
	props: {
		mypage: String,
		changer: Function
	}
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.menuclass {
	font-family: 'Shaston320';
	font-smooth: never;
	-webkit-font-smoothing: none;
	margin: 0;
	height: 10%;
	min-height: 20px;
	font-size: 16px;
	background-color: #eff9e7;
	text-align: left;
}

.time {
	display: inline-block;
	position: absolute;
	right: 0;
	top: 10px;

}
</style>
<style scoped>
ul {
	text-align: left;
	list-style-type: none;
	padding: 0;
	margin: 0;
	text-align: left;
	height: 100%;
	min-height: 20px;
	display: inline-block;
}

li {
	display: inline-block;
	height: 100%;
	min-height: 20px;
	margin: 0;
	padding: 10px;
	padding-right: 10px;
	padding-left: 10px;
	border-left: dotted black;

}

li:hover {
	background-color: #b8bfb2;

}

a {
	color: #42b983;
}
</style>