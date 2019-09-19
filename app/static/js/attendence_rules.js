const AttendenceRulesForm =
{
    template: '#attendence_rules_form',
    data() {
        return {
            view: true,
            form: {
                errors: {},
                id: null,
                late_comin: null,
                late_comin_day: null,
                early_going: null,
                early_going_day: null
            },
            data: null,
            modal: false,
            edit: {
                errors: {},
                id: null,
                late_comin: null,
                late_comin_day: null,
                early_going: null,
                early_going_day: null
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

            if (!this.form.early_going) {
                this.$set(this.form.errors, 'early_going', 'Data required');

            }
            if (!this.form.early_going_day) {
                this.$set(this.form.errors, 'early_going_day', 'Data required');

            }
            if (!this.form.late_comin) {
                this.$set(this.form.errors, 'late_comin', 'Data required');

            }
            if (!this.form.late_comin_day) {
                this.$set(this.form.errors, 'late_comin_day', 'Data required');

            }


            if (Object.keys(this.form.errors).length === 0) {
                return true;
            }
            else {
                return false;
            }
        },

        submitData(e) {

            let formdata = this;

            if (this.checkData()) {

                axios
                    .post('/master/add/attendence_rules', this.form)
                    .then(function (response) {

                        if (response.data.success) {

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
            }
            e.preventDefault();
            this.focusInput()
        },
        getData(e) {
            const formdata = this;

            axios
                .get('/master/get/attendence_rules')
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
            this.edit.late_comin = data.late_comin
            this.edit.early_going = data.early_going
            this.edit.late_comin_day = data.late_comin_day
            this.edit.early_going_day = data.early_going_day
            this.edit.id = data.id

        },
        saveEditData(e) {
            const formdata = this;
            var data = this.data;



            this.edit.errors = {}
            if (this.edit.early_going == "") {
                this.$set(this.edit.errors, 'early_going', 'Data required');

            }
            if (this.edit.early_going_day == "") {
                this.$set(this.edit.errors, 'early_going_day', 'Data required');

            }
            if (this.edit.late_comin == "") {
                this.$set(this.edit.errors, 'late_comin', 'Data required');

            }
            if (this.edit.late_comin_day == "") {
                this.$set(this.edit.errors, 'late_comin_day', 'Data required');

            }


            if (Object.keys(this.edit.errors).length == 0) {
                console.log('error free')

                axios
                    .post('/master/edit/attendence_rules', formdata.edit)
                    .then(function (response) {
                        console.log(response.data)
                        if (response.data.success) {
                            data = data.filter(function (x) { return x.id === formdata.edit.id })
                            data[0].early_going = formdata.edit.early_going
                            data[0].early_going_day = formdata.edit.early_going_day
                            data[0].late_comin = formdata.edit.late_comin
                            data[0].late_comin_day = formdata.edit.late_comin_day

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



            e.preventDefault();

        },
        deleteData(data, index) {
            // const removeId = data.id;
            let formdata = this;

            var datalist = this.data;

            axios
                .post('/master/delete/attendence_rules', data)
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
    }
}
