<template>
  <div>
    <div class="has-background-white" style="border-top: 1px solid #eee">
      <div
        class="section py-4 pt-5 is-fullwidth is-fullheight"
        :class="{ 'container px-0': $store.state.win }"
      >
        <!-- <transition name="fade"> -->
        <p class="is-size-5 has-text-weight-bold">Quick Report</p>
        <br />
        <!-- Filtere -->
        <b-field grouped group-multiline>
          <b-field label-position="on-border" label="Show">
            <b-select
              @input="loadAsyncData"
              v-model="showItems"
              icon="filter-variant"
            >
              <option value="20">20</option>
              <option value="40">40</option>
              <option value="60">60</option>
              <option value="100">100</option>
            </b-select>
          </b-field>
          <b-field expanded label-position="on-border" label="Search">
            <b-input
              @keypress.native.enter="loadAsyncData"
              placeholder="Search Employees"
              icon="magnify"
              v-model="query"
            ></b-input>
          </b-field>
          <b-field label-position="on-border" label="Company">
            <b-select
              @input="loadAsyncData"
              v-model="filter_company"
              placeholder="Select Company"
            >
              <option
                v-for="(item, index) in data_company"
                :key="'company_' + index"
                :value="item.id"
              >
                {{ titleCase(item.name) }}
              </option>
            </b-select>
          </b-field>
          <b-field label-position="on-border" label="Advances">
            <b-select
              @input="loadAsyncData"
              v-model="filter_advance"
              placeholder="Filter Advances"
            >
              <option value="jta">Jai Texart</option>
            </b-select>
          </b-field>
          <b-field>
            <div class="buttons">
              <button @click="loadAsyncData" class="button is-link">
                Search
              </button>
              <button @click="clearFields" class="button">Clear</button>
            </div>
          </b-field>
        </b-field>
        <!-- End Filters -->
        <br />
        <b-table
          :empty="data.length == 0"
          paginated
          backend-pagination
          @page-change="onPageChange"
          :per-page="showItems"
          @change="onPageChange"
          :current.sync="currentPage"
          :pagination-simple="false"
          :pagination-position="'bottom'"
          :data="data"
          :loading="loading"
          :range-before="3"
          :range-after="1"
          :total="totalItems"
          v-model="currentPage"
        >
          <template slot="empty">
            <div class="has-text-centered my-6 py-6">
              <b-icon
                icon="account-multiple-plus"
                size="is-large"
                class="has-text-grey-lighter"
              ></b-icon>
              <p
                class="is-size-5 has-text-grey-light has-text-weight-medium mt-4"
              >
                Theres nothing to see here. <br />
                Go add some data
              </p>
            </div>
          </template>
          <b-table-column label="Name" v-slot="props"
            >{{ props.row.name }}
          </b-table-column>
          <b-table-column label="Company" v-slot="props"
            >{{ props.row.company[0].name }}
          </b-table-column>
          <b-table-column label="Salary" v-slot="props"
            >{{ formatedNumber(props.row.basicpay) }}
          </b-table-column>
          <b-table-column label="Adv. Taken" v-slot="props">
            {{ formatedNumber(props.row.adv_total) }}
          </b-table-column>
          <b-table-column label="Adv. Pending" v-slot="props">
            {{ formatedNumber(props.row.outstanding) }}
          </b-table-column>
          <b-table-column label="" v-slot="props">
            <div class="buttons">
              <button class="button is-link" @click="giveAdvance(props.row.id)">
                <b-icon icon="comment-plus"></b-icon>
              </button>
              <!-- <button class="button is-link is-light">
                <b-icon icon="pencil"></b-icon>
              </button> -->
              <button class="button is-link is-light">
                <b-icon icon="eye"></b-icon>
              </button>
              <button class="button" @click="checkLedger(props.row)">
                <b-icon icon="poll-box"></b-icon>
              </button>
            </div>
          </b-table-column>
        </b-table>
      </div>
    </div>
    <b-sidebar
      mobile="fullwidth"
      type="is-white"
      :fullheight="true"
      :overlay="true"
      :right="true"
      :open.sync="showAdvLedger"
    >
      <div class="my-4 px-4">
          <div class="level my-0"  v-if="employee_adv_deets != null"
         >
              <div class="level-left">
                  <div class="level-item">
                       <p
          class="has-text-weight-medium is-size-5"
        >
          Reports for {{ this.employee_adv_deets.name }}
        </p>
                  </div>
              </div>
              <div class="level-right">
                  <div class="level-item">
                      <p class="delete" @click="showAdvLedger = !showAdvLedger"></p>
                  </div>
              </div>
          </div>
       
        <hr class="my-2" />
       
        <br />
        <b-table :data="quickReports" :empty="quickReports.length == 0">
                    <template slot="empty">
                      <div class="my-6 has-text-centered">
                        
                        <b-icon icon="table-remove" size="is-medium" class="has-text-grey-light"></b-icon>
                      <p class="has-text-weight-medium has-text-grey">No Reports Added</p>
                      </div>
                    </template>
                    <b-table-column v-slot="props" label="Date">{{ formatedDate(props.row.date) }}</b-table-column>
                    <b-table-column v-slot="props" label="Feedback">
