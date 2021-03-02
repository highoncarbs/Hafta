<template>
  <div>
    <div class="has-background-white" style="border-top: 1px solid #eee">
      <div
        class="section py-4 pt-5 is-fullwidth is-fullheight"
        :class="{ 'container px-0': $store.state.win }"
      >
        <!-- <transition name="fade"> -->
        <div v-if="showView">
          <p class="is-size-5 has-text-weight-bold">Firms</p>
          <br />
          <div class="columns">
            <div
              class="column is-3"
              v-for="(item, index) in data_company"
              :key="index"
            >
              <div class="box">
                
                <p class="is-size-4 has-text-weight-bold">
                  {{ titleCase(item.name) }}
                </p>
                <hr class="my-2" />
                <p class="is-size-5 mt-2">{{ item.num }} Employees</p>
                <p class="is-size-5 is-family-monospace">
                  INR {{ item.payout.toLocaleString("en-IN") }}
                </p>
                
    <br>
               <p
                  class="tag heading is-rounded is-warning "
                  v-if="item.sal_status == 'pending'"
                >
                  <span class="dot-warning"></span>
                  SALARY PENDING -
                  {{ new Date().toLocaleString("default", { month: "short" }) }}
                  <!-- <span class="ml-3">
                      <b-icon icon="arrow-right-circle" size="is-small"></b-icon>
                  </span> -->
                </p>
                <p
                  class="tag heading is-rounded is-info "
                  v-if="item.sal_status == 'done'"
                >
                  <span class="dot-link"></span>
                  SALARY PROCESSED -
                  {{ new Date().toLocaleString("default", { month: "short" }) }}
                </p>
                 <p class="tag heading is-rounded  is-warning " v-if="item.att_status == 'pending'">
                  <span class="dot-warning"></span>
                  Attendence pending - {{ new Date().toLocaleString('default', { month: 'short' })}}
                </p>
                <p class="tag heading is-rounded is-info " v-if="item.att_status == 'done'">
                  <span class="dot-link"></span>
                  Attendence Done - {{ new Date().toLocaleString('default', { month: 'short' })}}
                </p>

              </div>
            </div>
          </div>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showView: true,
      company: null,
      month: null,
      searchQuery: "",
      currentSort: "name",
      currentSortDir: "asc",
      data_company: [],
      data: null,
      company: null,
      month: null,
      isGenerating: null,
      errors: {},
      salarySheet: null,
      currSheetStatus: null,
      selectedRow: [],
      salarySheetView: null,
      dataList: [],
      detailModal: false,
      empDetail: null,
      errors: [],
      attendenceList: [],
      attModal: false,
      showEditTable: false,
      value: "Save",
      submitting: false,
      showEmpSelect: false,
      isLoading: false,
    };
  },
  mounted() {
    this.$axios.get("/master/get/company/detail").then((response) => {
      this.data_company = response.data;
      this.data_company.forEach((item) => {
        this.$axios
          .post("/transaction/salary_sheet/status", {
            id: item.id,
            date: new Date(),
          })
          .then((response) => {
            this.$set(item, "sal_status", response.data.status);
          });
        
         this.$axios.post('/transaction/attendence/status', {'id':item.id , 'date': new Date()}).then (response =>{
          this.$set(item , 'att_status', response.data.status)
        })
      });
    });
  },
  computed: {
    salarySheetEdit() {
      if (this.salarySheet != null) {
        this.salarySheet.forEach(function (row) {
          row.total_deductions =
            parseFloat(row.net_adv_deduction) ||
            0 +
              parseFloat(row.esi) +
              parseFloat(row.pf) +
              parseFloat(row.tds) +
              parseFloat(row.other_deduction) +
              parseFloat(0);
          const tempPay = row.pay_1;
          row.net_payable = Math.round(
            parseFloat(tempPay) - parseFloat(row.total_deductions)
          );
        });
      }

      return this.salarySheet;
    },
  },
  methods: {
    generateSalarySheet(company) {
      let self = this;
      console.log(this.checkData());
      if (this.checkData()) {
        this.company = company;
        this.isGenerating = true;
        let self = this;
        let formdata = { company: company.id, month: this.month };
        let checkformdata = { company: company.id, date: this.month };
        self.showView = !self.showView;
        this.$axios
          .post("/transaction/salary_sheet/status", {
            id: company.id,
            date:this.month,
          })
          .then((response) => {
            this.currSheetStatus= response.data.status;
          });
        this.$axios
          .post("/transaction/salary_sheet/get/processed", checkformdata)
          .then(function (response) {
            if (response.data.data) {
              self.salarySheet = response.data.data;
            } else {
              self.$axios
                .post("/transaction/salary_sheet/generate", formdata)
                .then(function (response) {
                  if (response.data.message) {
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
                    self.salarySheet = null;
                  } else {
                    self.salarySheet = response.data;
                    console.log(response.data);
                    console.log(self.salarySheet);
                  }
                })
                .catch(function (error) {
                  self.$buefy.snackbar.open({
                    duration: 4000,
                    message:
                      "Salary sheet could not be geenrated. Please check logs.",
                    type: "is-light",
                    position: "is-top-right",
                    actionText: "Close",
                    queue: true,
                    onAction: () => {
                      self.isActive = false;
                    },
                  });
                });
            }
          })
          .catch(function (error) {
            console.log(error);
          })
          .finally(() => {
            this.isGenerating = false;
          });
      }
    },
    formatedNumber(val) {
      let test = Number(val).toLocaleString("en-IN");
      return test;
    },

    checkData() {
      this.errors = {};

      if (!this.month) {
        this.$set(this.errors, "month", true);
      }

      if (Object.keys(this.errors).length === 0) {
        return true;
      } else {
        return false;
      }
    },
    printAll() {
      let self = this;
      localStorage.clear();
      let formdata = {
        company: this.company,
        date: this.month,
        data: this.salarySheet,
      };
      console.log(this.salarySheet);
      localStorage.setItem("jsondata", JSON.stringify(formdata));
       window.open(
        "/print/salary-sheet-all",
        "_blank",
        [],
        true
      );
    },
    printSavedAll() {
      let self = this;
      localStorage.clear();
      let formdata = {
        company: this.company,
        date: this.month,
        data: this.salarySheetView,
      };
      localStorage.setItem("jsondata", JSON.stringify(formdata));
      window.open(
        "/transaction/salary_sheet/print/all",
        "_blank",
        [],
        true
      );
    },
    pushRow(index) {
      console.log(index);
      let raw = this;
      if (this.selectedRow.includes(index)) {
        this.selectedRow.filter(function (item) {
          if (item == index) {
            console.log(item, index, raw.selectedRow);
            raw.selectedRow.splice(raw.selectedRow.indexOf(item), 1);
          }
        });
      } else {
        this.selectedRow.push(index);
      }
    },
    printSelected() {
      let self = this;
      let selectedData = [];
      this.selectedRow.forEach(function (index) {
        selectedData.push(self.salarySheet[self.selectedRow.indexOf(index)]);
      });
      let formdata = {
        company: this.company,
        date: this.month,
        data: selectedData,
      };
      localStorage.setItem("selecteddata", JSON.stringify(formdata));
      window.open(
        "/print/salary-sheet-selected",
        "_blank",
        [],
        true
      );
    },
    processSalary() {
      let self = this;
      let formdata = {
        company: this.company.id,
        date: this.month,
        data: this.salarySheet,
      };
      this.$axios
        .post("/transaction/salary_sheet/process", formdata)
        .then(function (response) {
          if (response.data.success) {
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
  },
};
</script>

<style>
.dot-warning {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 0.7rem;
  background-color: hsl(48, 100%, 29%);
}
.dot-link {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 0.7rem;
  background-color: #fff;
}
.dot-link-inv {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 0.7rem;
  background-color: #7957d5;
}
.noti-succ{
  
}
</style>