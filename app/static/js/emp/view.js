new Vue({
    el: '#emp_detail',
    data() {
        return {
            empDetail: null,
            emp_id: null,
            perfDetail: null
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
    }
})