<span  class="tag heading has-text-weight-medium is-rounded"
                          :class="{
                            'is-danger':
                              props.row.feedback == 'negative',
                            'is-info': props.row.feedback == 'positive',
                          }"
                        >
                          {{ props.row.feedback }}</span>

                    </b-table-column>
                    <b-table-column v-slot="props" label="Report">{{ props.row.report }}</b-table-column>
                  </b-table>
      </div>
    </b-sidebar>
    <b-modal v-model="showAdvModal">
      <div class="box pt-3 px-0">
        <div class="px-4">
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <p class="is-size-5 mt-4 has-text-weight-semibold">
                  New Quick Report
                  <span
                    class="has-text-weight-normal"
                    v-if="employee_adv_deets != null"
                  >
                    - {{ employee_adv_deets.name }}</span
                  >
                </p>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <div class="buttons">
                  <button @click="showAdvLedger = !showAdvLedger" class="button is-link">
                    <b-icon icon="table-eye"></b-icon>
                    <span class="ml-2">
                      <!-- TODO: Triggers Side bar for Advances List -->
                      View Reports
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <b-field grouped>
            <div class="control">
              <b-field>
                <b-field :type="{ 'is-danger': errors.date }" label="Date">
                  <b-datepicker
                    v-model="form.date"
                    :dob-formatter="dobFormatter"
                  >
                  </b-datepicker>
                </b-field>
              </b-field>
            </div>
          </b-field>
          <div class="control">
            <b-field>
              <b-field
                :type="{ 'is-danger': errors.feedback }"
                label="Feedback"
              >
                <b-radio v-model="form.feedback" native-value="positive"
                  >Positive</b-radio
                >
                <b-radio v-model="form.letter" native-value="negetaive"
                  >Negetaive</b-radio
                >
              </b-field>
            </b-field>
          </div>
          <br />
          <b-field :type="{ 'is-danger': errors.report }" label="Report">
            <b-input
              v-model="form.report"
              maxlength="500"
              type="textarea"
              placeholder="Enter report"
            ></b-input>
          </b-field>

          <button @click="submitData" class="button is-black">
            <b-icon icon="check"></b-icon>
            <span class="ml-3">Save</span>
          </button>
          <button class="button is-link is-fullwidth is-hidden">
            <b-icon icon="check"></b-icon>
            <span class="ml-3">Done</span>
          </button>
        </div>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showAdvLedger: false,
      showLedger: false,
      quickReports:[],
      data: [],
      errors: {},
      set_disabled: false,
      data_company: [],
      advance_list: [],
      showAdvModal: false,
      showAdvLedger: false,
      loading: false,
      showItems: 20,
      totalItems: 20,
      currentPage: 1,
      query: null,
      form: {
        feedback: null,
        date: null,
        report: null,
      },
      emp_id: null,
      filter_company: null,
      filter_advance: null,
      employee: null,
      employee_adv_deets: null,
    };
  },
  mounted() {
    this.loadAsyncData();
    this.$axios.get("/master/get/company").then((response) => {
      this.data_company = response.data;
    });
  },
  methods: {
    getSelected(option) {
      this.emp_id = option.id;
    },
    formatedNumber(val) {
      let test = Number(val).toLocaleString("en-IN", {
        style: "currency",
        currency: "INR",
      });
      return test;
    },
    formatedNumberNoCurr(val) {
      let test = Number(val).toLocaleString("en-IN");
      return test;
    },
    formatedDate(val) {
      var date = new Date(val);
      return (
        date.getDate() + "/" + (date.getMonth() + 1) + "/" + date.getFullYear()
      );
    },
    employeeDetail(id) {
      this.detailModal = !this.detailModal;
      let self = this;
      this.$axios
        .post("/employee/get/detail/" + String(id))
        .then(function (response) {
          self.empDetail = JSON.parse(response.data);
        });
    },
    getAdvanceDetail(e) {
      let self = this;

      if (this.emp_id != null) {
        this.$axios
          .post("/transaction/advance/employee/" + String(this.emp_id))
          .then(function (response) {
            console.log(response.data);
            self.empAdvanceDetail = JSON.parse(response.data);
            self.getAdvanceList();
            self.showAdvList = true;
          })
          .catch(function (error) {
            console.log(error);
          });
      } else {
        this.form.errors = {};
        console.log("NUll ID");
        this.$set(this.form.errors, "empadv", "Null ID for employee");
      }

      e.preventDefault();
    },

    getOutstandingAdvance() {
      let outstandingamt = Number(0);
      if (this.advance_list != null) {
        this.advance_list.forEach(function (item) {
          console.log(item);
          if (item.trans != "debit") {
            outstandingamt += Number(item.advanceamt);
          } else if (item.trans == "debit") {
            outstandingamt -= Number(item.advanceamt);
          }
        });
      }
      this.form.totalAdvance = Number(outstandingamt);
      return this.formatedNumber(outstandingamt);
    },
    getEmployee(e) {
      let self = this;
      this.form.errors = {};
      this.data = null;
      this.dataList = [];
      this.attModal = false;
      this.showEditTable = false;
      if (this.company && this.month) {
        this.$axios
          .get("/employee/get/by/company/" + String(this.company))
          .then(function (response) {
            console.log(response.data);
            self.dataName = [];
            self.dataList = JSON.parse(response.data);
            self.showEmpSelect = true;
            self.employee = "";
            self.showAdvList = false;
            self.dataList.forEach((item) => self.dataName.push(item));
          });

        //    Need to pop emps whose data is already been filled
      } else {
        this.$set(
          this.form.errors,
          "submit",
          "Please select both company and month."
        );
      }
      e.preventDefault();
    },
    submitData() {
      if (this.checkData()) {
        this.submitting = true;
        let raw = this;
        let formdata = {
          emp_id: this.emp_id,
          date: this.form.date,
          report: this.form.report,
          feedback: this.form.feedback,
        };
        this.$axios
          .post("/transaction/quick/add", formdata)
          .then(function (response) {
            if (response.data.success) {
              raw.$buefy.snackbar.open({
                duration: 4000,
                message: response.data.success,
                type: "is-light",
                position: "is-top-right",
                actionText: "Close",
                queue: true,
                onAction: () => {
                  this.isActive = false;
                },
              });
              raw.form.feeback = null;
              raw.form.report = null;
              raw.form.date = null;
              raw.selected = null;
            } else if (response.data.message) {
              raw.$buefy.snackbar.open({
                duration: 4000,
                message: response.data.message,
                type: "is-light",
                position: "is-top-right",
                actionText: "Close",
                queue: true,
                onAction: () => {
                  this.isActive = false;
                },
              });
            }
            raw.submitting = false;
          })
          .catch(function (error) {
            console.log(error);
            raw.submitting = false;
          });
      }
    },
    viewAdvances() {
      this.advEdit = !this.advEdit;
    },
    checkData() {
      this.errors = {};
      if (!this.form.feedback) {
        this.$set(this.errors, "feedback", true);
      }
      if (!this.form.date) {
        this.$set(this.errors, "date", true);
      }
      if (!this.form.report) {
        this.$set(this.errors, "report", true);
      }
        console.log('BOOm---',Object.keys(this.errors).length)
      if (Object.keys(this.errors).length == 0) {
        return true;
      }
    },
    editEmployee() {
      window.location.href = "/employee/edit/view/" + String(this.emp_id);
    },
    deleteAdvance(id, index) {
      let self = this;
      this.$axios
        .post("/transaction/advance/delete/" + String(id))
        .then(function (response) {
          if (response.data.success) {
            self.empAdvanceList.splice(index, 1);
            self.$buefy.snackbar.open({
              duration: 4000,
              message: response.data.success,
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                this.isActive = false;
              },
            });
          } else if (response.data.message) {
            self.$buefy.snackbar.open({
              duration: 4000,
              message: response.data.message,
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                this.isActive = false;
              },
            });
          }
        });
    },
    giveAdvance(emp_id) {
        this.emp_id = emp_id;
        console.log('oko---',emp_id)
      this.showAdvModal = !this.showAdvModal;
    },
    checkLedger(emp) {
        this.employee_adv_deets = emp
         let today = new Date();
        let fromdate = today.getFullYear() + "-01-01";
        let todate = today.getFullYear() + "-12-31";
        let self = this;
        let reportdata = {
          emp_id: emp.id,
          fromdate: fromdate,
          todate: todate,
        };
        this.$axios
          .post("/transaction/quick/get", reportdata)
          .then(function (response) {
            self.quickReports = response.data;
            self.showAdvLedger = !self.showAdvLedger;
          });
    //   this.$axios
    //     .get("/transaction/advance/employee/" + emp_id)
    //     .then((response) => {
    //       this.employee_adv_deets = response.data;
    //       this.showLedger = !this.showLedger;
    //       this.$axios
    //         .get("/transaction/advance/get/" + emp_id)
    //         .then((response) => {
    //           this.advance_list = response.data;
    //           if (
    //             this.advance_list.length >= this.employee_adv_deets.advancenum
    //           ) {
    //             this.set_disabled = true;
    //           } else {
    //             this.set_disabled = false;
    //           }
    //         });
    //     });
    },
    clearFields() {
      this.query = null;
      this.showItems = 20;
      this.totalItems = null;
      this.currentPage = 1;
      this.filter_company = null;
      this.filter_advance = null;
      this.employee = null;
    },
    onPageChange(page) {
      this.currentPage = page;

      this.loadAsyncData();
    },
    getTotalDebit() {
      return this.advance_list.reduce(function (total, value) {
        return value.trans == "debit" ? total + value.advanceamt : total + 0;
      }, 0);
    },
    getTotalCredit() {
      let tota = this.advance_list.reduce(function (total, value) {
        console.log(total, value);
        return value.trans == "credit" ? total + value.advanceamt : total + 0;
      }, 0);
      console.log("ggg", tota);
      return tota;
    },
    loadAsyncData() {
      let params = [
        `page=${this.currentPage}`,
        `show=${this.showItems}`,
        `query=${this.query}`,
        `company=${this.filter_company}`,
      ].join("&");
      let self = this;
      this.$axios.get("/employee/get/advance?" + params).then((response) => {
        self.data = response.data.data;
        self.totalItems = response.data.total;
      });
    },
  },
};
</script>

