
new Vue({
    el: "#salary_sheet_form_view",
    data() {
        return {
            company: null,
            month: null,
            isGenerating: null,
            errors: {},
            salarySheet: null,
            selectedRow: [],
            salarySheetView: null,
            days: Number(0),
            late: 0,
            going: 0,
            salary: 0,
            daysPayable: 0,
            pay_1: 0,
            adv_deduction: 0,
            esi: 0,
            pf: 0,
            tds: 0,
            other_deduction: 0,
            total_deductions: 0,
            net_pay: 0,
        }
    },
    delimiters: ['[[', ']]'],
    computed: {
        salarySheetEdit() {
            if (this.salarySheet != null) {
                this.salarySheet.forEach(function (row) {
                    row.total_deductions = parseFloat(row.net_adv_deduction) + parseFloat(row.esi) + parseFloat(row.pf) + parseFloat(row.tds) + parseFloat(row.other_deduction) + parseFloat(0)
                    const tempPay = row.pay_1
                    row.net_payable = Math.round(parseFloat(tempPay) - parseFloat(row.total_deductions))
                })
            }

            return this.salarySheet
        }
    },
    methods: {
        generateSalarySheet() {
            if (this.checkData()) {
                this.isGenerating = true
                let rawdata = this
                let formdata = { 'company': this.company, 'month': this.month }
                let checkformdata = { 'company': this.company, 'date': this.month }

                axios.post('/transaction/salary_sheet/get/processed', checkformdata)
                    .then(function (response) {
                        let payload = response.data

                        rawdata.salarySheetView = JSON.parse(payload.data)


                        let days = Number(0)
                        let late = 0
                        let going = 0
                        let salary = 0
                        let daysPayable = 0
                        let pay_1 = 0
                        let adv_deduction = 0
                        let esi = 0
                        let pf = 0
                        let tds = 0
                        let other_deduction = 0
                        let total_deductions = 0
                        let net_pay = 0

                        rawdata.salarySheetView.forEach(function (item) {
                            console.log(item.net_payable)
                            days = Number(item.daysatt)
                            late += item.latecomin
                            going += item.earlygoing
                            salary += Number(item.employee[0].basicpay)
                            daysPayable += item.days_payable
                            pay_1 += item.pay_1
                            adv_deduction += item.net_adv_deduction
                            esi += item.esi
                            pf += item.pf
                            tds += item.tds
                            other_deduction += item.other_deduction
                            total_deductions += item.total_deductions
                            net_pay += item.net_payable
                        })

                        rawdata.days = days
                        rawdata.late = late
                        rawdata.going = going
                        rawdata.salary = salary
                        rawdata.daysPayable = daysPayable
                        rawdata.pay_1 = Math.round(pay_1, 2)
                        rawdata.adv_deduction = adv_deduction
                        rawdata.esi = esi
                        rawdata.pf = pf
                        rawdata.tds = tds
                        rawdata.other_deduction = other_deduction
                        rawdata.total_deductions = total_deductions
                        rawdata.net_pay = Math.round(net_pay, 2)


                    })
                    .catch(function (error) {
                        console.log(error)
                    })

                axios.post('/transaction/salary_sheet/generate', formdata)
                    .then(function (response) {
                        if (response.data.message) {
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
                            rawdata.salarySheet = null

                            rawdata.isGenerating = null;
                        }
                        else {
                            rawdata.salarySheet = response.data

                            rawdata.isGenerating = null;
                        }
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
            // let test = Number(val).toLocaleString('en-IN');
            return val
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
            localStorage.clear()
            let formdata = { 'company': this.company, 'date': this.month, 'data': this.salarySheet }
            console.log(this.salarySheet)
            localStorage.setItem('jsondata', JSON.stringify(formdata))
            axios.post('/transaction/salary_sheet/print/all', formdata)
                .then(function (response) {
                    console.log(response)
                    const win = window.open('/transaction/salary_sheet/print/all', '_blank', [], true);
                })
        },
        // deleteSheet() {
            
        // },
        printSavedAll() {
            let rawdata = this
            localStorage.clear()
            let formdata = { 'company': this.company, 'date': this.month, 'data': this.salarySheetView }
            localStorage.setItem('jsondata', JSON.stringify(formdata))
            axios.post('/transaction/salary_sheet/print/all', formdata)
                .then(function (response) {
                    console.log(response)
                    const win = window.open('/transaction/salary_sheet/print/all', '_blank', [], true);
                })
        },
        pushRow(index) {
            console.log(index)
            let raw = this
            if (this.selectedRow.includes(index)) {
                this.selectedRow.filter(function (item) {
                    if (item == index) {
                        console.log(item, index, raw.selectedRow)
                        raw.selectedRow.splice((raw.selectedRow.indexOf(item)), 1)
                    }
                })

            }
            else {
                this.selectedRow.push(index);
            }
        },
        printSelected() {
            let rawdata = this
            let selectedData = []
            this.selectedRow.forEach(function (index) {
                selectedData.push(rawdata.salarySheet[rawdata.selectedRow.indexOf(index)])
            })
            let formdata = { 'company': this.company, 'date': this.month, 'data': selectedData }
            localStorage.setItem('selecteddata', JSON.stringify(formdata))
            axios.post('/transaction/salary_sheet/print/selected', formdata)
                .then(function (response) {
                    console.log(response)
                    const win = window.open('/transaction/salary_sheet/print/selected', '_blank', [], true);
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
