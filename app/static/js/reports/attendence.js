new Vue({
    el: "#attendence_form_view",
    data() {

        return {
            company: null,
            month: null,
            searchQuery: '',
            currentSort: 'name',
            currentSortDir: 'asc',
            data: null,
            dataList: [],
            detailModal: false,
            empDetail: null,
            errors: [],
            attendenceList: [],
            attModal: false,
            showEditTable: false,
            value: 'Save',
            submitting: false,
            showEmpSelect: false,
            isLoading: false



        }
    },
    mounted() {
    },
    computed: {
        //  TODO:   load on click only - FIX
        filteredList() {
            if (this.company != null && this.month != null) {

                this.dataList = this.data.filter(data => {
                    return data.name.toLowerCase().includes(this.searchQuery.toLowerCase())
                });

                return this.dataList;
            }
            return this.dataList;
        }


    },
    delimiters: ['[[', ']]'],
    methods: {
        formatedNumber(val) {
            let test = Number(val).toLocaleString('en-IN', { style: 'currency', currency: 'INR' });
            console.log(test)
            return test
        },
        formatedDate(val) {
            var date = new Date(val)
            return (date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear());


        },
        sortBy(sortKey) {
            console.log(sortKey)
            if (sortKey === this.currentSort) {
                this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
            }
            this.currentSort = sortKey;


        },
        employeeDetail(id) {
            this.detailModal = !this.detailModal
            let rawdata = this
            axios.post('/employee/get/detail/' + String(id))
                .then(function (response) {
                    rawdata.empDetail = JSON.parse(response.data)
                })
        },
        getAttendence() {
            let rawdata = this
            let attendenceform = { 'company': this.company, 'date': this.month }
            axios.post('/transaction/attendence/get', attendenceform)
                .then(function (response) {
                    rawdata.attendenceList = []
                    console.log(response.data)
                    rawdata.attendenceList = JSON.parse(response.data)


                    // Removes data from dataList if item present in AttendenceList
                    rawdata.attendenceList.forEach(function (item) {
                        if (rawdata.dataList.length != 0)
                            rawdata.dataList.forEach(function (check, index) {
                                if (check.id == item.employee[0].id) {
                                    console.log(check)
                                    rawdata.dataList.splice(index, 1)
                                }

                            })
                    })

                    rawdata.data = rawdata.dataList


                });

        },
        getEmployee(e) {
            let rawdata = this
            this.errors = []
            this.data = null
            this.dataList = []
            this.attModal = false
            this.showEditTable = false
            if (this.company && this.month) {
                this.isLoading = true
                axios.get('/employee/get/by/company/' + String(this.company))
                    .then(function (response) {
                        console.log(response.data);
                        // rawdata.data = JSON.parse(response.data)
                        rawdata.dataList = JSON.parse(response.data)
                        rawdata.getAttendence();
                        rawdata.isLoading = false



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
        submitData() {
            let rawdata = this
            
            if (this.checkData()) {


                this.submitting = true;
                this.value = 'Saving';
                let formdata = { 'company': this.company, 'date': this.month, 'data': this.filteredList }
                console.log(formdata)
                axios.post('/transaction/attendence/save', formdata)
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

                            rawdata.getAttendence();
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
                    .catch(function (error) {
                        // RUn error 
                        console.error(error);

                    })

            }
            this.submitting = false;
            this.value = 'Save';
        },
        checkData() {
            this.errors = []
            let raw = this
            let rawError = this.errors
            this.dataList.forEach(function (item) {
                if (item.daysatt == undefined) {
                    if (rawError[item.id]) {
                        raw.$set(rawError[item.id], 'daysatt', true)

                    }
                    else {
                        raw.$set(rawError, item.id, {})
                        raw.$set(rawError[item.id], 'daysatt', true)

                    }

                }
                if (item.latecomin == undefined) {

                    if (rawError[item.id]) {
                        raw.$set(rawError[item.id], 'latecomin', true)

                    }
                    else {
                        raw.$set(rawError, item.id, {})
                        raw.$set(rawError[item.id], 'latecomin', true)

                    }


                }
                if (item.earlygoing == undefined) {
                    if (rawError[item.id]) {
                        raw.$set(rawError[item.id], 'earlygoing', true)

                    }
                    else {
                        raw.$set(rawError, item.id, {})
                        raw.$set(rawError[item.id], 'earlygoing', true)

                    }

                }




                // Reconsider how to set this up

                // if(item.pfval == null || item.pfval == undefined ){
                //     this.$set(this.errors , 'pfval' , 'Please fill out P.F . Set <b>0</b> for None/Null')
                // }
                // if(item.esival== null || item.esival == undefined ){
                //     this.$set(this.errors , 'esival' , 'Please fill out ESI . Set <b>0</b> for None/Null')
                // }

            })

            if (Object.keys(this.errors).length == 0) {
                return true
            }
            else {
                return false;
            }
        },

    }
})

Vue.component('vue-feather', VueFeather);
