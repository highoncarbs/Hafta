
new Vue({
    el: "#firms_template",
    data() {

        return {
            firms: []

        }
    },
    delimiters: ["[[", "]]"],
    mounted() {

        let raw = this
        axios.post('/firms/info').
            then(function (response) {
                raw.firms = JSON.parse(response.data)
            })

    },
    methods: {
        formatedNumber(val) {
            let test = Number(val).toLocaleString('en-IN', { style: 'currency', currency: 'INR' });
            console.log(test)
            return test
        },
    }

})