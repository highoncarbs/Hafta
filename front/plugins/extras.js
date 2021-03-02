import Vue from 'vue'

Vue.mixin({
    methods: {
        formatedNumberNoCurr(val) {
            let test = Number(val).toLocaleString("en-IN");
            return test;
          },
        formatDate(date) {
            let temp_date = new Date(date);
            return temp_date.toLocaleDateString("en-IN");
        },
        dobFormatter(date) {
            console.log('BBOm----', date)
            let options = { year: "numeric", month: "numeric", day: "numeric" };

            return date.toLocaleDateString("en-IN", options);
        },
        getNormalImage(path, type) {
            let new_path = ""

            console.log(process.env.NODE_ENV)
            if (process.env.NODE_ENV == 'development') {
                new_path = String(path).split('uploads')[1]
                console.log('--' , new_path)
            } 
            if (new_path != "") {
                if (type == "normal_jpg") {
                    let fileSrc =
                        process.env.static_path + "/unsafe/fit-in/500x/filters:quality(80):fill(white)/" + process.env.static_base +
                        String(new_path);
                    console.log('--', new_path)
                    return fileSrc
                }
                if (type == "normal") {
                    let fileSrc =
                        process.env.static_path + "/unsafe/fit-in/500x/filters:quality(80):format(webp):fill(white)/" + process.env.static_base +
                        String(new_path);
                    console.log('--', new_path)
                    return fileSrc
                }
                if (type == "thumb") {
                    let fileSrc =
                        process.env.static_path + "/unsafe/96x/filters:format(webp):quality(70)/" + process.env.static_base +
                        String(new_path);
                    return fileSrc;
                }
                if (type == "small") {
                    let fileSrc =
                        process.env.static_path + "/unsafe/250x/filters:format(webp):quality(70)/" + process.env.static_base +
                        String(new_path);
                    return fileSrc;
                }
                if (type == "large") {
                    let fileSrc =
                        process.env.static_path + "/unsafe/filters:format(webp)/" + process.env.static_base +
                        String(new_path);
                    return fileSrc;
                }
            }
            return null;
        },
        numtoWords(num) {
            var a = ['', 'one ', 'two ', 'three ', 'four ', 'five ', 'six ', 'seven ', 'eight ', 'nine ', 'ten ', 'eleven ', 'twelve ', 'thirteen ', 'fourteen ', 'fifteen ', 'sixteen ', 'seventeen ', 'eighteen ', 'nineteen '];
            var b = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];

            if ((num = Number(num).toString()).length > 9) return 'overflow';
            let n = ('000000000' + num).substr(-9).match(/^(\d{2})(\d{2})(\d{2})(\d{1})(\d{2})$/);
            if (!n) return; var str = '';
            str += (n[1] != 0) ? (a[Number(n[1])] || b[n[1][0]] + ' ' + a[n[1][1]]) + 'crore ' : '';
            str += (n[2] != 0) ? (a[Number(n[2])] || b[n[2][0]] + ' ' + a[n[2][1]]) + 'lakh ' : '';
            str += (n[3] != 0) ? (a[Number(n[3])] || b[n[3][0]] + ' ' + a[n[3][1]]) + 'thousand ' : '';
            str += (n[4] != 0) ? (a[Number(n[4])] || b[n[4][0]] + ' ' + a[n[4][1]]) + 'hundred ' : '';
            str += (n[5] != 0) ? ((str != '') ? 'and ' : '') + (a[Number(n[5])] || b[n[5][0]] + ' ' + a[n[5][1]]) + 'only ' : '';
            return str;

        },
        titleCase(str) {
            return str.toLowerCase().split(' ').map(function (word) {
                return (word.charAt(0).toUpperCase() + word.slice(1));
            }).join(' ');
        },
        getLocalPrice(item) {
            // Add local currency
            let currency = this.$auth.user.roles.currency;
            if (Object.keys(this.$auth.user.roles).includes('price') && this.$auth.user.roles.price) {

                if (currency.name == "INR") {
                    return (
                        Math.round(
                            ((item.price + Number.EPSILON) * 10) /
                            currency.exchange
                        ) / 10
                    ).toFixed(2);
                } else {
                    let number = (item.price * item.product_category[0].factor) /
                        currency.exchange

                    return (this.get_ceil(number, 1)).toFixed(2);
                    // return (
                    //     Math.round(
                    //         (item.price * item.product_category[0].factor * 10) /
                    //         this.$auth.user.roles.currency[0].exchange
                    //     ) / 10
                    // ).toFixed(2);
                }
            }
            else return 0.0
        },
        get_ceil(number, digits) {
            return parseFloat(Math.ceil((10.0 ** digits) * number) / (10.0 ** digits))
        },
        getPriceBy(item, curr) {
            // Add local currency

            let currency = curr;

            if (currency.name == "INR") {
                return (
                    Math.round(
                        ((item.price + Number.EPSILON) * 10)
                    ) / 10
                ).toFixed(2);
            } else {
                let number = (item.price * item.product_category[0].factor) /
                    currency.exchange

                return (this.get_ceil(number, 1)).toFixed(2);
            }

        },
        convertBy(price, curr) {
            // Add local currency

            let currency = curr;

            if (currency.name == "INR") {
                return (
                    Math.round(
                        ((price + Number.EPSILON) * 10)
                    ) / 10
                ).toFixed(2);
            } else {
                let number = (price) /
                    currency.exchange

                return (this.get_ceil(number, 1)).toFixed(2);
            }

        },
    }
})