<style>
.success-bg {
  position: relative;
  /* border-radius: 5px 5px 0 0; */
  background-color: blue;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='20' viewBox='0 0 100 20' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M21.184 20c.357-.13.72-.264 1.088-.402l1.768-.661C33.64 15.347 39.647 14 50 14c10.271 0 15.362 1.222 24.629 4.928.955.383 1.869.74 2.75 1.072h6.225c-2.51-.73-5.139-1.691-8.233-2.928C65.888 13.278 60.562 12 50 12c-10.626 0-16.855 1.397-26.66 5.063l-1.767.662c-2.475.923-4.66 1.674-6.724 2.275h6.335zm0-20C13.258 2.892 8.077 4 0 4V2c5.744 0 9.951-.574 14.85-2h6.334zM77.38 0C85.239 2.966 90.502 4 100 4V2c-6.842 0-11.386-.542-16.396-2h-6.225zM0 14c8.44 0 13.718-1.21 22.272-4.402l1.768-.661C33.64 5.347 39.647 4 50 4c10.271 0 15.362 1.222 24.629 4.928C84.112 12.722 89.438 14 100 14v-2c-10.271 0-15.362-1.222-24.629-4.928C65.888 3.278 60.562 2 50 2 39.374 2 33.145 3.397 23.34 7.063l-1.767.662C13.223 10.84 8.163 12 0 12v2z' fill='%239C92AC' fill-opacity='0.2' fill-rule='evenodd'/%3E%3C/svg%3E");
  padding: 1rem 0.5rem;
}
</style>
<style scoped>
.b-sidebar {
  z-index: 99 !important;
}
</style>