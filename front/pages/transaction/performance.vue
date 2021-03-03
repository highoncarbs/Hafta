<template>
  <div class="has-background-white" style="border-top: 1px solid #eee">
    <div
      class="section py-4 pt-5 is-fullwidth is-fullheight"
      :class="{ 'container px-0': $store.state.win }"
    >
      <b-sidebar
        mobile="fullwidth"
        type="is-white"
        :fullheight="true"
        :overlay="true"
        :right="true"
        :open.sync="showReports"
      >
        <div class="my-4 px-4">
          <div class="level is-mobile my-0" v-if="employee != null">
            <div class="level-left">
              <div class="level-item">
                <p class="has-text-weight-medium is-size-5">
                  Reports for {{ this.employee.name }}
                </p>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <p class="delete" @click="showReports = !showReports"></p>
              </div>
            </div>
          </div>

          <hr class="my-2" />

          <br />
          <b-table :data="quickReports" :empty="quickReports.length == 0">
            <template slot="empty">
              <div class="my-6 has-text-centered">
                <b-icon
                  icon="table-remove"
                  size="is-medium"
                  class="has-text-grey-light"
                ></b-icon>
                <p class="has-text-weight-medium has-text-grey">
                  No Reports Added
                </p>
              </div>
            </template>
            <b-table-column v-slot="props" label="Date">{{
              formatedDate(props.row.date)
            }}</b-table-column>
            <b-table-column v-slot="props" label="Feedback">
              <span
                class="tag heading has-text-weight-medium is-rounded"
                :class="{
                  'is-danger': props.row.feedback == 'negative',
                  'is-info': props.row.feedback == 'positive',
                }"
              >
                {{ props.row.feedback }}</span
              >
            </b-table-column>
            <b-table-column v-slot="props" label="Report">{{
              props.row.report
            }}</b-table-column>
          </b-table>
        </div>
      </b-sidebar>
      <!-- Heading Title -->
      <div class="level">
        <div class="level-left">
          <p class="is-size-4 has-text-weight-semibold">Performance</p>
        </div>
      </div>

      <!-- Advacne Company and Date selection -->
      <div class="field is-grouped is-grouped-multiline">
        <div class="control">
          <b-field
            label="Select Employee"
            label-position="on-border"
            :type="{ 'is-danger': errors.emp }"
          >
            <b-autocomplete
              icon="maginify"
              v-model="query_employee"
              placeholder="Search Employees"
              :keep-first="true"
              :open-on-focus="true"
              :data="autocompleteEmp"
              field="name"
              @select="(option) => (employee = option)"
              :clearable="true"
            >
              <template slot-scope="props">
                <p>{{ props.option.name }}</p>
                <p class="has-text-grey">
                  {{
                    titleCase(
                      props.option.company[0].name +
                        ", " +
                        props.option.company[0].location[0].name
                    )
                  }}
                </p>
              </template>
            </b-autocomplete>
          </b-field>
        </div>

        <div class="control">
          <b-field
            label-position="on-border"
            label="From"
            :type="{ 'is-danger': errors.fromdate }"
          >
            <b-datepicker
              v-model="fromdate"
              placeholder="From Date"
            ></b-datepicker>
          </b-field>
        </div>
        <div class="control">
          <b-field
            label-position="on-border"
            label="To"
            :type="{ 'is-danger': errors.todate }"
          >
            <b-datepicker v-model="todate" placeholder="To Date"></b-datepicker>
          </b-field>
        </div>

        <div class="control">
          <button class="button is-black" @click="getFactor()">
            <b-icon icon="check"></b-icon>
            <span class="ml-2"> Submit </span>
          </button>
        </div>
        <div class="control">
          <button class="button" @click="viewPastRecords">
            <b-icon icon="eye"></b-icon>
            <span class="ml-2"> View </span>
          </button>
        </div>
      </div>
      <small v-if="errors.submit" class="has-text-danger is-underline">
        Please set both company and dates.
      </small>

      <hr class="my-2" />

      <!-- Modal Attention for performance -->

      <div v-if="attModal" :class="{ 'is-active': attModal }" class="modal">
        <div
          class="modal-background animated fadeIn"
          @click="attModal = !attModal"
        ></div>
        <div class="modal-content animated fadeIn">
          <div class="box is-fullwidth">
            <p class="is-size-5">
              Performance Details for -
              <span class="has-text-weight-semibold">
                {{ performanceDetail.employee[0].name }}</span
              >
            </p>
            <small class="has-text-grey"
              >DATE:
              <span class="has-text-weight-semibold"
                >{{ formatedDate(performanceDetail.fromdate) }} -
                {{ formatedDate(performanceDetail.todate) }}</span
              >
            </small>
            <br />
            <br />
            <div class="table-container">
              <table class="table is-fullwidth is-bordered">
                <thead>
                  <tr>
                    <th>Factor</th>
                    <th>Weight</th>
                    <th>Max. Score</th>
                    <th>Obtained Score</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(row, index) in performanceDetail.performance_items"
                    :key="index"
                  >
                    <td>{{ row.performance.name }}</td>
                    <td>{{ row.performance.weight }}</td>
                    <td>{{ row.performance.score }}</td>
                    <td>{{ row.obt_score }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <button
            class="modal-close is-large"
            @click="attModal = !attModal"
          ></button>
        </div>
      </div>

      <!-- View past records -->
      <div
        class="table-container animated fadeIn"
        style="overflow: visible"
        v-if="viewPast"
      >
        <div class="field is-grouped">
          <div class="control is-expanded has-icons-left">
            <input
              type="text"
              class="input is-fullwidth"
              v-model="searchQuery"
              placeholder="Search"
            />

            <span class="icon icon-btn is-left">
              <b-icon icon="search"></b-icon>
            </span>
          </div>
        </div>

        <table class="table is-fullwidth is-bordered is-hoverable">
          <thead style="cursor: pointer">
            <!-- TABLE HEADER -->
            <tr class="has-text-weight-semibold">
              <th @click="sortBy('from')">
                From
                <span class="icon icon-btn icon-btn-in">
                  <b-icon
                    v-if="this.currentSort == 'from'"
                    :type="
                      this.currentSortDir == 'asc'
                        ? 'chevron-up'
                        : 'chevron-down'
                    "
                  ></b-icon>
                </span>
              </th>

              <th @click="sortBy('to')">
                To
                <span class="icon icon-btn icon-btn-in">
                  <b-icon
                    v-if="this.currentSort == 'to'"
                    :type="
                      this.currentSortDir == 'asc'
                        ? 'chevron-up'
                        : 'chevron-down'
                    "
                  ></b-icon>
                </span>
              </th>
              <th @click="sortBy('name')">
                Employee
                <span class="icon icon-btn icon-btn-in">
                  <b-icon
                    v-if="this.currentSort == 'name'"
                    :type="
                      this.currentSortDir == 'asc'
                        ? 'chevron-up'
                        : 'chevron-down'
                    "
                  ></b-icon>
                </span>
              </th>
              <th @click="sortBy('performance')">
                Performance
                <span class="icon icon-btn icon-btn-in">
                  <b-icon
                    v-if="this.currentSort == 'performance'"
                    :type="
                      this.currentSortDir == 'asc'
                        ? 'chevron-up'
                        : 'chevron-down'
                    "
                  ></b-icon>
                </span>
              </th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(row, index) in filteredRecordList">
              <!-- add to row @dblclick="performanceModal(row.employee[0].id)" -->
              <td>{{ formatedDate(row.fromdate) }}</td>
              <td>{{ formatedDate(row.todate) }}</td>
              <td>{{ row.employee[0].name }}</td>
              <td>{{ row.net_score }} %</td>
              <td>
                <div class="buttons">
                  <button class="button" @click="editPerformance(index)">
                    <b-icon icon="pencil"></b-icon>
                  </button>
                  <button
                    class="button is-danger"
                    @click="deletePerformance(row.id, index)"
                  >
                    <b-icon icon="delete"></b-icon>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Entry  Performance Records -->
      <div v-show="showPerfTable && employee">
        <div class="table-container animated fadeIn" style="overflow: visible">
          <div class="field">
            <div class="control">
              <button class="button" @click="showReports = !showReports">
                <b-icon icon="poll-box"></b-icon>
                <span class="ml-2"> View Reports </span>
              </button>
            </div>
          </div>
          <table class="table is-fullwidth is-bordered">
            <thead>
              <th>Factor</th>
              <th>Max. Score</th>
              <th>Weight</th>
              <th>Obtained Score</th>
            </thead>

            <tfoot>
              <tr>
                <td colspan="5">
                  <div class="buttons">
                    <button
                      class="button is-black"
                      @click="submitData"
                      :disabled="submitting"
                    >
                      <span class="icon icon-btn">
                        <b-icon icon="check"></b-icon>
                      </span>
                      Save
                    </button>
                    <span
                      v-if="Object.keys(errors).length != 0"
                      class="has-text-danger is-underline"
                      >Please fix the errors.</span
                    >
                  </div>
                </td>
              </tr>
            </tfoot>
            <tbody>
              <tr v-for="(row, index) in factorList" :key="index">
                <td>
                  {{ row.name }}
                </td>
                <td v-html="row.score"></td>
                <td v-html="row.weight"></td>
                <td>
                  <input
                    type="text"
                    class="input"
                    v-model="row.obt_score"
                    placeholder="Enter Obtained Score"
                    :class="{
                      'is-danger':
                        errors[row.id] != undefined &&
                        errors[row.id].obt_score == true,
                    }"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Edit Modal -->
      <b-modal v-model="editPerfModal">
        <div class="box is-fullwidth" v-if="editFactorList">
          <p class="is-size-5">
            Edit Performance Details for -
            <span class="has-text-weight-semibold">
              {{ editFactorList.employee[0].name }}</span
            >
          </p>
          <small class="has-text-grey"
            >DATE:
            <span class="has-text-weight-semibold"
              >{{ formatedDate(fromdate) }} - {{ formatedDate(todate) }}</span
            >
          </small>
          <br />
          <br />
          <div
            class="table-container animated fadeIn"
            style="overflow: visible"
          >
            <table class="table is-fullwidth is-bordered">
              <thead>
                <th>Factor</th>
                <th>Max. Score</th>
                <th>Weight</th>
                <th>Obtained Score</th>
              </thead>

              <tfoot>
                <tr>
                  <td colspan="5">
                    <div class="buttons">
                      <button
                        class="button is-black"
                        @click="updateData"
                        :disabled="submitting"
                      >
                        <b-icon icon="refresh"></b-icon>
                        <span class="ml-2"> Update </span>
                      </button>
                      <span
                        v-if="Object.keys(editerrors).length != 0"
                        class="has-text-danger is-underline"
                        >Please fix the errors.</span
                      >
                    </div>
                  </td>
                </tr>
              </tfoot>
              <tbody>
                <tr
                  v-for="(row, index) in editFactorList.performance_items"
                  animation="spin ? submitting : false"
                  :key="index"
                >
                  <td>
                    {{ row.performance.name }}
                  </td>
                  <td v-html="row.performance.score"></td>
                  <td v-html="row.performance.weight"></td>
                  <td>
                    <input
                      type="text"
                      class="input"
                      v-model="row.obt_score"
                      placeholder="Enter Obtained Score"
                      :class="{
                        'is-danger':
                          editerrors[row.id] != undefined &&
                          editerrors[row.id].obt_score == true,
                      }"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      company: null,
      errors: {},
      editerrors: {},
      employee: "",
      data_employee: [],
      quickReports: [],
      query_employee: "",
      emp_id: null,

      fromdate: null,
      todate: null,
      currentSort: "employee",
      currentSortDir: "asc",
      dataList: [],
      factorList: [],
      showEmpSelect: false,
      tempfactor: "",
      rows: [],
      showPerfTable: false,
      showReports: false,
      submitting: false,
      viewPast: false,
      viewPastButton: false,
      pastRecords: [],
      tempPastRecords: [],
      searchQuery: "",

      attModal: false,
      performanceDetail: null,
      editFactorList: null,
      editPerfTable: null,
      editPerfModal: false,
      quickPerfModal: false,
    };
  },
  computed: {
    filteredRecordList() {
      this.pastRecords = this.tempPastRecords.filter((data) => {
        return data.employee[0].name
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase());
      });

      if (this.currentSort == "name") {
        if (this.currentSortDir == "asc") {
          this.pastRecords.sort(function (a, b) {
            return ("" + a.name).localeCompare(b.name);
          });
        } else if (this.currentSortDir == "desc") {
          this.pastRecords
            .sort(function (a, b) {
              return ("" + a.name).localeCompare(b.name);
            })
            .reverse();
        }
      }

      if (this.currentSort == "from") {
        if (this.currentSortDir == "asc") {
          this.pastRecords.sort(function (a, b) {
            return ("" + a.fromdate).localeCompare(b.fromdate);
          });
        } else if (this.currentSortDir == "desc") {
          this.pastRecords
            .sort(function (a, b) {
              return ("" + a.fromdate).localeCompare(b.fromdate);
            })
            .reverse();
        }
      }
      if (this.currentSort == "to") {
        if (this.currentSortDir == "asc") {
          this.pastRecords.sort(function (a, b) {
            return ("" + a.todate).localeCompare(b.todate);
          });
        } else if (this.currentSortDir == "desc") {
          this.pastRecords
            .sort(function (a, b) {
              return ("" + a.todate).localeCompare(b.todate);
            })
            .reverse();
        }
      }

      if (this.currentSort == "performance") {
        if (this.currentSortDir == "asc") {
          this.pastRecords.sort(function (a, b) {
            return ("" + a.net_score).localeCompare(b.net_score);
          });
        } else if (this.currentSortDir == "desc") {
          this.pastRecords
            .sort(function (a, b) {
              return ("" + a.net_score).localeCompare(b.net_score);
            })
            .reverse();
        }
      }

      return this.pastRecords;
    },
    autocompleteEmp() {
      if (this.data_employee.length != 0) {
        if (this.query_employee == "" || !this.query_employee) {
          return this.data_employee;
        } else {
          return this.data_employee.filter((option) => {
            return (
              option.name
                .toString()
                .toLowerCase()
                .indexOf(this.query_employee.toLowerCase()) >= 0
            );
          });
        }
      }
    },
  },
  mounted() {
    this.$axios.get("/employee/get/all").then((response) => {
      this.data_employee = response.data.data;
    });
  },
  watch: {
    employee: function (val) {
      if (val == "") {
        this.showPerfTable = false;
      }
    },
  },

  methods: {
    getSelected(option) {
      this.emp_id = option.id;
    },
    formatedDate(val) {
      var date = new Date(val);
      return (
        date.getDate() + "/" + (date.getMonth() + 1) + "/" + date.getFullYear()
      );
    },

    sortBy(sortKey) {
      console.log(sortKey);
      if (sortKey === this.currentSort) {
        this.currentSortDir = this.currentSortDir === "asc" ? "desc" : "asc";
      }
      this.currentSort = sortKey;
    },
    getFactor() {
      let self = this;
      this.errors = {};
      if (this.employee && this.fromdate && this.todadte) {
        this.viewPast = false;
        this.showEmpSelect = true;
        this.showPerfTable = true;
        let reportdata = {
          emp_id: this.employee.id,
          fromdate: this.fromdate,
          todate: this.todate,
        };
        this.factorList = [];
        if (this.employee) {
          this.$axios
            .post("/transaction/quick/get", reportdata)
            .then(function (response) {
              self.quickReports = response.data;
            });
          this.$axios
            .get("/transaction/get/performance")
            .then(function (response) {
              self.showPerfTable = true;
              console.log(response.data);
              self.viewPastButton = true;
              self.factorList = response.data;
            });

          //    Need to pop emps whose data is already been filled
        } else {
          this.$set(
            this.errors,
            "submit",
            "Please select both company and dates."
          );
        }
      }
      if (!this.employee) {
        this.$set(this.errors, "emp", true);
      }
      if (!this.fromdate) {
        this.$set(this.errors, "fromdate", true);
      }
      if (!this.todate) {
        this.$set(this.errors, "todate", true);
      }
    },

    checkData() {
      this.errors = {};
      let raw = this;
      let rawError = this.errors;
      this.factorList.forEach(function (item) {
        if (item.obt_score == undefined) {
          raw.$set(rawError, item.id, {});
          raw.$set(rawError[item.id], "obt_score", true);
        }
      });

      if (Object.keys(this.errors).length == 0) {
        return true;
      } else {
        return false;
      }
    },
    checkEditData() {
      this.editerrors = {};
      let raw = this;
      let rawError = this.editerrors;
      this.editFactorList.performance_items.forEach(function (item) {
        if (item.obt_score == "" || item.obt_score == undefined) {
          raw.$set(rawError, item.id, {});
          raw.$set(rawError[item.id], "obt_score", true);
        }
      });

      if (Object.keys(this.editerrors).length == 0) {
        return true;
      } else {
        return false;
      }
    },
    submitData() {
      let self = this;
      if (this.checkData()) {
        this.submitting = true;
        let formdata = {
          emp_id: this.employee.id,
          fromdate: this.fromdate,
          todate: this.todate,
          data: this.factorList,
        };
        this.$axios
          .post("/transaction/performance/save", formdata)
          .then(function (response) {
            if (response.data.success) {
              // Run notificaiton
              // Open selection for reports and printing
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

              self.showPerfTable = false;
              self.employee = "";
            } else if (response.data.message) {
              // Run message
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
              console.log(response.data.message);
            }

            this.submitting = false;
          })
          .catch(function (error) {
            self.$buefy.snackbar.open({
              duration: 4000,
              message: "Couldn't send request. Server Error.",
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                this.isActive = false;
              },
            });
            console.error(error);
            this.submitting = false;
          })
          .finally(() => {
            this.submitting = false;
          });
      }
    },
    viewPastRecords() {
      this.errors = {};
      if (this.employee && this.fromdate && this.todate) {
        let formdata = {
          company: this.employee.company[0].id,
          fromdate: this.fromdate,
          todate: this.todate,
        };
        let self = this;
        this.viewPast = true;
        this.showEmpSelect = false;
        this.showPerfTable = false;

        this.$axios
          .post("/transaction/performance/company", formdata)
          .then(function (response) {
            self.pastRecords = JSON.parse(response.data);
            self.tempPastRecords = JSON.parse(response.data);
            self.$buefy.snackbar.open({
              duration: 4000,
              message: "Performance Loaded",
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                this.isActive = false;
              },
            });
          })
          .catch(function (error) {
            self.$buefy.snackbar.open({
              duration: 4000,
              message: "Couldn't send request. Server Error.",
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                this.isActive = false;
              },
            });
            console.error(error);
          });
      } else {
            if (!this.employee) {
        this.$set(this.errors, "emp", true);
      }
      if (!this.fromdate) {
        this.$set(this.errors, "fromdate", true);
      }
      if (!this.todate) {
        this.$set(this.errors, "todate", true);
      }
        this.$set(
          this.errors,
          "submit",
          "Please select both company and dates."
        );
      }
    },
    performanceModal(id) {
      this.attModal = !this.attModal;
      let self = this;
      this.$axios
        .get("/transaction/performance/get/employee/" + String(id))
        .then(function (response) {
          self.performanceDetail = JSON.parse(response.data);
        });
    },
    deletePerformance(id, index) {
      let self = this;
      this.$axios
        .post("/transaction/performance/delete/" + String(id))
        .then(function (response) {
          if (response.data.success) {
            self.tempPastRecords.splice(index, 1);
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
    editPerformance(id) {
      this.editFactorList = this.tempPastRecords[id];
      this.editPerfModal = !this.editPerfModal;
    },
    updateData() {
      this.submitting = true;
      let self = this;
      let formdata = this.editFactorList;
      if (this.checkEditData()) {
        this.$axios
          .post("/transaction/performance/update", formdata)
          .then(function (response) {
            if (response.data.success) {
              // Run notificaiton
              // Open selection for reports and printing
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
              self.editPerfModal = !self.editPerfModal;
              self.viewPastRecords();
            } else if (response.data.message) {
              // Run message
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
              console.log(response.data.message);
            }

            this.submitting = false;
          })
          .catch(function (error) {
            self.$buefy.snackbar.open({
              duration: 4000,
              message: "Couldn't send request. Server Error.",
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                this.isActive = false;
              },
            });
            console.error(error);
            this.submitting = false;
          });
      }
      this.submitting = false;
    },
  },
};
</script>

<style>
</style>