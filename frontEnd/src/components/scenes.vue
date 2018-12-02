<template>
	<div class="messageBox">
		<div class="menuTop">Scene Editor</div>
		<div class="unsaved" v-if="!saved">Unsaved Changes</div>
		<div class="table">
			<div class="input">

				Scenes:
				<b-form-select v-model="selectValue" @change="changeItem">
					<option v-for="value in graphicList" :key="value.id" :value="value.name" :selected="value.name==sceneData.name">{{value.name}}</option>
				</b-form-select>
				&nbsp;&nbsp;<button class="btn btn-dark btt" style="display:inline-block" @click="makeNew">New</button>
				&nbsp;&nbsp;<button class="btn btn-dark btt" style="display:inline-block" v-if="selectValue" @click="deleteThis">Delete</button>
			</div>
			<div class="form">
				<div class="input">Name <input v-model="sceneData.name" /></div>
				<div class="input">Type <b-form-select v-model="sceneData.type">
						<option value="oneShot">One Shot</option>
						<option value="loop">Loop</option>
						<option value="timeTemp">Time/Temp</option>
						<option value="textScroll">Text Scroll</option>
					</b-form-select>
				</div>
				<div class="input" v-if="sceneData.type=='oneShot'">Graphic <b-form-select style="max-width:80%" v-model="sceneData.imageFile" @change="changeGif">
						<option value="null">-</option>
						<option v-for="value in imageFiles" :key="value.id" :value="value.name" :selected="value.name==sceneData.imageFile">{{value.name}}</option>
					</b-form-select>
				</div>
				<div v-if="loadingimg" class="input">Preview: <img class="imgman" ref="imgtest" :src="selectedImage" rel:auto_play="1" rel:rubbable="0" @load="loaded" width=128>
</div>
					<div class="input" v-if="sceneData.type=='oneShot'">Frame Rate <input v-model="sceneData.frameRate" /></div>
					<div class="input" v-if="sceneData.type=='oneShot'">Hold Time <input v-model="sceneData.holdFrame" /></div>
					<div class="input" v-if="sceneData.type=='loop'">Loop In <input v-model="sceneData.loopIn" /></div>
					<div class="input" v-if="sceneData.type=='loop'">Loop Out <input v-model="sceneData.loopOut" /></div>
					<div class="input" v-if="sceneData.type=='loop'">Loop Count <input v-model="sceneData.loops" /></div>
					<div class="input" v-if="sceneData.type=='timeTemp'">Font <input v-model="sceneData.font" /></div>
					<div class="input" v-if="sceneData.type=='timeTemp'">Font Size <input v-model="sceneData.fontSize" /></div>
					<div class="input" v-if="sceneData.type=='timeTemp'">Time X <input v-model="sceneData.timeX" /></div>
					<div class="input" v-if="sceneData.type=='timeTemp'">Time Y <input v-model="sceneData.timeY" /></div>
					<div class="input" v-if="sceneData.type=='timeTemp'">Temp X <input v-model="sceneData.tempX" /></div>
					<div class="input" v-if="sceneData.type=='timeTemp'">Temp Y <input v-model="sceneData.tempY" /></div>
					<div class="input" v-if="sceneData.type=='textScroll'">Scoll Text <input v-model="sceneData.scrollText" /></div>
					<div class="input" v-if="sceneData.type=='textScroll'">Scroll Speed <input v-model="sceneData.scrollSpeed" /></div>
					<div class="input" v-if="sceneData.type=='textScroll'">Text Color <input v-model="sceneData.colorText" /></div>
					<div class="input" v-if="sceneData.type=='textScroll'">BG Color <input v-model="sceneData.colorBg" /></div>
					<div class="input" v-if="sceneData.type=='textScroll'">Blink <input v-model="sceneData.blink" /></div>
					<div class="input" v-if="sceneData.type=='textScroll'">Blink Speed <input v-model="sceneData.blinkSpeed" /></div>
					<div class="input">Segment Displays
						<b-form-select v-model="sceneData.pinDisplay">
							<option value="null">-</option>
							<option v-for="value in segmentList" :key="value.id" :value="value.name">{{value.name}}</option>
						</b-form-select>
					</div>
					<div style="text-align:right">
						<button class="btn btn-dark btt" @click="saveChanges">Save Changes</button></div>
				</div>
			</div>
		</div>
