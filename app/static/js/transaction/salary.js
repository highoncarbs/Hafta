
new Vue({
    el: "#salary_sheet_form",
    data() {
        return {
            company: null,
            month: null,
            isGenerating: null,
            errors: {},
            salarySheet: null
        }
    },
    delimiters: ['[[', ']]'],
    methods: {
        generateSalarySheet() {
            console.log("DAD")
            if (this.checkData()) {
                this.isGenerating = true
                let rawdata = this
                let formdata = { 'company': this.company, 'month': this.month }
                axios.post('/transaction/salary_sheet/generate', formdata)
                    .then(function (response) {
                        rawdata.salarySheet = response.data

                        rawdata.isGenerating = null;
                    })
                    .catch(function (error) {
                        rawdata.$buefy.snackbar.open({
                            duration: 4000,
                            message: 'Salary sheet could not be geenrated. Please check logs.',
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }
                        })

                        rawdata.isGenerating = null;

                    })
            }
            else {


            }

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
        }
    }

})

Vue.component('vue-feather', VueFeather);
