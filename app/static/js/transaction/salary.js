
new Vue({
    el: "#salary_sheet_form",
    data() {
        return {
            company: null,
            month: null,
            isGenerating: null,
            errors: {},
            salarySheet: null,
            selectedRow: null
        }
    },
    delimiters: ['[[', ']]'],
    computed: {
        salarySheetEdit() {
            if (this.salarySheet != null) {
                this.salarySheet.forEach(function (row) {
                    row.total_deductions = parseFloat(row.net_adv_deduction) + parseFloat(row.esi) + parseFloat(row.pf) + parseFloat(row.tds) + parseFloat(row.other_deduction) + parseFloat(0)
                    const tempPay = row.pay_1
                    row.net_payable = parseFloat(tempPay) - parseFloat(row.total_deductions)
                })
            }

            return this.salarySheet
        }
    },
    methods: {
        generateSalarySheet() {
            console.log("DAD")
            if (this.checkData()) {
                this.isGenerating = true
                let rawdata = this
                let formdata = { 'company': this.company, 'month': this.month }
                axios.post('/transaction/salary_sheet/generate', formdata)
                    .then(function (response) {
                        rawdata.salarySheet = response.data

                        rawdata.isGenerating = null;
                    })
                    .catch(function (error) {
                        rawdata.$buefy.snackbar.open({
                            duration: 4000,
                            message: 'Salary sheet could not be geenrated. Please check logs.',
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }
                        })

                        rawdata.isGenerating = null;

                    })
            }


        },
        formatedNumber(val) {
            let test = Number(val).toLocaleString('en-IN');
            return test
        },

        checkData() {
            this.errors = {}

            if (!this.company || !this.month) {
                this.$set(this.errors, 'req', true)
            }

            if (Object.keys(this.errors).length === 0) {
                return true
            }
            else {
                return false
            }
        },
        printAll() {
            let rawdata = this
            let formdata = { 'company': this.company, 'date': this.month, 'data': this.salarySheet }
            localStorage.setItem('jsondata', JSON.stringify(formdata))
            axios.post('/transaction/salary_sheet/print/all', formdata)
                .then(function (response) {
                    console.log(response)
                    const win = window.open('/transaction/salary_sheet/print/all', '_blank', [], true);
                })
        },
        processSalary() {
            let rawdata = this
            let formdata = { 'company': this.company, 'date': this.month, 'data': this.salarySheet }
            axios.post('/transaction/salary_sheet/process', formdata)
                .then(function (response) {
                    if (response.data.success) {
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
