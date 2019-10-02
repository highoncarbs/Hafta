new Vue({
    el: '#quickinput_form',
    data() {
        return {
            employee: '',
            date: null,
            showInput: false,
            dataList: [],
            data: [],
            selected: null,
            submitting: false,
            report: null,
            feedback: null,
            errors: {
            }
        }
    },
    delimiters: ['[[', ']]'],
    computed: {
        filteredDataObj() {
            if (this.dataList.length != 0) {
                return this.dataList.filter((option) => {
                    return option.name
                        .toString()
                        .toLowerCase()
                        .indexOf(this.employee.toLowerCase()) >= 0
                })
            }
        }
    },
    methods: {

        checkData() {
            if (!this.selected) {
                this.$set(this.errors, 'selected', true)
            }
            if (!this.date) {
                this.$set(this.errors, 'date', true)
            }
            if (!this.report) {
                this.$set(this.errors, 'report', true)
            }

            if (Object.keys(this.errors).length == 0) {
                return true
            }

        },
        submitData() {

            if (this.checkData()) {
                this.submitting = true
                let raw = this
                let formdata = { 'emp_id': this.selected, 'date': this.date, 'report': this.report, 'feedback': this.feedback }
                axios.post('/transaction/quick/add', formdata)
                    .then(function (response) {
                        if (response.data.success) {
                            raw.$buefy.snackbar.open({
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
                            raw.report = null
                            raw.employee = ''
                            raw.selected = null
                        }
                        else if (response.data.message) {
                            raw.$buefy.snackbar.open({
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
                        raw.submitting = false

                    })
                    .catch(function (error) {
                        console.log(error)
                        raw.submitting = false
                    })
            }

        }
    },
    mounted() {
        let rawdata = this

        let today = new Date()
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();

        this.date = yyyy + '-' + mm + '-' + dd;

        axios.get('/employee/get/basic')
            .then(function (response) {
                rawdata.dataName = []
                rawdata.dataList = JSON.parse(response.data)
                rawdata.dataList.forEach((item) => rawdata.dataName.push(item))

                console.log(response.data)
            })


    }


})