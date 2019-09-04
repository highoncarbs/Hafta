const LocationView =
{
    template: `  
      <div class="table-container">
    <table class="table">
        <thead>
            <tr>
                <td></td>
                <td>Name</td>
                <td>Action</td>
            </tr>

        </thead>
        <tbody>
            <tr>
                <td></td>
                <td>Bagru</td>
                <td>Edit , Delete</td>
            </tr>
        </tbody>
    </table>
</div>
    `,
    data() {
        return {
            form: {
                errors: [],
                name: null,
            },
        }
    },
    delimiters: ["[[", "]]"], 
    mounted() {
        console.log("Component Mounted");
    },
    methods: {
        checkData(e) {
            if (this.form.name && this.form.location) {
                return true;
            }

            this.form.errors = []

            if (!this.form.name) {
                this.form.errors.push('Location required');
            }
           

            e.preventDefault();
        },
        submitData(e) {
            this.checkData(e);
            if (this.form.errors.length == 0) {
                axios
                    .post('{{url_for("master.add_location")}}', this.form)
                    .then(function (response) {
                        console.log(response);
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            }
            e.preventDefault();
        }

    }
}
