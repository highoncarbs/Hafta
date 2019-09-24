const PerformanceForm =
{
    template: "#performance_form",
    data() {
        return {
            view: true,
            form: {
                errors: {},
                id: null,
                name: null,
                score: null,
                weight: null,
                mssg: null
            },
            data: null,
            modal: false,
            edit: {
                errors: {},
                id: null,
                name: null,
                score: null,
                weight: null,
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
            this.form.errors = {}

            if (!this.form.name) {
                this.$set(this.form.errors, 'name', 'Data required');

            }
            if (!this.form.score) {
                this.$set(this.form.errors, 'score', 'Data required');

            }
            if (!this.form.weight) {
                this.$set(this.form.errors, 'weight', 'Data required');

            }


            if (Object.keys(this.form.errors).length === 0) {
                return true;
            }
            else {
                return false;
            }


        },

        submitData(e) {
            this.checkData(e);
            let formdata = this;

            if (this.checkData()) {
                axios
                    .post('/master/add/performance', this.form)
                    .then(function (response) {
                        formdata.form.mssg = response['data']
                        formdata.form.name = null;
                        formdata.form.score = null;
                        formdata.form.weight = null;

                        if (response.data.success) {
                            data = data.filter(function (x) { return x.id === formdata.edit.id })
                            data[0].name = formdata.edit.name
                            data[0].score = formdata.edit.score
                            data[0].weight = formdata.edit.weight
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
            }
            e.preventDefault();
            this.focusInput()
        },
        getData(e) {
            const formdata = this;

            axios
                .get('/master/get/performance')
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
            this.edit.weight = data.weight
            this.edit.score = data.score
            this.edit.id = data.id

        },
        saveEditData(e) {
            let formdata = this;
            var data = this.data;

            this.edit.errors = {}

            if (!this.edit.name) {
                this.$set(this.edit.errors, 'name', 'Data required');

            }
            if (!this.edit.score) {
                this.$set(this.edit.errors, 'score', 'Data required');

            }
            if (!this.edit.weight) {
                this.$set(this.edit.errors, 'weight', 'Data required');

            }


            if (Object.keys(this.edit.errors).length == 0) {
                console.log('error free')


                axios
                    .post('/master/edit/performance', this.edit)
                    .then(function (response) {
                        console.log(response.data)
                        if (response.data.success) {
                            data = data.filter(function (x) { return x.id === formdata.edit.id })
                            data[0].name = formdata.edit.name
                            data[0].score = formdata.edit.score
                            data[0].weight = formdata.edit.weight
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
                    })
                return true
            }




            e.preventDefault();

        },
        deleteData(data, index) {
            // const removeId = data.id; 
            console.log(data);
            var datalist = this.data;
            let formdata = this

            axios
                .post('/master/delete/performance', data)
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
