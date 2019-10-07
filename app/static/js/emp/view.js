new Vue({
    el: '#emp_detail',
    data() {
        return {
            empDetail: null,
            emp_id: null,
            perfDetail: null,
            attDetail:[],
            total: {
                days: 0,
                late: 0,
                early: 0,
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
        // getTotalDays() {
        //     this.total.days = this.attDetail.day_att.reduce(function (total, num) { return total + num }, 0);
        //     return this.total.days
        // }

    }
})