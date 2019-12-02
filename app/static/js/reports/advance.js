// Reset all data when changing selection of select employee

new Vue({
    el: "#advance_form_view",
    data() {

        return {
            company: null,
            employee: '',
            emp_id: null,
            empAdvanceDetail: null,
            empAdvanceList: null,
            month: null,

            advanceForm: {
                letter: null,
                date: null,
                totalAdvance: 0,
                advanceamt: 0,
                cheque_no: null,
                deduction_period: null,
                deduction: null,
                errors: {}

            },
            dataName: null,
            data: null,
            dataList: [],
            advEdit: false,
            empDetail: null,
            errors: {},
            submitting: false,
            value: 'Save',
            showEmpSelect: false,
            more: true,
            showAdvList: false
        }
    },
    mounted() {
    },
    watch: {
        employee: function (val) {
            if (val == "") {
                this.showAdvList = false
            }
        }
    },
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
        },

        total: function () {
            console.log(this.advanceForm.totalAdvance, this.advanceForm.advanceamt)
            return Number(this.advanceForm.totalAdvance) + Number(this.advanceForm.advanceamt)
        },

        // return this.formatedNumber(this.advanceForm.totalAmount)
    },
    delimiters: ['[[', ']]'],
    methods: {
        getSelected(option) {
            this.emp_id = option.id
        },
        formatedNumber(val) {
            let test = Number(val).toLocaleString('en-IN', { style: 'currency', currency: 'INR' });
            return test
        },
        formatedDate(val) {
            var date = new Date(val)
            return (date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear());
        },
        employeeDetail(id) {
            this.detailModal = !this.detailModal
            let rawdata = this
            axios.post('/employee/get/detail/' + String(id))
                .then(function (response) {
                    rawdata.empDetail = JSON.parse(response.data)
                })
        },
        getAdvanceDetail(e) {
            let rawdata = this

            if (this.company != null) {
                axios.get('/transaction/advance/all/' + String(this.company))
                    .then(function (response) {
                        console.log(response.data);
                        rawdata.empAdvanceDetail = JSON.parse(response.data)
                        rawdata.getAdvanceList();
                        rawdata.showAdvList = true;



                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            }
            else {
                this.advanceForm.errors = {}
                console.log("NUll ID")
                this.$set(this.advanceForm.errors, 'empadv', 'Null ID for employee')
            }

            e.preventDefault();
        },
        getAdvanceList() {
            let rawdata = this

            if (this.emp_id != null) {
                axios.post('/transaction/advance/get/' + String(this.emp_id))
                    .then(function (response) {
                        console.log(response.data);
                        rawdata.empAdvanceList = JSON.parse(response.data)
                        console.log(rawdata.empAdvanceList.length)
                        rawdata.more = true
                        if (rawdata.empAdvanceList.length >= rawdata.empAdvanceDetail.advancenum) {
                            rawdata.more = false;
                        }

                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            }
            else {
                this.$set(this.advanceForm.errors, 'empadv', 'Null ID for employee')
            }

        },
        getOutstandingAdvance() {
            let outstandingamt = Number(0)
            if (this.empAdvanceList != null) {
                this.empAdvanceList.forEach(function (item) {
                    console.log(item)
                    if (item.trans != 'debit') {
                        outstandingamt += Number(item.advanceamt)
                    }
                    else if (item.trans == 'debit') {
                        outstandingamt -= Number(item.advanceamt)
                    }
                })
            }
            this.advanceForm.totalAdvance = Number(outstandingamt)
            return this.formatedNumber(outstandingamt)
        },
        getAll(e) {
            let rawdata = this
            this.advanceForm.errors = {}
            this.data = null
            this.dataList = []
            this.attModal = false
            this.showEditTable = false
            if (this.company && this.month) {
                axios.get('/employee/get/by/company/' + String(this.company))
                    .then(function (response) {
                        console.log(response.data);
                        rawdata.dataName = []
                        rawdata.dataList = JSON.parse(response.data)
                        rawdata.showEmpSelect = true
                        rawdata.employee = ""
                        rawdata.showAdvList = false
                        rawdata.dataList.forEach((item) => rawdata.dataName.push(item))

                    })


                //    Need to pop emps whose data is already been filled
            }
            else {
                this.$set(this.advanceForm.errors, 'submit', "Please select both company and month.")
            }
            e.preventDefault();
        },
        submitData(e) {
            let rawdata = this
            if (this.checkData()) {
                console.log(this.advanceForm.errors.length)
                if (Object.keys(this.advanceForm.errors).length == 0) {

                    this.submitting = true
                    this.value = 'Saving'

                    let formdata = { 'emp_id': this.emp_id, 'data': this.advanceForm }
                    console.log(formdata)
                    axios.post('/transaction/advance/save', formdata)
                        .then(function (response) {
                            if (response.data.success) {
                                // Run notificaiton 
                                // Open selection for reports and printing
                                rawdata.$buefy.snackbar.open({
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

                                this.advanceForm.advanceamt = 0
                                this.advanceForm.date = null
                                this.advanceForm.deduction = null
                                this.advanceForm.deduction_period = null
                                this.advanceForm.cheque_no = null
                                this.advanceForm.letter = null

                            }
                            else if (response.data.message) {
                                // Run message
                                rawdata.$buefy.snackbar.open({
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
                                console.log(response.data.message)

                            }
                            this.submitting = false
                            this.value = 'Save'

                        })
                        .catch(function (error) {
                            // RUn error 
                            console.error(error);
                        })
                    this.submitting = false
                    this.value = 'Save'
                }
            }

            e.preventDefault();
        },
        viewAdvances() {
            this.advEdit = !this.advEdit

        },
        checkData() {
            this.advanceForm.errors = {}

            console.log('Inside cehckdata', this.advanceForm.date, this.advanceForm.cheque_no, this.advanceForm.deduction)

            if (!this.advanceForm.date) {
                this.$set(this.advanceForm.errors, 'date', true)
            }
            if (!this.advanceForm.letter) {
                this.$set(this.advanceForm.errors, 'letter', true)
            }
            if (!this.advanceForm.advanceamt) {
                this.$set(this.advanceForm.errors, 'advanceamt', true)
            }
            if (!this.advanceForm.cheque_no) {
                this.$set(this.advanceForm.errors, 'cheque_no', true)
            }
            if (!this.advanceForm.deduction_period) {
                this.$set(this.advanceForm.errors, 'deduction_period', true)
            }
            if (!this.advanceForm.deduction) {
                this.$set(this.advanceForm.errors, 'deduction', true)
            }

            if (this.advanceForm.advanceamt > this.empAdvanceDetail.advancevalue) {
                this.$set(this.advanceForm.errors, 'maxadv', true)

            }

            if (Object.keys(this.advanceForm.errors).length === 0) {
                return true
            }
            else {
                return false;
            }
        },
        editEmployee() {
            window.location.href = "/employee/edit/view/" + String(this.emp_id)
        },
        deleteAdvance(id, index) {
            let rawdata = this
            axios.post('/transaction/advance/delete/' + String(id))
                .then(function (response) {
                    if (response.data.success) {
                        rawdata.empAdvanceList.splice(index, 1)
                        rawdata.$buefy.snackbar.open({
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
                    else if (response.data.message) {
                        rawdata.$buefy.snackbar.open({
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
        }

    }
})

Vue.component('vue-feather', VueFeather);
