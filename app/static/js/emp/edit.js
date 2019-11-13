new Vue({
    el: '#emp_entry',
    data() {
        return {
            filteredBenefits: null,
            benefitsList: null,
            submitting: false,
            value: 'Update',
            formdatasaved: null,
            emp_id: null,
            formdata: {
                name: null,
                dob: null,
                spousename: null,
                fathername: null,
                education: null,
                contact: null,
                curr_address: null,
                curr_city: null,
                perm_address: null,
                perm_city: null,
                pan: null,

                aadhar: null,
                reference: null,
                dateofapp: null,
                appointment: null,
                post: null,
                department: null,
                company: null,
                benefits: [],
                dateeff: null,
                salary_structure: null,
                basicpay: null,
                pf: null,
                esi: null,
                advance: 'allowed',
                bankname: null ,
                accnumber: null ,
                ifsccode: null ,
                advancevalue: null,
                advancenum: null,
                paidleave: null,
                incrementpr: null,
                errors: {}


            },
            formfiles: {
                panfile: null,
                aadharfile: null,
                photofile: null,
                extraidfile: null,
                educertfile: null,
                resumefile: null,


            },
            confirmExit: false
        }
    },
    delimiters: ['[[', ']]'],
    created() {
        let data = this;
        axios.get('/master/get/benefits')
            .then(function (response) {
                data.filteredBenefits = response.data;
                data.benefitsList = response.data;
                console.log(response.data)

            });
        if (confirmExit) {
            window.onbeforeunload = confirmExit;
            function confirmExit() {
                this.confirmExit
                return "You have attempted to leave this page.  If you have made any changes to the fields without clicking the Save button, your changes will be lost.  Are you sure you want to exit this page?";
            }
        }
        feather.replace()


    },
    mounted() {
        let data = this
        emp_fields = ['name', 'dob',
            'spousename',
            'fathername',
            'education',
            'contact',
            'curr_address',
            'perm_address',
            'pan',
            'aadhar',
            'reference',
            'dateofapp',
            'dateeff',
            'salary_structure',
            'basicpay',
            'pf',
            'esi',
            'advance',
            'advancevalue',
            'advancenum',
            'paidleave',
            'incrementpr',
            'benefits'
        ]

        this.emp_id = window.location.href.split('/').slice(-1)[0]

        select_fields = ['post', 'appointment', 'company', 'department']

        axios.post('/employee/edit/' + String(data.emp_id))
            .then(function (response) {
                data.formdatasaved = JSON.parse(response.data)

                emp_fields.forEach(function (key) {
                    Object.keys(data.formdatasaved).forEach(function (subkey) {
                        if (key == subkey) {
                            data.$set(data.formdata, key, data.formdatasaved[subkey])
                        }
                        if (key == 'dateofapp') {
                            tempdate = String(data.formdatasaved[key].split('T')[0])
                            data.$set(data.formdata, key, tempdate)
                        }
                        if (key == 'dateeff') {
                            tempdate = String(data.formdatasaved[key].split('T')[0])
                            data.$set(data.formdata, key, tempdate)
                        }
                        if (key == 'dob') {
                            tempdate = String(data.formdatasaved[key].split('T')[0])
                            data.$set(data.formdata, key, tempdate)
                        }
                    })

                })

                select_fields.forEach(function (key) {
                    Object.keys(data.formdatasaved).forEach(function (subkey) {
                        if (key == subkey) {
                            data.$set(data.formdata, key, String(data.formdatasaved[subkey][0].id))
                        }
                    })

                })


            })
    },
    methods: {
        submitData(e) {
            if (this.checkData(e)) {
                let formData = new FormData()

                this.submitting = true;
                this.value = 'Updating';

                let rawdata = this
                let formdata = {'emp_id' : this.emp_id , 'formdata': this.formdata}
                formData.append('data', JSON.stringify(formdata))

                if (this.formfiles.panfile) {
                    formData.append('panfile', this.formfiles.panfile, this.formfiles.panfile.name)
                }
                if (this.formfiles.photofile) {
                    formData.append('photofile', this.formfiles.photofile, this.formfiles.photofile.name)
                }
                if (this.formfiles.aadharfile) {

                    formData.append('aadharfile', this.formfiles.aadharfile, this.formfiles.aadharfile.name)
                }
                if (this.formfiles.extraidfile) {

                    formData.append('extraidfile', this.formfiles.extraidfile, this.formfiles.extraidfile.name)
                }
                if (this.formfiles.educertfile) {

                    formData.append('educertfile', this.formfiles.educertfile, this.formfiles.educertfile.name)
                }
                if (this.formfiles.resumefile) {

                    formData.append('resumefile', this.formfiles.resumefile, this.formfiles.resumefile.name)
                }
                axios.post('/employee/update', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                    .then(function (response) {
                        if (response.data.success) {
                            rawdata.$buefy.snackbar.open({
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
                            rawdata.confirmExit = true


                        }
                        if (response.data.message) {
                            rawdata.$buefy.snackbar.open({
                                indefinate: true,
                                message: response.data.message,
                                type: 'is-warning',
                                position: 'is-top-right',
                                actionText: 'Close',
                                queue: true,
                                onAction: () => {
                                    this.isActive = false;
                                }
                            })
                        }

                        rawdata.submitting = false;
                        rawdata.value = 'Update';
                    })

                    .catch(function (error) {
                        rawdata.$buefy.snackbar.open({
                            duration: 4000,
                            message: 'Something went wrong . Please check logs.',
                            type: 'is-light',
                            position: 'is-top-right',
                            actionText: 'Close',
                            queue: true,
                            onAction: () => {
                                this.isActive = false;
                            }

                        })
                        console.error(error)

                    })



                e.preventDefault();
            }
            else {
                this.$buefy.snackbar.open({
                    duration: 4000,
                    message: 'Please enter the required data , then submit.',
                    type: 'is-light',
                    position: 'is-top-right',
                    actionText: 'Close',
                    queue: true,
                    onAction: () => {
                        this.isActive = false;
                    }
                })
            }


        },
        getFilteredTags(text) {
            this.filteredBenefits = this.benefitsList.filter((option) => {
                return option.name
                    .toString()
                    .toLowerCase()
                    .indexOf(text.toLowerCase()) >= 0
            })
        },
        checkData(e) {
            this.formdata.errors = []
            if (this.formdata.name && this.formdata.dob && this.formdata.fathername) {
                return true;
            }
            if (!this.formdata.name) {
                this.$set(this.formdata.errors, 'name', "Data required")
            }
            if (!this.formdata.dob) {
                this.$set(this.formdata.errors, 'dob', "Data required")
            }
            if (!this.formdata.fathername) {
                this.$set(this.formdata.errors, 'fathername', "Data required")
            }
            e.preventDefault();
        },
        sameAddress(e) {
            if (this.formdata.curr_address) {
                this.formdata.perm_address = this.formdata.curr_address
                this.formdata.perm_city = this.formdata.curr_city
            }
            else {
                this.$set(this.formdata.errors, 'perm_address', "Values not set for Current Address.")
            }

            e.preventDefault();
        },
        handleFileUpload(field) {

            if (field == 'pan') {
                this.formfiles.panfile = this.$refs.panfile.files[0];

                this.fileUploadType(this.formfiles.panfile.name, field)

            }
            if (field == 'aadhar') {
                this.formfiles.aadharfile = this.$refs.aadharfile.files[0];
                this.fileUploadType(this.formfiles.aadharfile.name, field)

            }
            if (field == 'photo') {
                this.formfiles.photofile = this.$refs.photofile.files[0];
                this.fileUploadType(this.formfiles.photofile.name, field)

            }
            if (field == 'extraidfile') {
                this.formfiles.extraidfile = this.$refs.extraidfile.files[0];
                this.fileUploadType(this.formfiles.extraidfile.name, field)

            }
            if (field == 'educertfile') {
                this.formfiles.educertfile = this.$refs.educertfile.files[0];
                this.fileUploadType(this.formfiles.educertfile.name, field)

            }
            if (field == 'resumefile') {
                this.formfiles.resumefile = this.$refs.resumefile.files[0];
                this.fileUploadType(this.formfiles.resumefile.name, field)

            }
        },
        fileUploadType(type, field) {
            let allowedTypes = ['pdf', 'jpg', 'peg', 'png']
            type = type.split('.')[1]
            if (allowedTypes.includes(type.toLowerCase())) {
                this.$set(this.formdata.errors, field, null)
                return true;
            }
            else {
                this.$set(this.formdata.errors, field, { "error": "Please upload pdf,jpg ,jpeg or png file" })

                return false;
            }
        }
    }
})

Vue.use('route')