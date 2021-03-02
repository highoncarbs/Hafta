<template>
  <div>
    <div class="has-background-white" style="border-top: 1px solid #eee">
      <b-sidebar
        mobile="fullwidth"
        type="is-white"
        :fullheight="true"
        :overlay="true"
        :right="true"
        :open.sync="showCalc"
      >
        <div class="my-4 px-4">
          <div class="level">
            <div class="left-left">
              <div class="level-item">
                <p class="has-text-weight-medium is-size-5">Quick Calculator</p>
              </div>
            </div>
            <div class="left-right">
              <div class="level-item">
                <p @click="showCalc = !showCalc" class="delete"></p>
              </div>
            </div>
          </div>
          <hr class="my-2" />
          <br />
          <b-field label="Period">
            <b-radio v-model="calc.period" native-value="hour">Hour</b-radio>
            <b-radio v-model="calc.period" native-value="day">Day</b-radio>
            <b-radio v-model="calc.period" native-value="month">Month</b-radio>
          </b-field>
          <b-field grouped>
            <div class="control">
              <b-field label="Unit Pay" style="width: 10rem">
                <b-input type="number" v-model.number="calc.pay"></b-input>
              </b-field>
            </div>
            <div class="control">
              <b-field label="Time" style="width: 10rem">
                <b-input type="number" v-model.number="calc.time"></b-input>
              </b-field>
            </div>
          </b-field>
          <hr class="my-3" />
          <div class="notification has-background-info-light py-3 px-3">
            <div class="level my-0">
              <div class="level-left">
                <div class="level-item">
                  <b-field label="Amount">
                    {{ formatedNumber(getOverTime) }}
                  </b-field>
                </div>
              </div>
              <div class="level-right">
                <div class="level-item">
                  <button @click="copyAmt" class="button is-link">
                    <b-icon icon="content-copy"></b-icon>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </b-sidebar>
      <div
        class="section py-4 pt-5 is-fullwidth is-fullheight"
        :class="{ 'container px-0': $store.state.win }"
      >
        <!-- <transition name="fade"> -->
        <div v-if="showView">
          <p class="is-size-5 has-text-weight-bold">Salary Sheet</p>
          <br />
          <div class="columns">
            <div
              class="column is-3"
              v-for="(item, index) in data_company"
              :key="index"
            >
              <div class="box">
                <p
                  class="tag heading is-rounded is-warning mb-4"
                  v-if="item.status == 'pending'"
                >
                  <span class="dot-warning"></span>
                  SALARY PENDING -
                  {{ new Date().toLocaleString("default", { month: "long" }) }}
                </p>
                <p
                  class="tag heading is-rounded is-info mb-4"
                  v-if="item.status == 'done'"
                >
                  <span class="dot-link"></span>
                  SALARY PROCESSED -
                  {{ new Date().toLocaleString("default", { month: "short" }) }}
                </p>
                <p class="is-size-4 has-text-weight-bold">
                  {{ titleCase(item.name) }}
                </p>
                <hr class="my-2" />
                <p class="is-size-5 mt-2">{{ item.num }} Employees</p>
                <p class="is-size-5 is-family-monospace">
                  INR {{ item.payout.toLocaleString("en-IN") }}
                </p>
                <br />
                <b-field label="Select Month">
                  <b-datepicker
                    trap-focus
                    type="month"
                    icon="calendar"
                    v-model="month"
                    placeholder="Select Month"
                  ></b-datepicker>
                </b-field>
                <button
                  @click="generateSalarySheet(item)"
                  class="button is-fullwidth is-link"
                >
                  Generate Salary Sheet
                </button>
              </div>
            </div>
          </div>
        </div>
        <!-- </transition> -->
        <div v-if="!showView">
          <div class="level my-0">
            <div class="level-left">
              <div class="level-item">
                <button class="button mb-4" @click="showView = !showView">
                  <b-icon icon="chevron-left"></b-icon>
                  <span>Back to Firms</span>
                </button>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <button class="button mb-4" @click="showCalc = !showCalc">
                  <b-icon icon="calculator"></b-icon>
                  <span>Quick Calc.</span>
                </button>
              </div>
            </div>
          </div>
          <br />
          <p
            class="tag heading is-rounded is-warning mb-4"
            v-if="company.status == 'pending' && currSheetStatus != 'done'"
          >
            <span class="dot-warning"></span>
            Salary pending -
            {{ new Date().toLocaleString("default", { month: "short" }) }}
          </p>
          <p
            class="tag heading is-rounded is-info mb-4"
            v-if="company.status == 'done'"
          >
            <span class="dot-link"></span>
            Salary Proccessed -
            {{ new Date().toLocaleString("default", { month: "short" }) }}
          </p>

          <div
            class="notification is-link has-text-white"
            v-if="currSheetStatus == 'done'"
          >
            <p
              class="tag heading is-rounded is-white mb-4"
              v-if="currSheetStatus == 'done'"
            >
              <span class="dot-link-inv"></span>
              Salary Proccessed -
              {{
                new Date(this.month).toLocaleString("default", {
                  month: "short",
                })
              }}
            </p>
            <p class="has-text-weight-medium">
              Salary Sheet has been processed for this month.
            </p>
            <p>No further changes will be saved. You can <b>Print</b>  this sheet or <b>select empolyees</b>  for whom you want the slips.</p>
          </div>

          <div class="level is-mobile">
            <div class="level-left">
              <div class="level-item">
                <div>
                  <p class="heading">COMPANY</p>
                  <p class="is-size-5 has-text-weight-semibold">Jai Texart</p>
                </div>
              </div>
              <div class="level-item ml-2">
                <div>
                  <p class="heading">PAYROLL FOR</p>
                  <p class="is-size-5 has-text-weight-semibold">
                    {{
                      new Date(this.month).toLocaleString("default", {
                        month: "long",
                      }) +
                      ", " +
                      new Date(this.month).getFullYear()
                    }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div id="salary_sheet_form">
            <!-- Advacne Company and Date selection -->
            <div
              class="box has-background-info-light has-text-info-dark fadeIn"
              v-if="isGenerating"
            >
              <p class="has-text-weight-semibold">Generating Salary Sheet</p>
            </div>

            <div v-if="salarySheet != null && salarySheet.length == 0">
              <div
                class="box has-text-centered has-text-weight-bold has-text-grey fadeIn"
              >
                <b-icon icon="information"></b-icon>
                <p>
                  Attendence has not been added for this month. <br />
                  Please add them before processing salary sheet for the month.
                </p>
              </div>
            </div>
           

            <div v-if="salarySheet != null && salarySheet.length != 0">
              <div class="buttons">
                <button class="button" @click="printAll">
                  <b-icon icon="printer"></b-icon>
                  <span class="ml-2"> Print </span>
                </button>
                <button
                  @click="printSelected"
                  class="button is-link"
                  :disabled="selectedRow == null || selectedRow.length == 0"
                >
                  <b-icon icon="printer-check "></b-icon>
                  <span class="ml-2"> Print Selected </span>
                </button>
              </div>
              <!-- Sheet Entry -->
              <b-table
                checkable
                :checked-rows.sync="selectedRow"
                :data="salarySheetEdit"
                :striped="true"
              >
                <b-table-column v-slot="props" field="name" label="Name">{{
                  props.row.employee[0].name
                }}</b-table-column>
                <b-table-column v-slot="props" field="" label="Dept.">
                  <span v-if="props.row.employee[0].department.length != 0">
                    {{ props.row.employee[0].department[0].name }}</span
                  >
                  <span v-else class="has-text-grey"> None</span>
                </b-table-column>
                <b-table-column v-slot="props" field="" label="Post">
                  <span v-if="props.row.employee[0].post.length != 0">
                    {{ props.row.employee[0].post[0].name }}</span
                  >
                  <span v-else class="has-text-grey"> None</span>
                </b-table-column>
                <b-table-column v-slot="props" label="Days Attn.">
                  <span class="has-text-weight-semibold">
                    {{ props.row.daysatt }}
                  </span>
                </b-table-column>
                <b-table-column v-slot="props" label="Late Comin">{{
                  props.row.latecomin
                }}</b-table-column>
                <b-table-column v-slot="props" label="Early Going">{{
                  props.row.earlygoing
                }}</b-table-column>
                <b-table-column v-slot="props" label="Basic Pay">{{
                  formatedNumber(props.row.employee[0].basicpay)
                }}</b-table-column>
                <b-table-column v-slot="props" label="Days Payable">{{
                  formatedNumber(props.row.days_payable)
                }}</b-table-column>
                <b-table-column v-slot="props" label="Pay #1">{{
                  formatedNumber(props.row.pay_1)
                }}</b-table-column>
                <b-table-column v-slot="props" label="Adv. Ded.">
                  <small class="has-text-grey">MONTHLY</small>
                  <span v-if="typeof props.row.deductions.month == 'object'">
                    <ul
                      :key="index"
                      v-for="(dec, index) in props.row.deductions.month"
                    >
                      <li>{{ dec }}</li>
                    </ul>
                  </span>
                  <span v-else>
                    <ul>
                      <li>{{ props.row.deductions.month }}</li>
                    </ul>
                  </span>
                  <hr class="my-2" />
                  <b-field>
                    <b-input
                      v-model="props.row.net_adv_deduction"
                      :value="props.row.net_adv_deduction"
                      placeholder="Deduct"
                    ></b-input>
                  </b-field>
                </b-table-column>
                <b-table-column v-slot="props" label="ESI">{{
                  formatedNumber(props.row.esi)
                }}</b-table-column>
                <b-table-column v-slot="props" label="PF">{{
                  formatedNumber(props.row.pf)
                }}</b-table-column>
                <b-table-column v-slot="props" label="TDS">{{
                  formatedNumber(props.row.tds)
                }}</b-table-column>
                <b-table-column v-slot="props" label="Overtime">
                  <b-field>
                    <b-numberinput
                      :controls="false"
                      v-model.number="props.row.overtime"
                      controls-rounded
                    ></b-numberinput>

                    <!-- <b-input type="number" v-model.number="props.row.overtime"></b-input> -->
                  </b-field>
                </b-table-column>
                <b-table-column v-slot="props" label="Other Ded.">{{
                  formatedNumber(props.row.other_deduction)
                }}</b-table-column>
                <b-table-column v-slot="props" label="Total Ded. #2">{{
                  formatedNumber(props.row.total_deductions)
                }}</b-table-column>
                <b-table-column v-slot="props" label="Net (#1 - #2)">{{
                  formatedNumber(props.row.net_payable)
                }}</b-table-column>
              </b-table>
            </div>
          </div>
          <br />

          <button class="button is-black" @click="processSalary">
            <b-icon icon="check-circle"></b-icon>

            <span class="ml-2"> Process Salary </span>
          </button>
          <br />
          <p class="is-underline mt-3">
            Processing debits advances of employees.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      calc: {
        period: null,
        pay: null,
        time: null,
        final: null,
      },
      showCalc: false,
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
            this.$set(item, "status", response.data.status);
          });
      });
    });
  },
  computed: {
    getOverTime() {
      if (this.calc.period && this.calc.time && this.calc.pay) {
        return this.calc.time * this.calc.pay;
      } else return 0;
    },
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
            let overtime = parseFloat(row.overtime)||0
          row.net_payable = Math.round(
            parseFloat(tempPay) - parseFloat(row.total_deductions) + overtime 
          );

        });
      }

      return this.salarySheet;
    },
  },
  methods: {
    async copyAmt() {
      try {
        await navigator.clipboard.writeText(this.getOverTime);
      } catch (err) {}
    },

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
            date: this.month,
          })
          .then((response) => {
            this.currSheetStatus = response.data.status;
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
      window.open("/print/salary-sheet-all", "_blank", [], true);
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
      window.open("/transaction/salary_sheet/print/all", "_blank", [], true);
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
      window.open("/print/salary-sheet-selected", "_blank", [], true);
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
.noti-succ {
}
</style>