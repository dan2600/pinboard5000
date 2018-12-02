<template>
    <div class="messageBox">
        <div class="menuTop">Playlist</div>
        <div class="unsaved" v-if="!saved">Unsaved Changes</div>
        <div class="table">
            test
            <div class="playlistSelect" v-for="(row, ind) in playlistData" :key="row.id+'ddd'">
                <b-dropdown class="sceneSelect" v-model="playlistData[ind].graphic" variant="link">
                    <template slot="button-content">
                        {{playlistData[ind].graphic}} <div v-if="playlistData[ind].url" class="menuImg"><img :src="playlistData[ind].url" height=32></div>
                    </template>
                    <b-dropdown-item class="buttonitem" v-for="value in graphicList" :key="value.id" :value="value.name" @click="updateChoice(ind, value.name, value.imageFile)">
                        <div class="containerItem">
                            <div class="menuImg"><img  :src="url + '/../images/' + value.imageFile" height=32></div>
                                <div class="menuVal">{{value.name}}</div>
                            </div>
                    </b-dropdown-item>
                </b-dropdown>
                <button type="button" class="btn btn-dark btt2" @click="removeRow(row.id)">X</button>
            </div>
            <div class="padding"></div>
            <button type="button" class="btn btn-dark btt" @click="addEntry">Add Spot</button>
            <button type="button" class="btn btn-dark btt" @click="saveChanges">Save Changes</button>
        </div>
    </div>
</template>
<script>
export default {
    name: 'homePage',
    data: function() {
        return {
            url: process.env.VUE_APP_WEB_URL,
            playlistData: null,
            imagePreviews: [],
            graphicList: null,
            saved: true,
        }
    },

    mounted: function() {
        this.axios.get(process.env.VUE_APP_WEB_URL + "/scene").then((response) => {
            this.graphicList = response.data
            this.axios.get(process.env.VUE_APP_WEB_URL + "/playlist").then((response) => {
                this.playlistData = response.data
                for (this.i = 0; this.i < this.playlistData.length; this.i++) {
                    for (this.z = 0; this.z < this.graphicList.length; this.z++) {
                        if (this.playlistData[this.i].graphic == this.graphicList[this.z].name) {
                            window.console.log(this.graphicList[this.z].imageFile)
                            this.playlistData[this.i].url = this.url + '/../images/' + this.graphicList[this.z].imageFile
                        }
                    }
                }
            })
        })

    },
    methods: {
        setImage: function(image, index) {

            this.playlistData[index].url = this.url + '/../images/' + image
        },
        addEntry: function() {
            this.playlistData.push({ "id": this.playlistData.length, "graphic": "New" })
        },
        saveChanges: function() {
            this.axios.post(process.env.VUE_APP_WEB_URL + "/playlist/update", { data: JSON.stringify(this.playlistData) })
                .then((response) => {
                    this.playlistData = response.data
            for (this.i = 0; this.i < this.playlistData.length; this.i++) {
                for (this.z = 0; this.z < this.graphicList.length; this.z++) {
                    if (this.playlistData[this.i].graphic == this.graphicList[this.z].name) {
                        window.console.log(this.graphicList[this.z].imageFile)
                        this.playlistData[this.i].url = this.url + '/../images/' + this.graphicList[this.z].imageFile
                    }
                }
            }

                })
                .catch((error) => {
                    alert("error" + error)
                })
            this.saved = true
        },
        updateValue: function(e) {
            alert(e)
            this.playlistData[parseInt(e.target.id)].graphic = e.target.value
        },
        removeRow: function(id) {
            this.playlistData.splice(id, 1)
            for (var i = 0; i < this.playlistData.length; i++) {
                this.playlistData[i].id = i
            }
            this.saved = false
        },
        updateChoice(index, value, imageFile) {

            this.playlistData[index].graphic = value
            this.playlistData[index].url = this.url + '/../images/' + imageFile
            this.saved = false


        }
    },

    props: {
        message: String,
    }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->

<style>
	
.dropdown-toggle
{
	color: black;
}
.dropdown-toggle:hover, .dropdown-toggle:focus{
	color: black;
	text-decoration: none;
}

.dropdown-menu.show, .containerItem{
	background-color: #eee;

}

</style>

<style scoped>
.containerItem {
    width: auto;
    position: relative;
}

.menuImg {

    display: inline-block;

}

.menuVal {
    padding-left: 5px;
    display: inline-block;
}

.messageBox {
    background-color: #eff9e7;
    display: inline-table;
    text-align: left;
    width: 50%;
    margin-top: 40px;
}

.menuTop {
    background-color: white;
    font-family: 'Shaston320';
    font-smooth: never;
    -webkit-font-smoothing: none;
    display: inline-table;
    text-align: left;
    width: 100%;
    background-color: #eff9e7;
}

.deleteButton {
    display: inline-block;
}

.btt,
.btt2 {
    font-family: 'PrintChar21';
    font-smooth: never;
    -webkit-font-smoothing: none;
    border: unset;
    border-radius: unset;

    height: 30px;
    margin-left: 10px;

    background-color: black;

}

.btt2 {
    width: 10%;
    height: 30px;
    padding: 0;
    margin: 0;
    background-color: black;
}


.playlistSelect {
    height: 48px;
    padding: 2px;

}

.menuImg
{
	float: left;
}


.btn-link:hover{
		text-decoration: none;
		color: black;
}

.sceneSelect, .sceneSelect a {
    font-family: 'PrintChar21';
    padding: 0;
    margin: 0;
    height: 48px;
    font-smooth: never;
    -webkit-font-smoothing: none;
    font-size: 16px;
    width: 90%;
    color: black;
    display: inline-block;
    background: unset;

    border: unset;
}
.padding{
	height: 20px;
}
.sceneSelect:focus {
    background-color: #000;
    color: #fff;
    box-shadow: unset;
    border: unset;
    border-radius: unset;
}
</style>