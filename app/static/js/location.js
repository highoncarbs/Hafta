const LocationForm =
{
    template: `  
            <div>

<!-- Edit Modal -->
<div class="modal animated is-active fadeIn" v-show="modal">
    <div class="modal-background" @click="modal = !modal"></div>
    <div class="modal-content">

        <div class="box">

            <div v-if="edit.mssg" class="notification animated fadeIn">
                <p><span class="icon icon-btn" v-if="edit.mssg['success']"><i
                            data-feather="alert-circle"></i></span> [[ edit.mssg['success'] ]]
                </p>
                <p class="icon icon-btn" v-if="edit.mssg['message']">[[ edit.mssg['message'] ]]
                </p>

            </div>
            <form id="data_entry" novalidate="true" @submit="submitData">
                <div v-if="edit.errors.length" class="notification animated fadeIn">ERROR</p>
                    <ul>
                        <li v-for="error in edit.errors" class="is-underline">[[ error.message ]]</li>
                    </ul>
                </div>
                <p class="is-size-5">Edit Location</p>
                <br>
                <div class="field">
                    <label class="label">Location</label>
                    <input class="input" v-model="edit.name" type="text">
                </div>
                <br>
                <div class="field is-grouped">
                    <p class="control">
                        <a class="button is-black" @click="saveEditData"><span class="icon icon-btn icon-btn-in"><i
                                    data-feather="plus"></i></span>Save
                        </a>
                    </p>

                    <p class="control">
                        <a class="button" @click="modal = !modal"><span class="icon icon-btn icon-btn-in"><i
                                    data-feather="x"></i></span>Cancel
                        </a>
                    </p>
                </div>
            </form>

        </div>
        <button class="modal-close is-large" aria-label="close" @click="modal = !modal"></button>

    </div>

</div>

<!-- Entry Form -->
<div v-if="form.mssg" class="notification animated fadeIn">
    <p v-if="form.mssg.success">[[ form.mssg['success'] ]]</p>
    <p v-if="form.mssg.message" class="is-underline">[[ form.mssg['message'] ]]</p>

</div>

<form id="data_entry" novalidate="true" @submit="submitData ;" v-show="view">
    <div v-if="form.errors.length" class="notification">
        <p class="has-text-weight-semibold"> ERROR</p>
        <ul>
            <li v-for="error in form.errors " class="is-underline">[[ error ]]</li>
        </ul>
    </div>

    <div class="field">
        <div class="control">
            <label for="" class="label">Location</label>
            <input type="text" class="input" v-model="form.name" placeholder="Enter Location">
        </div>

    </div>
    <div class="field is-grouped">
        <div class="control">
            <button type="submit" @click="submitData" class="button is-black"><span
                    class="icon icon-btn icon-btn-in"><i data-feather="plus"></i></span> Add</button>
        </div>
        <div class="control">
            <button class="button" v-on:click="view = !view" @click="getData"><span
                    class="icon icon-btn icon-btn-in"><i data-feather="eye"></i></span> View</button>
        </div>
    </div>
</form>


<!-- Table  -->

<div v-show="!view">
<div class="control">
            <button class="button" v-on:click="view = !view ; form.errors = [] ; "><span
                    class="icon icon-btn icon-btn-in"><i data-feather="eye"></i></span> View</button>
        </div>
        <br>
    <div class="table-container" id="data_view">

        <table class="table is-bordered is-fullwidth">
            <thead>
                <tr>
                    <th v-on:click="sortTable()">Name</th>
                    <th>Action</th>
                </tr>

            </thead>
            <tbody>
                <tr v-for="( loc ,index ) in location" v-bind:index="index" @click="selectRow(loc)"
                    v:bind:class="selected : isSelected">
                    <td>[[ loc.name]]</td>
                    <td>
                        <div class="buttons">
                            <div class="button" @click="editData(loc)">Edit</div>
                            <div class="dropdown">
                                <div class="dropdown is-hoverable">
                                    <div class="dropdown-trigger">
                                        <button class="button is-danger" aria-haspopup="true"
                                            aria-controls="dropdown-menu4">
                                            <span>Delete</span>

                                        </button>
                                    </div>
                                    <div class="dropdown-menu" style="z-index:10;" id="dropdown-menu4" role="menu">
                                        <div class="dropdown-content has-background-light">
                                            <p class="dropdown-item">
                                                Are you sure ?
                                            </p>
                                            <hr class="dropdown-divider">

                                            <a class="dropdown-item">
                                                <div class="buttons ">
                                                    <div class="button is-danger is-small"
                                                        @click="deleteData(loc , index)">Delete</div>
                                                    <div class="button is-small">Cancel</div>
                                                </div>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</div>
    `,
    data() {
        return {
            view: true ,
            form: {
                errors: [],
                id : null,
                name: null,
                mssg: null
            },
            location: null,
            modal: false,
            edit: {
                errors: [],
                name: null,
                mssg: null
            },
            confirm: false,
            ascending: false,
            sortColumn: '',
        }
    },
    watch:{
        location : function(){
            feather.replace()
        }
    },
    delimiters: ["[[", "]]"], 
    mounted() {
        feather.replace();
    },
    methods: {
        checkData(e) {
            if (this.form.name && this.form.location) {
                return true;
            }

            this.form.errors = []

            if (!this.form.name) {
                this.form.errors.push('Location required');
            }
           

        },
        
        submitData(e) {
            this.checkData(e);
            var formdata = this ;

            if (this.form.errors.length == 0) {
                axios
                    .post('/master/add/location', this.form)
                    .then(function (response) {
                        formdata.form.mssg = response['data']
                        formdata.form.name = null;
                        setTimeout( () => { formdata.form.mssg = null } , 3000);
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            }
            e.preventDefault();
        },
        getData(e){
            const formdata = this ;

            axios
                    .get('/master/get/location')
                    .then(function (response) {
                        console.log(response);
                        formdata.location = response['data']

                    })
                    .catch(function (error) {
                        console.log(error)
                    });
        
            e.preventDefault();
        },
        editData(data){
            this.edit.errors = []

            this.modal = true
            this.edit.name = data.name
            this.edit.id = data.id

        },
        saveEditData(e){
            const formdata = this;
            var loc  = this.location;
            if (this.edit.name) {
                
                axios
                .post('/master/edit/location' , this.edit)
                .then(function (response) {
                    console.log(response.data.success)
                    if(response.data.success){
                        loc = loc.filter( function(x){ return x.id === formdata.edit.id } )
                        console.log(loc , loc.name)
                        loc[0].name = formdata.edit.name
                        formdata.modal =     !formdata.modal;
                    }
                    else{
                        formdata.edit.errors.push(response.data)
                    }

                })
                .catch(function (error) {
                    console.log(error)
                })
                return true;
            }


            this.edit.errors = []
            console.log(this.edit.name)

            if (this.edit.name == "") {
                this.edit.errors.push('Location required');
                
            }
          
    e.preventDefault();
            
        },
        deleteData(data , index){
            const removeId = data.id; 
            console.log(data);
            var loc = this.location; 

            axios
                    .post('/master/delete/location', data)
                    .then(function (response) {
                        console.log(response.data)
                        if(response.data.success){
                            loc.splice(index, 1)
                        }
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
        },
        selectRow(){

        },
    }
}
