<template>
  <div>
    <div class="has-background-white" style="border-top: 1px solid #eee">
      <div
        class="section py-4 pt-5 is-fullwidth is-fullheight"
        :class="{ 'container px-0': $store.state.win }"
      >
        <section class="section">
          <div v-if="empDetail">
            <table class="table is-fullwidth is-bordered">
              <thead>
                <tr>
                  <th colspan="2">
                    <small class="has-text-grey has-text-weight-semibold"
                      >NAME</small
                    >
                    <p
                      class="is-size-5 is-size-6-mobile has-text-weight-normal-mobile is-capitalized"
                    >
                      {{ empDetail.name }}
                    </p>
                  </th>
                  <th colspan="2">
                    <small class="has-text-grey has-text-weight-semibold"
                      >COMPANY</small
                    >
                    <p
                      class="is-size-5 is-size-6-mobile has-text-weight-normal-mobile"
                      v-if="!empDetail.company.length"
                    >
                      None
                    </p>
                    <p
                      class="is-size-5 is-size-6-mobile has-text-weight-normal-mobile"
                      v-if="empDetail.company.length"
                    >
                      {{ titleCase(empDetail.company[0].name) }} ,
                      {{ titleCase(empDetail.company[0].location[0].name) }}
                    </p>
                  </th>
                  <th colspan="2">
                    <small class="has-text-grey has-text-weight-semibold"
                      >BASIC PAY</small
                    >
                    <p
                      class="is-size-5 is-size-6-mobile has-text-weight-normal-mobile"
                    >
                      {{ formatedNumber(empDetail.basicpay) }}
                    </p>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td colspan="1">
                    <small class="has-text-weight-semibold has-text-grey">
                      APPOINTMENT</small
                    >

                    <p
                      class="has-text-black has-text-weight-semibold"
                      v-html="
                        empDetail.appointment.length
                          ? empDetail.appointment[0].name
                          : 'None'
                      "
                    ></p>
                  </td>
                  <td colspan="1">
                    <small class="has-text-weight-semibold has-text-grey"
                      >POST</small
                    >
                    <p
                      class="has-text-black has-text-weight-semibold"
                      v-html="
                        empDetail.post.length ? empDetail.post[0].name : 'None'
                      "
                    ></p>
                  </td>

                  <td colspan="1">
                    <small class="has-text-weight-semibold has-text-grey">
                      DEPARTMENT</small
                    >

                    <p
                      class="has-text-black has-text-weight-semibold"
                      v-html="
                        empDetail.department.length
                          ? empDetail.department[0].name
                          : 'None'
                      "
                    ></p>
                  </td>
                  <td colspan="1">
                    <small class="has-text-weight-semibold has-text-grey">
                      ADVANCE AMOUNT</small
                    >

                    <p
                      class="has-text-black has-text-weight-semibold"
                      v-html="
                        empDetail.advancevalue
                          ? formatedNumber(empDetail.advancevalue)
                          : 'None'
                      "
                    ></p>
                  </td>
                  <td colspan="1">
                    <small class="has-text-weight-semibold has-text-grey">
                      NUMBER of ADVANCES</small
                    >

                    <p
                      class="has-text-black has-text-weight-semibold"
                      v-html="
                        empDetail.advancenum ? empDetail.advancenum : 'None'
                      "
                    ></p>
                  </td>
                </tr>
                <tr class="has-background-light">
                  <td>
                    <small class="has-text-weight-semibold has-text-grey">
                      PHOTO</small
                    >
                    <br />
                    <button
                      class="button"
                      @click="
                        isPdf.pan
                          ? viewPDF('photofile')
                          : showUpload('photofile')
                      "
                      :disabled="empDetail.photofile == null"
                    >
                      <span class="icon icon-btn">
                        <b-icon icon="eye"></b-icon>
                      </span>
                      View
                    </button>
                  </td>
                  <td>
                    <small class="has-text-weight-semibold has-text-grey">
                      PAN</small
                    >
                    <br />
                    <button
                      class="button"
                      @click="
                        isPdf.pan ? viewPDF('panfile') : showUpload('panfile')
                      "
                      :disabled="empDetail.panfile == null"
                    >
                      <span class="icon icon-btn">
                        <b-icon icon="eye"></b-icon>
                      </span>
                      View
                    </button>
                  </td>
                  <td>
                    <small class="has-text-weight-semibold has-text-grey">
                      AADHAR</small
                    >
                    <br />
                    <button
                      class="button"
                      @click="
                        isPdf.pan
                          ? viewPDF('panfile')
                          : showUpload('aadharfile')
                      "
                      :disabled="empDetail.aadharfile == null"
                    >
                      <span class="icon icon-btn">
                        <b-icon icon="eye"></b-icon>
                      </span>
                      View
                    </button>
                  </td>
                  <td>
                    <small class="has-text-weight-semibold has-text-grey">
                      EXTRA ID</small
                    >
                    <br />
                    <button
                      class="button"
                      @click="
                        isPdf.pan
                          ? viewPDF('panfile')
                          : showUpload('extraidfile')
                      "
                      :disabled="empDetail.extraidfile == null"
                    >
                      <span class="icon icon-btn">
                        <b-icon icon="eye"></b-icon>
                      </span>
                      View
                    </button>
                  </td>
                  <td>
                    <small class="has-text-weight-semibold has-text-grey">
                      EDUCATION CERT.</small
                    >
                    <br />
                    <button
                      class="button"
                      @click="
                        isPdf.pan
                          ? viewPDF('panfile')
                          : showUpload('educertfile')
                      "
                      :disabled="empDetail.educertfile == null"
                    >
                      <span class="icon icon-btn">
                        <b-icon icon="eye"></b-icon>
                      </span>
                      View
                    </button>
                  </td>
                  <td>
                    <small class="has-text-weight-semibold has-text-grey">
                      RESUME</small
                    >
                    <br />
                    <button
                      class="button"
                      @click="
                        isPdf.pan
                          ? viewPDF('panfile')
                          : showUpload('resumefile')
                      "
                      :disabled="empDetail.resumefile == null"
                    >
                      <span class="icon icon-btn">
                        <b-icon icon="eye"></b-icon>
                      </span>
                      View
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Image Viewer -->
            <b-modal v-model="viewUpload">

                <figure class="image">
                  <img :src="fileSrc" alt="" />
                </figure>
            </b-modal>
         
            <!-- End Image Modal -->
            <div class="columns">
              <div class="column">
                <div class="box">
                  <p class="is-size-5 has-text-weight-semibold">Attendence</p>
                  <p>
                    View
                    <span class="has-text-weight-semibold">
                      {{ empDetail.name }}'s</span
                    >
                    attendence below.
                    <br />
                    Hover on color block for more info.
                  </p>
                  <br />

                  <div class="columns">
                    <div class="column">
                      <small class="has-text-grey has-text-weight-semibold"
                        >LATE COMIN</small
                      >

                      <Heatmap :datalist="attDetail.late_att"></Heatmap>
                      <br />
                      <small class="has-text-grey has-text-weight-semibold"
                        >EARLY GOING</small
                      >

                      <Heatmap :datalist="attDetail.early_att"></Heatmap>
                      <br />
                      <small class="has-text-grey has-text-weight-semibold"
                        >DAYS ATTENDED</small
                      >

                      <Heatmap :datalist="attDetail.day_att"></Heatmap>
                    </div>
                    <div class="column">
                      <small
                        class="has-text-grey has-text-weight-semibold is-uppercase"
                        >Total Late Comins</small
                      >
                      <p
                        class="has-text-black is-size-5 has-text-weight-semibold"
                      >
                        {{ total.late }} Days
                      </p>
                      <br />
                      <small
                        class="has-text-grey has-text-weight-semibold is-uppercase"
                        >Total Early Going</small
                      >
                      <p
                        class="has-text-black is-size-5 has-text-weight-semibold"
                      >
                        {{ total.early }} Days
                      </p>
                      <br />
                      <small
                        class="has-text-grey has-text-weight-semibold is-uppercase"
                        >Total Days Attended</small
                      >
                      <p
                        class="has-text-black is-size-5 has-text-weight-semibold"
                      >
                        {{ total.days }} Days
                      </p>
                    </div>
                  </div>
                </div>
                <div class="box">
                  <p class="is-size-5 has-text-weight-semibold">Salary Slips</p>
                  <br />
                  <b-field grouped group-multiline>
                    <b-field expanded label-position="on-border" label="Month">
                      <b-datepicker
                        expanded
                        type="month"
                        v-model="date"
                        placeholder="Select Month"
                      ></b-datepicker>
                    </b-field>
                    <!-- <div class="control">
                    </div> -->
                    <div class="control">
                      <button class="button is-black" @click="getSlip">
                        Submit
                      </button>

                      <button
                        @click="printSelected"
                        v-if="slip != null && !slipNone"
                        class="button"
                      >
                        <b-icon icon="printer"></b-icon>
                        <span class="ml-2"> Print </span>
                      </button>
                    </div>
                  </b-field>

                  <br />

                  <div
                    class="notification has-text-centered animated fadeIn"
                    v-if="slip == null && slipNone"
                  >
                    <span class="icon">
                      <b-icon icon="info"></b-icon>
                    </span>
                    <p>
                      Either Attendence or Salary Sheet hasn't been processed
                      for this month.
                    </p>
                  </div>
                  <table
                    class="table is-bordered is-fullwidth"
                    v-if="slip != null && !slipNone"
                  >
                    <tbody>
                      <tr>
                        <td colspan="1">
                          <small class="has-text-weight-semibold">
                            DAYS ATTENDED</small
                          >

                          <p>{{ slip.daysatt }}</p>
                        </td>
                        <td colspan="1">
                          <small class="has-text-weight-semibold"
                            >LATE COMING</small
                          >
                          <p>{{ slip.latecomin }}</p>
                        </td>

                        <td colspan="1">
                          <small class="has-text-weight-semibold"
                            >BASIC PAY</small
                          >

                          <p>{{ formatedNumber(slip.employee[0].basicpay) }}</p>
                        </td>
                        <td colspan="1">
                          <small class="has-text-weight-semibold">
                            DAYS PAYABLE</small
                          >

                          <p>{{ slip.days_payable }}</p>
                        </td>
                        <td colspan="1">
                          <small class="has-text-weight-semibold">
                            ADVANCE DEDUCTION</small
                          >
                          <p>{{ formatedNumber(slip.net_adv_deduction) }}</p>
                        </td>
                      </tr>
                      <tr>
                        <td colspan="1">
                          <small class="has-text-weight-semibold">P.F</small>
                          <p>{{ slip.esi }}</p>
                        </td>

                        <td colspan="1">
                          <small class="has-text-weight-semibold"> ESI</small>

                          <p>{{ slip.pf }}</p>
                        </td>
                        <td colspan="1">
                          <small class="has-text-weight-semibold"> TDS</small>

                          <p>{{ slip.tds }}</p>
                        </td>
                        <td colspan="1">
                          <small class="has-text-weight-semibold">
                            Other Deduction</small
                          >

                          <p>{{ slip.other_deduction }}</p>
                        </td>
                        <td colspan="1">
                          <small class="has-text-weight-semibold"
                            >TOTAL DEDUCTION</small
                          >

                          <p>{{ formatedNumber(slip.total_deductions) }}</p>
                        </td>
                      </tr>
                      <tr>
                        <td colspan="4">
                          <small class="has-text-weight-semibold"
                            >OVERTIME</small
                          >
                        </td>
                        <td colspan="1">
                          <p>{{ formatedNumber(slip.overtime) }}</p>
                        </td>
                      </tr>
                      <tr>
                        <td colspan="4">
                          <small class="has-text-weight-semibold"
                            >NET PAYABLE</small
                          >
                        </td>
                        <td colspan="1">
                          <p>{{ formatedNumber(slip.net_payable) }}</p>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <div class="box">
                  <p class="is-size-5 has-text-weight-semibold">
                    Quick Reports
                  </p>
                  <br />
                  <b-table
                    :data="quickReports"
                    :empty="quickReports.length == 0"
                  >
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
              </div>
              <div class="column">
                <div class="box">
                  <p class="is-size-5 has-text-weight-semibold">Performance</p>
                  <br />
                  <div
                    v-if="perfDetail.length == 0"
                    class="notification has-text-centered"
                  >
                    <span class="icon">
                      <b-icon
                        icon="information"
                        class="has-text-grey-light"
                        size="is-medium"
                      ></b-icon>
                    </span>
                    <br />
                    <br />
                    <p>
                      Performances has not been added for
                      <span class="has-text-weight-semibold">
                        {{ empDetail.name }}</span
                      >
                      .
                    </p>
                  </div>
                  <div
                    v-if="perfDetail.length != 0"
                    v-for="(row, index) in perfDetail"
                    :key="index"
                  >
                    <p
                      class="has-text-semibold has-text-black has-text-weight-medium"
                    >
                      <span class="mr-2 has-text-grey"
                        >DATE
                      </span>
                      {{ formatedDate(row.fromdate) }} -
                      {{ formatedDate(row.todate) }}
                    </p>
                    <Columnchart :datalist="[row]"></Columnchart>
                    <hr class="my-3">
                  </div>
                </div>
                <div class="box">
                  <p class="is-size-5 has-text-weight-semibold">Advances</p>
                  <div class="my-4 px-4">
                    <p
                      v-if="advance_list != null"
                      class="has-text-weight-medium is-size-5"
                    >
                      Advance Ledger for {{ this.empDetail.name }}
                    </p>
                    <hr class="my-2" />
                    <p>
                      <span class="has-text-weight-semibold has-text-grey"
                        >Balance</span
                      >
                      <span class="is-pulled-right">
                        {{ formatedNumber(getTotalCredit() - getTotalDebit()) }}
                      </span>
                    </p>
                    <br />
                    <b-table
                      :data="advance_list"
                      :empty="advance_list.length == 0"
                    >
                      <template #empty>
                        <div class="has-text-centered">
                          <br />
                          <b-icon
                            icon="table-remove"
                            class="has-text-grey-lighter"
                            size="is-large"
                          ></b-icon>
                          <p class="mt-4 has-text-weight-medium has-text-grey">
                            No Advances taken yet
                          </p>
                        </div>
                      </template>
                      <b-table-column label="Date" v-slot="props">{{
                        formatDate(new Date(props.row.date))
                      }}</b-table-column>
                      <!-- <b-table-column label="Amt." v-slot="props">{{
            formatedNumber(props.row.advanceamt)
          }}</b-table-column> -->
                      <b-table-column centered label="Debit" v-slot="props">
                        <span
                          v-if="props.row.trans == 'debit'"
                          class="is-pulled-right"
                        >
                          {{ formatedNumberNoCurr(props.row.advanceamt) }}
                        </span>
                      </b-table-column>
                      <b-table-column centered label="Credit" v-slot="props">
                        <span
                          v-if="props.row.trans == 'credit'"
                          class="is-pulled-right"
                        >
                          {{ formatedNumberNoCurr(props.row.advanceamt) }}
                        </span>
                      </b-table-column>
                      <!-- <b-table-column label="Ded." v-slot="props"
            >{{ formatedNumber(props.row.deduction) }} /
            <span class="has-text-grey has-text-weight-medium">{{
              props.row.deduction_period
            }}</span></b-table-column> -->

                      <template #footer>
                        <td></td>
                        <td class="has-text-right">
                          {{ formatedNumberNoCurr(getTotalDebit()) }}
                        </td>
                        <td class="has-text-right">
                          {{ formatedNumberNoCurr(getTotalCredit()) }}
                        </td>
                      </template>
                    </b-table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- <b-modal v-model="showEmp">
      <div class="box">
        <p class="is-size-5 has-text-weight-bold">New Advance</p>
      </div>
    </b-modal> -->
  </div>
