
new Vue({
    el: "#dash_template",
    data() {

        return {
            firms: [],
            latecomers: null,
            earlygoers: null

        }
    },
    delimiters: ["[[", "]]"],
    mounted() {

        let raw = this
        axios.post('/firms/info').
            then(function (response) {
                raw.firms = JSON.parse(response.data)
            })
        axios.post('transaction/attendence/summary/latecomin').
            then(function (response) {
                raw.latecomers = response.data.late
                raw.earlygoers = response.data.early
            })

    },
    methods: {
        formatedNumber(val) {
            let test = Number(val).toLocaleString('en-IN', { style: 'currency', currency: 'INR' });
            console.log(test)
            return test
        },
        parsejson(val) {
            company = JSON.parse(val)
            return company[0].name + ',' + company[0].location[0].name 
        },
        viewReport(id) {
            window.location.href= "/employee/view/detail/"+String(id)
        }
    }

})
Vue.component('vue-feather', VueFeather);
