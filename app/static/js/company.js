const CompanyForm =
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
                <p class="is-size-5">Edit Company</p>
                <br>
                <div class="field">
        <div class="control">
            <label for="" class="label">Company</label>
            <input type="text" class="input" v-model="edit.name" v-bind:class="[edit.name == '' ? 'is-danger' : '']" placeholder="Enter Comapny">
        </div>

    </div>
    <div class="field">
        <div class="control is-expanded">
            <label for="" class="label">Location</label>
            <div class="select is-fullwidth">
                <select  v-model="edit.location" v-bind:class="[edit.location == -1 ? 'is-danger' : '']">
                    <option value="-1" selected>Select Location</option>
                    <option v-for="opt in options" v-bind:value="opt.id">[[opt.name]]</option>
                </select>
            </div>
        </div>

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
            <label for="" class="label">Company</label>
            <input type="text" class="input" v-model="form.name" v-bind:class="[form.name == '' ? 'is-danger' : '']" placeholder="Enter Comapny">
        </div>

    </div>
    <div class="field">
        <div class="control is-expanded">
            <label for="" class="label">Location</label>
            <div class="select is-fullwidth">
                <select  v-model="form.location" v-bind:class="[form.location == -1 ? 'is-danger' : '']">
                    <option value="-1" selected>Select Location</option>
                    <option v-for="opt in options" v-bind:value="opt.id">[[opt.name]]</option>
                </select>
            </div>
        </div>

    </div>
    <div class="field is-grouped">
        <div class="control">
            <button type="submit" @click="submitData" class="button is-black"><span
                    class="icon icon-btn icon-btn-in"><i data-feather="plus"></i></span> Add</button>
        </div>
        <div class="control">
            <button class="button" v-on:click="view = !view ; form.name = null ; form.location = -1; " @click="getData"><span
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
                    <th v-on:click="sortTable()">Company</th>
                    <th v-on:click="sortTable()">Location</th>

                    <th>Action</th>
                </tr>

            </thead>
            <tbody>
                
                <tr v-for="( row ,index ) in data" v-bind:index="index" @click="selectRow(row)"
                    v:bind:class="selected : isSelected">
                    <td>[[ row.name]]</td>
                    <td>[[ row.location[0].name ]] </td>

                    <td>
                        <div class="buttons">
                            <div class="button" @click="editData(row)">Edit</div>
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
                                                        @click="deleteData(row , index)">Delete</div>
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
                location: -1,
                mssg: null
            },
            data: null,
            modal: false,
            edit: {
                errors: [],
                name: null,
                mssg: null,
                location: null,
            },
            confirm: false,
            ascending: false,
            sortColumn: '',
            options: null
        }
    },
    watch:{
        data : function(){
            feather.replace()
        }
    },
    delimiters: ["[[", "]]"], 
    mounted() {
        feather.replace();
        var formdata = this;
        axios.get('/master/get/location')
            .then( function(response){
                formdata.options = response.data;
            })
    },
    methods: {
        checkData(e) {
            if (this.form.name && this.form.location) {
                return true;
            }

            this.form.errors = []

            if (!this.form.name) {
                this.form.name = '';
                this.form.errors.push('Company required');
            }
            if (!this.form.location || this.form.location == -1)  {
                this.form.location = -1;
                this.form.errors.push('Location required');
            }
           

        },
        
        submitData(e) {
            this.checkData(e);
            var formdata = this ;
            console.log()
            if (this.form.errors.length == 0) {
                axios
                    .post('/master/add/company', this.form)
                    .then(function (response) {
                        formdata.form.mssg = response['data']
                        formdata.form.name = null;
                        formdata.form.location = -1;

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
                    .get('/master/get/company')
                    .then(function (response) {
                        formdata.data = response['data']

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
            this.edit.location= data.location[0].id


        },
        saveEditData(e){
            var formdata = this;
            var data  = this.data;
        
            if (this.edit.name) {
                
                axios
                .post('/master/edit/company' , this.edit)
                .then(function (response) {
                    if(response.data['success']){
                        data = data.filter( function(x){ return x.id === formdata.edit.id } )
                        data[0].name = formdata.edit.name
                        data[0].location = [response.data['payload']]
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

            if (this.edit.name == "") {
                this.edit.errors.push('Location required');
                
            }
          
    e.preventDefault();
            
        },
        deleteData(data , index){
            const removeId = data.id; 
            var loc = this.data; 

            axios
                    .post('/master/delete/company', data)
                    .then(function (response) {
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
