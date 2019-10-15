const BenefitsForm =
{
    template: '#benefit_template',
    data() {
        return {
            view: true,
            form: {
                errors: [],
                id: null,
                name: null,
                mssg: null
            },
            data: null,
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
        data: function () {
            feather.replace()
        }
    },
    delimiters: ["[[", "]]"],
    mounted() {
        feather.replace();
        this.focusInput();
    },
    methods: {
        focusInput() {
            this.$refs.name.focus();
        },
        checkData(e) {
            this.form.errors = []
            if (this.form.name) {

                return true;
            }



            if (!this.form.name) {
                this.form.errors.push('Benefit required');
                this.$buefy.snackbar.open({
                    duration: 4000,
                    message: 'Benefit required',
                    type: 'is-light',
                    position: 'is-top-right',
                    actionText: 'Close',
                    queue: true,
                    onAction: () => {
                        this.isActive = false;
                    }
                })
            }

        },

        submitData(e) {
            this.checkData(e);
            var formdata = this;

            if (this.form.errors.length == 0) {
                axios
                    .post('/master/add/benefits', this.form)
                    .then(function (response) {
                        formdata.form.mssg = response['data']
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
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            }
            e.preventDefault();
            this.focusInput()
        },
        getData(e) {
            const formdata = this;

            axios
                .get('/master/get/benefits')
                .then(function (response) {
                    console.log(response);
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

        },
        saveEditData(e) {
            const formdata = this;
            var data = this.data;
            if (this.edit.name) {

                axios
                    .post('/master/edit/benefits', this.edit)
                    .then(function (response) {
                        console.log(response.data.success)
                        if (response.data.success) {
                            data = data.filter(function (x) { return x.id === formdata.edit.id })
                            data[0].name = formdata.edit.name
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
                            formdata.edit.errors.push(response.data)

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
            }


            this.edit.errors = []
            console.log(this.edit.name)

            if (this.edit.name == "") {
                this.edit.errors.push('Benefits required');

            }

            e.preventDefault();

        },
        deleteData(data, index) {
            // const removeId = data.id; 
            console.log(data);
            var datalist = this.data;

            axios
                .post('/master/delete/benefits', data)
                .then(function (response) {
                    if (response.data.success) {
                        datalist.splice(index, 1)
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
                })
                .catch(function (error) {
                    console.log(error)
                    formdata.$buefy.snackbar.open({
                        duration: 4000,
                        message: error,
                        type: 'is-light',
                        position: 'is-top-right',
                        actionText: 'Close',
                        queue: true,
                        onAction: () => {
                            this.isActive = false;
                        }
                    })
                })
        },
        selectRow() {

        },
    }
}
