const CompanyForm =
{
    template: "#company_form",
    data() {
        return {
            view: true,
            form: {
                errors: [],
                id: null,
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
    watch: {
        data: function () {
            feather.replace()
        }
    },
    delimiters: ["[[", "]]"],
    mounted() {
        feather.replace();
        var formdata = this;
        axios.get('/master/get/location')
            .then(function (response) {
                formdata.options = response.data;
            })
        this.focusInput()
    },
    methods: {
        focusInput() {
            this.$refs.name.focus();
        },
        checkData() {
            this.form.errors = []




            if (!this.form.name) {
                this.form.name = '';
                this.form.errors.push('Company required');
            }
            if (!this.form.location || this.form.location == -1) {
                this.form.location = -1;
                this.form.errors.push('Location required');
            }

            if (this.form.name && this.form.location) {
                return true;
            }


        },

        submitData(e) {
            this.checkData();
            var formdata = this;
            if (this.form.errors.length == 0) {
                axios
                    .post('/master/add/company', this.form)
                    .then(function (response) {

                        if (response.data.success) {
                            formdata.form.name = null;
                            formdata.form.location = -1;

                            formdata.$buefy.snackbar.open({
                                duration: 4000,
                                message: response.data.success,
                                type: 'is-light',
                                position: 'is-top-right',
                                actionText: 'Close',
                                queue: true,
                                onAction: () => {
                                    this.isActive = false;
                                }
                            })
                        }
                        else {
                            if (response.data.message) {
                                formdata.$buefy.snackbar.open({
                                    duration: 4000,
                                    message: response.data.message,
                                    type: 'is-light',
                                    position: 'is-top-right',
                                    actionText: 'Close',
                                    queue: true,
                                    onAction: () => {
                                        this.isActive = false;
                                    }
                                })
                            }
                        }
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            }
            e.preventDefault();
        },
        getData(e) {
            const formdata = this;

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
        editData(data) {
            this.edit.errors = []

            this.modal = true
            this.edit.name = data.name
            this.edit.id = data.id
            this.edit.location = data.location[0].id


        },
        saveEditData(e) {
            var formdata = this;
            var data = this.data;

            if (this.edit.name) {

                axios
                    .post('/master/edit/company', this.edit)
                    .then(function (response) {

                        if (response.data.success) {
                            data = data.filter(function (x) { return x.id === formdata.edit.id })
                            data[0].name = formdata.edit.name
                            data[0].location = [response.data['payload']]
                            formdata.modal = !formdata.modal;

                            formdata.$buefy.snackbar.open({
                                duration: 4000,
                                message: response.data.success,
                                type: 'is-light',
                                position: 'is-top-right',
                                actionText: 'Close',
                                queue: true,
                                onAction: () => {
                                    this.isActive = false;
                                }
                            })
                        }
                        else {
                            if (response.data.message) {
                                formdata.$buefy.snackbar.open({
                                    duration: 4000,
                                    message: response.data.message,
                                    type: 'is-light',
                                    position: 'is-top-right',
                                    actionText: 'Close',
                                    queue: true,
                                    onAction: () => {
                                        this.isActive = false;
                                    }
                                })
                            }
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
        deleteData(data, index) {
            let formdata = this
            axios
                .post('/master/delete/company', data)
                .then(function (response) {
                    if (response.data.success) {
                        data.splice(index, 1)
                        formdata.$buefy.snackbar.open({
                            duration: 4000,
                            message: response.data.success,
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }
                        })
                    }
                    else{
                        formdata.$buefy.snackbar.open({
                            duration: 4000,
                            message: response.data.message,
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }
                        })
                    }
                })
                .catch(function (error) {
                    console.log(error)
                })
        },
        selectRow() {

        },
    }
}