</template>
<script>
export default {
	name: 'sceneSelect',
	data: function() {
		return {
			sceneData: { name: "" },
			graphicList: null,
			imageFiles: null,
			saved: true,
			selected: "",
			selectValue: "",
			imageValue: "",
			selectedImage: null,
			loadingimg: false,
			imageData: "",
			segmentList: "",
			animator: "",
			currentFrame: "",
		}
	},
	mounted: function() {
		this.axios.get(process.env.VUE_APP_WEB_URL + "/scene").then((response) => {
			this.graphicList = response.data

		})
		this.axios.get(process.env.VUE_APP_WEB_URL + "/images").then((response) => {
			this.imageFiles = response.data
		})

		this.axios.get(process.env.VUE_APP_WEB_URL + "/segments").then((response) => {
			this.segmentList = response.data
		})
	},
	methods: {
		changeGif: function() {
			clearTimeout(this.animator)
			this.currentFrame = 0
			this.loadingimg = false
			this.$nextTick(() => {
				this.loadingimg = true
				this.selectedImage = process.env.VUE_APP_WEB_URL + "/../images/" + this.sceneData.imageFile
			})
		},
		gifAnimate: function() {
			this.imageData.move_to(this.currentFrame)
			this.currentFrame++;
			var cFramer = this.sceneData.frameRate
			if (cFramer < 1 || cFramer == null) {
				cFramer = 1
			}
			if (this.imageData.get_length() > this.currentFrame + 1) {
				this.animator = setTimeout(this.gifAnimate, (1 / cFramer) * 1000)
			} else {
				this.currentFrame = 0
				this.animator = setTimeout(this.gifAnimate, this.sceneData.holdFrame * 1000)
			}
		},
		loaded: function() {
			let self = this
			this.imageData = new this.$libgif({ gif: this.$refs.imgtest })
			this.imageData.load(function() {
				window.console.log()
				self.imageData.pause()
				self.imageData.move_to(0)
				if (self.sceneData.frameRate < 1) {
					self.sceneData.frameRate = 1
				}
				if (self.imageData.get_length() > 1) {
					self.currentFrame = 0
					self.animator = setTimeout(self.gifAnimate, (1 / self.sceneData.frameRate) * 1000)
				}
			})
		},
		changeItem: function(valueChange) {
			this.axios.get(process.env.VUE_APP_WEB_URL + "/scene?name=" + valueChange).then((response) => {
				this.sceneData = response.data[0]
				if (this.sceneData.imageFile) {
					this.changeGif()
				}
			})

		},
		saveChanges: function() {
			let self = this
			this.axios.post(process.env.VUE_APP_WEB_URL + '/scene/update', { data: JSON.stringify(this.sceneData) })
				.then(function(response) {
					self.graphicList = response.data
				})
				.catch(function(error) {
					alert("error" + error)
				})
			this.saved = true
			this.selectValue = this.sceneData.name
		},
		makeNew: function() {
			this.loadingimg = false
			this.sceneData = { id: 999999, name: '', type: null, imageFile: null, frameRate: null, holdFrame: null, loopIn: null, loopOut: null, loops: null, font: null, fontSize: null, timeX: null, timeY: null, tempX: null, tempY: null, scrollText: null, scrollSpeed: null, colorText: null, colorBg: null, blink: null, blinkSpeed: null, pinDisplay: null }
			this.selectValue = null
		},
		deleteThis: function() {
			let self = this
			this.axios.get(process.env.VUE_APP_WEB_URL + "/scene/delete?name=" + this.selectValue).then(() => {
				this.axios.get(process.env.VUE_APP_WEB_URL + "/scene").then((response) => {
					this.graphicList = response.data
					this.loadingimg = false
					self.makeNew()

				})

			})
		}
	},

	props: {
		message: String,
	}
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.jsgif {
	display: inline-block;
}
</style>
<style scoped>
.messageBox {
	background-color: #eff9e7;
	display: inline-table;
	text-align: left;
	width: 50%;
	margin-top: 40px;
}

.table {
	padding: 15px;
	font-family: 'PrintChar21';
}

.imgman,
canvas {
	display: inline-block;
}

.menuTop {
	background-color: white;
	font-family: 'Shaston320';
	font-smooth: never;
	-webkit-font-smoothing: none;
	display: inline-table;
	text-align: left;

	background-color: #eff9e7;
}

.deleteButton {
	display: inline-block;
}

input,
.input {
	font-family: 'PrintChar21';
	font-smooth: never;
	-webkit-font-smoothing: none;

}

input {
	display: inline-block;
}

.input {
	padding-bottom: 10px;
}



.playlistSelect {
	height: 30px;
}

.custom-select {
	width: unset;
	font-family: 'PrintChar21';
	font-smooth: never;
	-webkit-font-smoothing: none;
	color: black;
}

.sceneSelect {
	font-family: 'PrintChar21';
	padding: 0;
	margin: 0;
	height: 30px;
	font-smooth: never;
	-webkit-font-smoothing: none;
	font-size: 16px;
	display: inline-block;
	max-width: 90%;
	background: unset;
	background-color: #FFF;
	border: unset;
}

.sceneSelect:focus {
	background-color: #000;
	color: #fff;
	box-shadow: unset;
	border: unset;
	border-radius: unset;
}
</style>