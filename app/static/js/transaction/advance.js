new Vue({
    el: "#advance_form",
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
                deduction: null

            },
            dataName: null,
            data: null,
            dataList: [],
            detailModal: false,
            empDetail: null,
            errors: [],
            submitting: false,
            value: 'Save',
            showEmpSelect: false



        }
    },
    mounted() {
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

        total: function(){
            console.log(this.advanceForm.totalAdvance , this.advanceForm.advanceamt)
            return Number(this.advanceForm.totalAdvance) + Number(this.advanceForm.advanceamt) }
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

            if (this.emp_id != null) {
                axios.post('/transaction/advance/employee/' + String(this.emp_id))
                    .then(function (response) {
                        console.log(response.data);
                        rawdata.empAdvanceDetail = JSON.parse(response.data)
                        rawdata.getAdvanceList();
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            }
            else {
                this.$set(this.errors, 'empadv', 'Null ID for employee')
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
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            }
            else {
                this.$set(this.errors, 'empadv', 'Null ID for employee')
            }

        },
        getOutstandingAdvance() {
            let outstandingamt = Number(0)
            if (this.empAdvanceList != null) {
                this.empAdvanceList.forEach(function (item) {
                    console.log(item)
                    outstandingamt += Number(item.advanceamt)
                })
            }
            this.advanceForm.totalAdvance = Number(outstandingamt)
            return this.formatedNumber(outstandingamt)
        },
        getEmployee(e) {
            let rawdata = this
            this.errors = []
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
                        rawdata.showEmpSelect = !rawdata.showEmpSelect
                        rawdata.dataList.forEach((item) => rawdata.dataName.push(item))



                        // let attendenceform = { 'company': rawdata.company, 'date': rawdata.month }
                        // axios.post('/transaction/attendence/get', attendenceform)
                        //     .then(function (response) {
                        //         rawdata.attendenceList = []
                        //         console.log(response.data)
                        //         rawdata.attendenceList = JSON.parse(response.data)


                        //         // Removes data from dataList if item present in AttendenceList
                        //         rawdata.attendenceList.forEach(function (item) {
                        //             if (rawdata.dataList.length != 0)
                        //                 rawdata.dataList.forEach(function (check, index) {
                        //                     if (check.id == item.employee[0].id) {
                        //                         console.log(check)
                        //                         rawdata.dataList.splice(index, 1)
                        //                     }

                        //                 })
                        //         })

                        //         rawdata.data = rawdata.dataList


                        //     });

                    })


                //    Need to pop emps whose data is already been filled
            }
            else {
                this.$set(this.errors, 'submit', "Please select both company and month.")
            }
            e.preventDefault();
        },
        updateData(e) {
            let rawdata = this
            let formdata = { 'company': this.company, 'date': this.month, 'data': this.attendenceList }
            axios.post('/transaction/attendence/update', rawdata.attendenceList)
                .then(function (response) {
                    console.log(response)
                    if (response.data.success) {
                        rawdata.$buefy.snackbar.open({
                            duration: 5000,
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

                    if (response.data.message) {
                        rawdata.$buefy.snackbar.open({
                            duration: 8000,
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

            e.preventDefault();
        },
        submitData(e) {
            let rawdata = this
            if (this.checkData(e)) {
                if (this.errors.length == 0) {

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
        checkData(e) {
            this.errors = []
            let raw = this
            let rawError = this.errors
            // this.dataList.forEach(function (item) {
            //     if (!item.daysatt == undefined) {
            //         if (rawError[item.id]) {
            //             raw.$set(rawError[item.id], 'daysatt', true)

            //         }
            //         else {
            //             raw.$set(rawError, item.id, {})
            //             raw.$set(rawError[item.id], 'daysatt', true)

            //         }

            //     }
            //     if (item.latecomin == undefined) {

            //         if (rawError[item.id]) {
            //             raw.$set(rawError[item.id], 'latecomin', true)

            //         }
            //         else {
            //             raw.$set(rawError, item.id, {})
            //             raw.$set(rawError[item.id], 'latecomin', true)

            //         }


            //     }
            //     if (item.earlygoing == undefined) {
            //         if (rawError[item.id]) {
            //             raw.$set(rawError[item.id], 'earlygoing', true)

            //         }
            //         else {
            //             raw.$set(rawError, item.id, {})
            //             raw.$set(rawError[item.id], 'earlygoing', true)

            //         }

            //     }




            //     // Reconsider how to set this up

            //     // if(item.pfval == null || item.pfval == undefined ){
            //     //     this.$set(this.errors , 'pfval' , 'Please fill out P.F . Set <b>0</b> for None/Null')
            //     // }
            //     // if(item.esival== null || item.esival == undefined ){
            //     //     this.$set(this.errors , 'esival' , 'Please fill out ESI . Set <b>0</b> for None/Null')
            //     // }

            // })

            e.preventDefault();
            if (this.errors.length == 0) {
                return true
            }
            else {
                return false;
            }
        },

    }
})

Vue.component('vue-feather', VueFeather);
