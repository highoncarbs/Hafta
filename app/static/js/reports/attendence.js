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
            let self = this
            axios.post('/employee/get/detail/' + String(id))
                .then(function (response) {
                    self.empDetail = JSON.parse(response.data)
                })
        },
        getAttendence() {
            let self = this
            let attendenceform = { 'company': this.company, 'date': this.month }
            axios.post('/transaction/attendence/get', attendenceform)
                .then(function (response) {
                    self.attendenceList = []
                    console.log(response.data)
                    self.attendenceList = JSON.parse(response.data)


                    // Removes data from dataList if item present in AttendenceList
                    self.attendenceList.forEach(function (item) {
                        if (self.dataList.length != 0)
                            self.dataList.forEach(function (check, index) {
                                if (check.id == item.employee[0].id) {
                                    console.log(check)
                                    self.dataList.splice(index, 1)
                                }

                            })
                    })

                    self.data = self.dataList


                });

        },
        getEmployee(e) {
            let self = this
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
                        // self.data = JSON.parse(response.data)
                        self.dataList = JSON.parse(response.data)
                        self.getAttendence();
                        self.isLoading = false



                    })


                //    Need to pop emps whose data is already been filled
            }
            else {
                this.$set(this.errors, 'submit', "Please select both company and month.")
            }
            e.preventDefault();
        },
        updateData(e) {
            let self = this
            let formdata = { 'company': this.company, 'date': this.month, 'data': this.attendenceList }
            axios.post('/transaction/attendence/update', self.attendenceList)
                .then(function (response) {
                    console.log(response)
                    if (response.data.success) {
                        self.$buefy.snackbar.open({
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
                        self.$buefy.snackbar.open({
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
            let self = this
            
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
                            self.$buefy.snackbar.open({
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

                            self.getAttendence();
                        }
                        else if (response.data.message) {
                            self.$buefy.snackbar.open({
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
