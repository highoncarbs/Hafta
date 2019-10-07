const LocationForm =
{
    template: "#location_form",
    data() {
        return {
            view: true,
            form: {
                errors: [],
                id: null,
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
    watch: {
        location: function () {
            feather.replace()
        }
    },
    delimiters: ["[[", "]]"],
    mounted() {
        feather.replace();
        this.$refs.name.focus();
    },
    methods: {
        checkData(e) {
            this.form.errors = []

            if (this.form.name) {
                return true;
            }
            if (!this.form.name) {
                this.form.errors.push('Location required');
            }


        },

        submitData(e) {
            this.checkData(e);
            var formdata = this;

            if (this.form.errors.length == 0) {
                axios
                    .post('/master/add/location', this.form)
                    .then(function (response) {

                        if (response.data.success) {
                            formdata.form.name = null;

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
        editData(data) {
            this.edit.errors = []

            this.modal = true
            this.edit.name = data.name
            this.edit.id = data.id
            this.$refs.editname.focus();

        },
        saveEditData(e) {
            const formdata = this;
            var loc = this.location;
            if (this.edit.name) {

                axios
                    .post('/master/edit/location', this.edit)
                    .then(function (response) {
                        console.log(response.data.success)

                        if (response.data.success) {
                            loc = loc.filter(function (x) { return x.id === formdata.edit.id })
                            loc[0].name = formdata.edit.name
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
            console.log(this.edit.name)

            if (this.edit.name == "") {
                this.edit.errors.push('Location required');

            }

            e.preventDefault();

        },
        deleteData(data, index) {

            var loc = this.location;
            let formdata = this
            axios
                .post('/master/delete/location', data)
                .then(function (response) {
                    if (response.data.success) {
                        loc.splice(index, 1)
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
