// Reset all data when changing selection of select employee

new Vue({
    el: "#performance_form",
    data() {

        return {
            company: null,
            errors: {},
            employee: '',
            emp_id: null,

            frommonth: null,
            tomonth: null,

            dataList: [],
            factorList: [],
            factorName: [],
            showEmpSelect: false,
            tempfactor: '',
            rows: []
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
        // filteredFactorObj() {
        //     let tempdataList = this.factorList.filter(data => {
        //         return data.name.toLowerCase().includes(this.tempfactor.toLowerCase())
        //     });

        //     return tempdataList
        //     return this.factorList.filter((option) => {
        //         return option.name
        //             .toString()
        //             .toLowerCase()
        //             .indexOf(this.tempfactor.toLowerCase()) >= 0
        //     })
        // }
    },



    methods: {

        getSelected(option) {
            this.emp_id = option.id
        },
        getSelectedFactor(option , index) {
            this.rows[index].weight = option.weight
            this.rows[index].score = option.score
            // this.rows.index.factor_id = option.id
        },
        getFactor() {
            let rawdata = this
            this.factorList = []
            if (this.emp_id) {
                axios.get('/transaction/get/performance')
                    .then(function (response) {
                        console.log(response.data);
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

            if (this.company && this.frommonth && this.tomonth) {
                this.showEmpSelect = true

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
        removeElement: function (index) {
            this.rows.splice(index, 1);
        },
        addRow: function (e) {
            var elem = document.createElement('tr');
            this.rows.push({
                name: "",
                obt_score: "",
                score: "",
                weight: "",
                factor_id: null

            });
            e.preventDefault();
        },
    }
})