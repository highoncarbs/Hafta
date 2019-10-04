// Reset all data when changing selection of select employee

//  #TODO : Needs update  to Performance when edited , move Performace calculation to front - later 
new Vue({
    el: "#performance_form",
    data() {

        return {
            company: null,
            errors: {},
            editerrors: {},
            employee: '',
            emp_id: null,

            fromdate: null,
            todate: null,
            currentSort: 'employee',
            currentSortDir: 'asc',
            dataList: [],
            factorList: [],
            factorName: [],
            showEmpSelect: false,
            tempfactor: '',
            rows: [],
            showPerfTable: false,
            submitting: false,
            viewPast: false,
            viewPastButton: false,
            pastRecords: [],
            tempPastRecords: [],
            searchQuery: '',

            attModal: false,
            performanceDetail: null,
            editFactorList: null,
            editPerfTable: null,
            editPerfModal: false,
            quickReports: null,
            quickPerfModal: false
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
        },
        filteredRecordList() {
            this.pastRecords = this.tempPastRecords.filter(data => {
                return data.employee[0].name.toLowerCase().includes(this.searchQuery.toLowerCase())
            });

            if (this.currentSort == 'name') {
                if (this.currentSortDir == 'asc') {
                    this.pastRecords.sort(function (a, b) { return ('' + a.name).localeCompare(b.name) })
                }
                else if (this.currentSortDir == 'desc') {
                    this.pastRecords.sort(function (a, b) { return ('' + a.name).localeCompare(b.name) }).reverse()
                }
            }

            if (this.currentSort == 'from') {
                if (this.currentSortDir == 'asc') {
                    this.pastRecords.sort(function (a, b) { return ('' + a.fromdate).localeCompare(b.fromdate) })
                }
                else if (this.currentSortDir == 'desc') {
                    this.pastRecords.sort(function (a, b) { return ('' + a.fromdate).localeCompare(b.fromdate) }).reverse()

                }

            }
            if (this.currentSort == 'to') {
                if (this.currentSortDir == 'asc') {
                    this.pastRecords.sort(function (a, b) { return ('' + a.todate).localeCompare(b.todate) })
                }
                else if (this.currentSortDir == 'desc') {
                    this.pastRecords.sort(function (a, b) { return ('' + a.todate).localeCompare(b.todate) }).reverse()

                }

            }

            if (this.currentSort == 'performance') {
                if (this.currentSortDir == 'asc') {

                    this.pastRecords.sort(function (a, b) { return ('' + a.net_score).localeCompare(b.net_score) })
                }
                else if (this.currentSortDir == 'desc') {
                    this.pastRecords.sort(function (a, b) { return ('' + a.net_score).localeCompare(b.net_score) }).reverse()

                }
            }


            return this.pastRecords
        },
    },

    watch: {
        employee: function (val) {
            if (val == "") {
                this.showPerfTable = false
            }
        }
    },

    methods: {

        getSelected(option) {
            this.emp_id = option.id
        },
        formatedDate(val) {
            var date = new Date(val)
            return (date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear());
        },
        getSelectedFactor(option, index) {
            this.rows[index].weight = option.weight
            this.rows[index].score = option.score
            this.rows[index].factor_id = option.id
            // this.rows.index.factor_id = option.id
        },
        sortBy(sortKey) {
            console.log(sortKey)
            if (sortKey === this.currentSort) {
                this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
            }
            this.currentSort = sortKey;


        },
        getFactor() {
            let rawdata = this
            this.viewPast = false;
            this.showEmpSelect = true;
            this.showPerfTable = true;
            this.quickReports = null
            let reportdata = { 'emp_id': this.emp_id, 'fromdate': this.fromdate, 'todate': this.todate }
            this.factorList = []
            if (this.emp_id) {

                axios.post('/transaction/quick/get', reportdata)
                    .then(function (response) {
                        rawdata.quickReports = JSON.parse(response.data)
                    })
                axios.get('/transaction/get/performance')
                    .then(function (response) {
                        rawdata.showPerfTable = true
                        console.log(response.data);
                        rawdata.viewPastButton = true
                        rawdata.factorName = []
                        rawdata.factorList = JSON.parse(response.data)
                        rawdata.factorList.forEach((item) => rawdata.factorName.push(item))

                    })


                //    Need to pop emps whose data is already been filled
            }
            else {
                this.$set(this.errors, 'submit', "Please select both company and dates.")
            }
        },
        filteredFactorObj(index) {
            let tempdataList = this.factorList.filter(data => {
                return data.name.toLowerCase().includes(this.rows[index].name.toLowerCase())
            });

            return tempdataList
        },
        getEmployee() {
            let rawdata = this
            this.errors = {}
            this.data = null
            this.dataList = []

            if (this.company && this.fromdate && this.todate) {
                this.showEmpSelect = true
                this.viewPast = false

                axios.get('/employee/get/by/company/' + String(this.company))
                    .then(function (response) {
                        console.log(response.data);
                        rawdata.dataName = []
                        rawdata.dataList = JSON.parse(response.data)
                        rawdata.dataList.forEach((item) => rawdata.dataName.push(item))

                    })


                //    Need to pop emps whose data is already been filled
            }
            else {
                this.$set(this.errors, 'submit', "Please select both company and dates.")
            }
        },
        // removeElement: function (index) {
        //     this.rows.splice(index, 1);
        // },
        // addRow: function (e) {
        //     var elem = document.createElement('tr');
        //     this.rows.push({
        //         name: "",
        //         obt_score: "",
        //         score: "",
        //         weight: "",
        //         factor_id: null,
        //         errors: {}

        //     });
        //     e.preventDefault();
        // },
        checkData() {
            this.errors = {}
            let raw = this
            let rawError = this.errors
            this.factorList.forEach(function (item) {
                if (item.obt_score == undefined) {
                    raw.$set(rawError, item.id, {})
                    raw.$set(rawError[item.id], 'obt_score', true)
                }

            })

            if (Object.keys(this.errors).length == 0) {
                return true
            }
            else {
                return false;
            }
        },
        checkEditData() {
            this.editerrors = {}
            let raw = this
            let rawError = this.editerrors
            this.editFactorList.performance_items.forEach(function (item) {
                if (item.obt_score == "" || item.obt_score == undefined) {
                    raw.$set(rawError, item.id, {})
                    raw.$set(rawError[item.id], 'obt_score', true)
                }
            })

            if (Object.keys(this.editerrors).length == 0) {
                return true
            }
            else {
                return false;
            }
        },
        submitData() {
            this.submitting = true
            let rawdata = this
            let formdata = { 'emp_id': this.emp_id, 'fromdate': this.fromdate, 'todate': this.todate, 'data': this.factorList }
            if (this.checkData()) {
                axios.post('/transaction/performance/save', formdata)
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

                            rawdata.showPerfTable = false
                            rawdata.employee = ''



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

                    })
                    .catch(function (error) {
                        rawdata.$buefy.snackbar.open({
                            duration: 4000,
                            message: "Couldn't send request. Server Error.",
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }
                        })
                        console.error(error)
                        this.submitting = false

                    })
            }

            this.submitting = false

        },
        viewPastRecords() {
            this.errors = {}
            if (this.company && this.fromdate && this.todate) {

                let formdata = { 'company': this.company, 'fromdate': this.fromdate, 'todate': this.todate }
                let rawdata = this
                this.viewPast = true;
                this.showEmpSelect = false;
                this.showPerfTable = false;

                axios.post('/transaction/performance/company', formdata)
                    .then(function (response) {
                        rawdata.pastRecords = JSON.parse(response.data)
                        rawdata.tempPastRecords = JSON.parse(response.data)
                        rawdata.$buefy.snackbar.open({
                            duration: 4000,
                            message: "Performance Loaded",
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
                        rawdata.$buefy.snackbar.open({
                            duration: 4000,
                            message: "Couldn't send request. Server Error.",
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }
                        })
                        console.error(error)
                    }
                    )
            }
            else {
                this.$set(this.errors, 'submit', "Please select both company and dates.")
            }
        },
        performanceModal(id) {
            this.attModal = !this.attModal
            let rawdata = this
            axios.get('/transaction/performance/get/employee/' + String(id))
                .then(function (response) {
                    rawdata.performanceDetail = JSON.parse(response.data)
                })
        },
        deletePerformance(id, index) {
            let rawdata = this
            axios.post('/transaction/performance/delete/' + String(id))
                .then(function (response) {
                    if (response.data.success) {
                        rawdata.tempPastRecords.splice(index, 1)
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
        },
        editPerformance(id) {
            this.editFactorList = this.tempPastRecords[id]
            this.editPerfModal = !this.editPerfModal
        },
        updateData() {
            this.submitting = true
            let rawdata = this
            let formdata = this.editFactorList
            if (this.checkEditData()) {

                axios.post('/transaction/performance/update', formdata)
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
                            rawdata.editPerfModal = !rawdata.editPerfModal
                            rawdata.viewPastRecords()

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

                    })
                    .catch(function (error) {
                        rawdata.$buefy.snackbar.open({
                            duration: 4000,
                            message: "Couldn't send request. Server Error.",
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }
                        })
                        console.error(error)
                        this.submitting = false

                    })

            }
            this.submitting = false

        },
    }
})