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
            }
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
            console.log(test)
            return test
        },
        formatedDate(val) {
            var date = new Date(val)
            console.log(date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear())
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
                window.open(this.fileSrc , '_blank')
            }
        }
        // getTotalDays() {
        //     this.total.days = this.attDetail.day_att.reduce(function (total, num) { return total + num }, 0);
        //     return this.total.days
        // }

    }
})