</template>

<script>
import Columnchart from "~/components/columnchart";
import Heatmap from "~/components/Heatmap";
export default {
  components: [Heatmap, Columnchart],
  data() {
    return {
      empDetail: null,
      emp_id: null,
      advance_list: [],

      perfDetail: [],
      attDetail: [],
      viewUpload: false,
      total: {
        days: 0,
        late: 0,
        early: 0,
      },
      viewFile: null,
      fileSrc: null,
      isPdf: {
        pan: false,
        aadhar: false,
        extraid: false,
        educert: false,
        resume: false,
      },
      date: null,
      slip: null,
      slipNone: false,
      quickReports: [],
    };
  },
  mounted() {
    this.emp_id = this.$route.params.id;
    let raw = this;
    this.$axios
      .get("/transaction/advance/get/" + this.emp_id)
      .then((response) => {
        this.advance_list = response.data;
      });
    if (this.emp_id != null) {
      this.$axios
        .post("/employee/get/detail/" + String(this.emp_id))
        .then(function (response) {
          raw.empDetail = response.data;
          if (raw.empDetail.panfile) {
            // console.log(raw.empDetail.panfile.split('.')[raw.empDetail.panfile.length -1])
            temp = raw.empDetail.panfile.split(".");
            if (temp[temp.length - 1] == "pdf") raw.isPdf.pan = true;
          }
          if (raw.empDetail.aadharfile) {
            // console.log(raw.empDetail.panfile.split('.')[raw.empDetail.panfile.length -1])
            temp = raw.empDetail.aadharfile.split(".");
            if (temp[temp.length - 1] == "pdf") raw.isPdf.aadhar = true;
          }
          if (raw.empDetail.educertfile) {
            // console.log(raw.empDetail.panfile.split('.')[raw.empDetail.panfile.length -1])
            temp = raw.empDetail.educertfile.split(".");
            if (temp[temp.length - 1] == "pdf") raw.isPdf.educert = true;
          }
          if (raw.empDetail.extraidfile) {
            // console.log(raw.empDetail.panfile.split('.')[raw.empDetail.panfile.length -1])
            temp = raw.empDetail.extraidfile.split(".");
            if (temp[temp.length - 1] == "pdf") raw.isPdf.extraid = true;
          }
          if (raw.empDetail.resumefile) {
            // console.log(raw.empDetail.panfile.split('.')[raw.empDetail.panfile.length -1])
            temp = raw.empDetail.resumefile.split(".");
            if (temp[temp.length - 1] == "pdf") raw.isPdf.resume = true;
          }
        });

      this.$axios
        .get("/transaction/performance/get/employee/" + String(this.emp_id))
        .then(function (response) {
          raw.perfDetail = response.data;
        });
      this.$axios
        .get("/transaction/attendence/employee/" + String(this.emp_id))
        .then(function (response) {
          raw.attDetail = JSON.parse(response.data);
        });

      if (this.emp_id != null) {
        let today = new Date();
        let fromdate = today.getFullYear() + "-01-01";
        let todate = today.getFullYear() + "-12-31";
        let self = this;
        let reportdata = {
          emp_id: this.emp_id,
          fromdate: fromdate,
          todate: todate,
        };
        this.$axios
          .post("/transaction/quick/get", reportdata)
          .then(function (response) {
            self.quickReports = response.data;
          });
      }
    }
  },
  watch: {
    attDetail: function (val) {
      this.total.days = val.day_att.reduce(function (total, num) {
        return total + num;
      }, 0);
      this.total.late = val.late_att.reduce(function (total, num) {
        return total + num;
      }, 0);
      this.total.early = val.early_att.reduce(function (total, num) {
        return total + num;
      }, 0);
    },
  },
  methods: {
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
    formatedNumber(val) {
      let test = Number(val).toLocaleString("en-IN", {
        style: "currency",
        currency: "INR",
      });
      return test;
    },
    formatedDate(val) {
      var date = new Date(val);
      return (
        date.getDate() + "/" + (date.getMonth() + 1) + "/" + date.getFullYear()
      );
    },
    showUpload(filetype) {
      this.viewFile = filetype;
      if (this.viewFile != null) {
        this.fileSrc = this.getStaticImg(this.empDetail[this.viewFile])
        this.viewUpload = !this.viewUpload;
      }
    },
    viewPDF(filetype) {
      this.viewFile = filetype;
      if (this.viewFile != null) {
        this.fileSrc = this.getStaticImg(this.empDetail[this.viewFile])

        window.open(this.fileSrc, "_blank");
      }
    },
    getSlip() {
      let raw = this;
      let formdata = { emp_id: this.emp_id, date: this.date };
      this.$axios
        .post("/transaction/salary_sheet/slips", formdata)
        .then(function (response) {
          let payload = response.data;
          if (payload.success) {
            raw.slipNone = false;
            raw.slip = payload.success;
          }

          if (payload.message) {
            raw.slip = null;
            raw.slipNone = true;
          }
        });
    },
    printSelected() {
      let self = this;
      localStorage.clear();
      let selectedData = [];
      selectedData.push(this.slip);
      let formdata = {
        company: this.empDetail.company,
        date: this.date,
        data: selectedData,
      };
      localStorage.setItem("selecteddata", JSON.stringify(formdata));
      this.$axios
        .post("/transaction/salary_sheet/print/selected", formdata)
        .then(function (response) {
          const win = window.open(
            "/transaction/salary_sheet/print/selected",
            "_blank",
            [],
            true
          );
        });
    },
  },
};
</script>

<style>
</style>