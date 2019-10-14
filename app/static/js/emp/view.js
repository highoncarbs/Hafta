new Vue({
    el: '#emp_detail',
    data() {
        return {
            empDetail: null,
            emp_id: null,
            perfDetail: null,
            attDetail: [],
            viewUpload: false,
            total: {
                days: 0,
                late: 0,
                early: 0,
            },
            viewFile: null,
            fileSrc: null,
            isPdf: {
                pan: false,
                aadhar: false,
                extraid: false,
                educert: false,
                resume: false,
            },
            date: null,
            slip: null,
            slipNone: false,
            quickReports: null
        }

    },
    delimiters: ['[[', ']]'],
    mounted() {
        this.emp_id = window.location.href.split('/').slice(-1)[0]
        let raw = this
        if (this.emp_id != null) {
            axios.post('/employee/get/detail/' + String(this.emp_id))
                .then(function (response) {
                    raw.empDetail = JSON.parse(response.data)
                    if (raw.empDetail.panfile) {
                        // console.log(raw.empDetail.panfile.split('.')[raw.empDetail.panfile.length -1])
                        temp = raw.empDetail.panfile.split('.')
                        if (temp[temp.length - 1] == 'pdf')
                            raw.isPdf.pan = true
                    }
                    if (raw.empDetail.aadharfile) {
                        // console.log(raw.empDetail.panfile.split('.')[raw.empDetail.panfile.length -1])
                        temp = raw.empDetail.aadharfile.split('.')
                        if (temp[temp.length - 1] == 'pdf')
                            raw.isPdf.aadhar = true
                    }
                    if (raw.empDetail.educertfile) {
                        // console.log(raw.empDetail.panfile.split('.')[raw.empDetail.panfile.length -1])
                        temp = raw.empDetail.educertfile.split('.')
                        if (temp[temp.length - 1] == 'pdf')
                            raw.isPdf.educert = true
                    }
                    if (raw.empDetail.extraidfile) {
                        // console.log(raw.empDetail.panfile.split('.')[raw.empDetail.panfile.length -1])
                        temp = raw.empDetail.extraidfile.split('.')
                        if (temp[temp.length - 1] == 'pdf')
                            raw.isPdf.extraid = true
                    }
                    if (raw.empDetail.resumefile) {
                        // console.log(raw.empDetail.panfile.split('.')[raw.empDetail.panfile.length -1])
                        temp = raw.empDetail.resumefile.split('.')
                        if (temp[temp.length - 1] == 'pdf')
                            raw.isPdf.resume = true
                    }
                })

            axios.get('/transaction/performance/get/employee/' + String(this.emp_id))
                .then(function (response) {
                    raw.perfDetail = JSON.parse(response.data)
                })
            axios.get('/transaction/attendence/employee/' + String(this.emp_id))
                .then(function (response) {
                    raw.attDetail = JSON.parse(response.data)

                })

            if (this.emp_id != null) {
                let today = new Date 
                let fromdate = today.getFullYear()+'-01-01'
                let todate = today.getFullYear() + '-12-31'
                let rawdata = this
                let reportdata = { 'emp_id': this.emp_id, 'fromdate': fromdate, 'todate': todate }
                axios.post('/transaction/quick/get', reportdata)
                    .then(function (response) {
                        rawdata.quickReports = JSON.parse(response.data)
                    })
            }
        }




    },
    watch: {
        attDetail: function (val) {

            this.total.days = val.day_att.reduce(function (total, num) { return total + num }, 0);
            this.total.late = val.late_att.reduce(function (total, num) { return total + num }, 0);
            this.total.early = val.early_att.reduce(function (total, num) { return total + num }, 0);
        }
    },
    methods: {
        formatedNumber(val) {
            let test = Number(val).toLocaleString('en-IN', { style: 'currency', currency: 'INR' });
            return test
        },
        formatedDate(val) {
            var date = new Date(val)
            return (date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear());


        },
        showUpload(filetype) {
            this.viewFile = filetype
            if (this.viewFile != null) {
                this.viewUpload = !this.viewUpload
                this.fileSrc = String('\\static') + String(this.empDetail[this.viewFile]).split('\static')[1]
            }
        },
        viewPDF(filetype) {
            this.viewFile = filetype
            if (this.viewFile != null) {

                this.fileSrc = String('\\static') + String(this.empDetail[this.viewFile]).split('\static')[1]
                window.open(this.fileSrc, '_blank')
            }
        },
        getSlip() {
            let raw = this
            let formdata = { 'emp_id': this.emp_id, 'date': this.date }
            axios.post('/transaction/salary_sheet/slips', formdata)
                .then(function (response) {
                    let payload = response.data
                    if (payload.success) {

                        raw.slipNone = false
                        raw.slip = payload.success
                    }

                    if (payload.message) {
                        raw.slip = null
                        raw.slipNone = true
                    }


                })
        },
        printSelected() {
            let rawdata = this
            localStorage.clear()
            let selectedData = []
            selectedData.push(this.slip)
            let formdata = { 'company': this.empDetail.company, 'date': this.date, 'data': selectedData }
            localStorage.setItem('selecteddata', JSON.stringify(formdata))
            axios.post('/transaction/salary_sheet/print/selected', formdata)
                .then(function (response) {
                    const win = window.open('/transaction/salary_sheet/print/selected', '_blank', [], true);
                })
        }
    }
})