<template>
	<div class="messageBox">
		<div class="unsaved" v-if="!saved">Unsaved Changes</div>
		<div v-if="loadingimg">
			<img ref="imgtest" :src="filesource" rel:auto_play="1" rel:rubbable="1" @load="loaded" width=128>
		</div>
			<div class="form">
				Add Image
				<div class="input">Name <input v-if="uploadReady" type="file" id="file" ref="file" v-on:change="handleFileUpload" accept="image/*" /> </div>
				<button @click="submitFile">Upload</button>
			</div>
			<div class="table">
				Current Images
				<select v-model="selectValue" @change="changeGif">
					<option value="null">-</option>
					<option v-for="value in graphicList" :key="value.id" :value="value.name">{{value.name}}</option>
				</select>
				<button @click="deleteGraphic">Delete</button>
			</div>
		</div>
</template>
<script>
export default {

	name: 'homePage',
	data: function() {
		return {
			segmentData: null,
			graphicList: null,
			saved: true,
			selected: '',
			selectValue: '',
			uploadReady: true,
			file: '',
			filesource: null,
			loadingimg: true
		}
	},
	mounted: function() {
		this.axios.get(process.env.VUE_APP_WEB_URL + '/images').then((response) => {
			this.graphicList = response.data

		})
		window.console.log('shits')

	},
	methods: {
		changeGif: function() {
			this.loadingimg = false

			this.$nextTick(() => {
				this.loadingimg = true
				this.filesource = 'http://localhost:2600/images/' + this.selectValue
			})
		},
		loaded: function() {},
		handleFileUpload: function() {
			this.file = this.$refs.file.files[0];

		},
		deleteGraphic: function() {

			if (this.selectValue != null) {
				this.axios.get(process.env.VUE_APP_WEB_URL + '/deleteImage?name=' + encodeURIComponent(this.selectValue)).then((response) => {
					this.graphicList = response.data
				})
			}
		},
		submitFile: function() {
			var selfie = this
			let formData = new FormData();
			formData.append('file', this.file);
			this.axios.post(process.env.VUE_APP_WEB_URL + '/imageupload', formData, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			}).then(function(response) {
				selfie.graphicList = response.data
				selfie.uploadReady = false
				selfie.$nextTick(() => {
					selfie.uploadReady = true
				})
			}).catch(function(e) { alert(e) });
		}
	},
	props: {
		message: String,
	}
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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