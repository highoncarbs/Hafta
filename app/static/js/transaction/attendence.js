new Vue({
    el: "#attendence_form",
    data() {

        return {
            company: null,
            month: null,
            searchQuery: '',
            currentSort: 'name',
            currentSortDir: 'asc',
            data: null,
            dataList: []
        }
    },
    mounted() {
    },
    computed: {
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
        getEmployee(e) {
            let rawdata = this
            axios.get('/employee/get/basic')
                .then(function (response) {
                    rawdata.data = JSON.parse(response.data)
                    rawdata.dataList = JSON.parse(response.data)

                })
            e.preventDefault();
        }

    }
})

Vue.component('vue-feather', VueFeather);
