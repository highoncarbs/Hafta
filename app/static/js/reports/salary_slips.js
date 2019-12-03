
new Vue({
    el: "#salary_slips_view",
    data() {
        return {
            employee: '',
            emp_id: null,
            start_month: null,
            end_month: null,
            dataList: [],
            dataName: [],
            slips: null
        }
    },
    delimiters: ['[[', ']]'],
    mounted() {
        let rawdata = this

        axios.get('/employee/get/basic')
            .then(function (response) {
                console.log(response.data);
                rawdata.dataName = []
                rawdata.dataList = JSON.parse(response.data)
                rawdata.employee = ""
                rawdata.dataList.forEach((item) => rawdata.dataName.push(item))

            })
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
    },
    methods: {
        getSelected(option) {
            this.emp_id = option.id
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
        formatedMonth(val) {
            let temp_date = new Date(val)
            let month = temp_date.toLocaleString('default', { month: 'long' })
            let year = temp_date.getFullYear()
            let print_date = month + ' , ' + year
            return print_date
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
        submitData() {
            let rawdata = this
            if (true) {

                let formdata = { 'emp_id': this.emp_id, 'start_date': this.start_month, 'end_date': this.end_month }

                axios.post('/transaction/salary_sheet/slips/range', formdata)
                    .then(function (response) {
                        if (response.data.success) {
                            rawdata.$buefy.snackbar.open({
                                duration: 4000,
                                message: "Data Loaded",
                                type: 'is-light',
                                position: 'is-top-right',
                                actionText: 'Close',
                                queue: true,
                                onAction: () => {
                                    this.isActive = false;
                                }
                            })

                            rawdata.slips = response.data.success

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

                    })
                    .catch(function (error) {
                        // RUn error 
                        console.error(error);
                    })
            }
        }

    }



})

Vue.component('vue-feather', VueFeather);
