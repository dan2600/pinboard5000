<template>
	<div class="messageBox">
		Segment Display
		<div class="unsaved" v-if="!saved">Unsaved Changes</div>
		<div class="table">
			<select v-model="selectValue" @change="changeItem">
				<option v-for="value in segmentList" :key="value.id" :value="value.name">{{value.name}}</option>
			</select>
			<button @click="makeNew" class="btn btn-dark btt">New</button>
		</div>
		<div class="form" v-if="segmentData">
			<div class="input">Name <input v-model="segmentData.name" /></div>
			<div class="lines" :key="x.id" v-for="x in linecount">
				<div class="input"><span class="scrs" v-if="segmentData.data[x-1].length > 16">Scrolling</span><input class="segmentInput" v-model="segmentData.data[x-1]" /></div>
			</div>
			<button  class="btn btn-dark btt" @click="addLine">Add Line</button>
			<button  class="btn btn-dark btt" @click="saveChanges">Save Changes</button>
		</div>
	</div>
</template>
<script>
export default {
	name: 'homePage',
	data: function() {
		return {
			segmentData: null,
			segmentList: null,
			saved: true,
			selected: '',
			selectValue: '',
			linecount: 0
		}
	},
	mounted: function() {
		this.axios.get(process.env.VUE_APP_WEB_URL + '/segments').then((response) => {
			this.segmentList = response.data
		})
	},
	methods: {
		changeItem: function() {
			this.axios.get(process.env.VUE_APP_WEB_URL + '/segments?name=' + this.selectValue).then((response) => {
				this.segmentData = response.data[0]
				this.segmentData.data = JSON.parse(this.segmentData.data)
				this.linecount = this.segmentData.data.length
				window.test = this.segmentData.data
			})

		},
		saveChanges: function() {
			let self = this
			this.axios.post(process.env.VUE_APP_WEB_URL + '/segments/update', { data: JSON.stringify(this.segmentData) })
				.then(function(response) {
					self.segmentList = response.data
				})
				.catch(function(error) {
					alert('error' + error)
				})
			this.saved = true
		},
		makeNew: function() {
			this.segmentData = { id: 999999, name: '', data: [''] }
			this.linecount = 1;
			this.segmentData.data[this.linecount - 1] = ''
			this.selectValue = null
		},
		addLine: function() {
			this.linecount++;
			this.segmentData.data[this.linecount - 1] = ''
		}
	},

	props: {
		message: String,
	}
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
input, select,
.input {
	font-family: 'PrintChar21';
	font-smooth: never;
	-webkit-font-smoothing: none;
	padding:none;
	margin:10px;
	height:36px;
	font-size: 16px;

}

.scrs
{
	font-size:8px;
	display:block;
}


.segmentInput
{
    height: 55px;
    width: 455px;
    font-family: '16segments';
    font-size: 60px;
    line-height: 40px;
    padding: 0;
    margin: 0;
    padding-top: 11px;
    color: orange;
    background-color: black;
    border: none;
}

.btt{
	background-color: black;
	margin:5px;
	padding:2px;
	height:35px;
	border-radius: 0;
}
.messageBox {
	text-align: center;

}

.form {
	width: 100%;
	text-align: center;
}

.input {
	width: 50%;
	display: inline-block;
}
</style>