<template>
<div class="has-background-white" style="border-top: 1px solid #eee">
      <div
        class="section py-4 pt-5 is-fullwidth is-fullheight"
        :class="{ 'container px-0': $store.state.win }"
      >
        <div class="level">
            <div class="level-left">
                <p class="is-size-4 has-text-weight-semibold">Dashboard</p>
            </div>

        </div>

        <div class="columns">
            <div class="column">
                <div class="box">
                    <p class="has-text-weight-semibold is-size-5">
                        <span class="icon icon-btn">
                            <b-icon icon="bell" ></b-icon>
                        </span>
                        Updates</p>
                    <br>
                    <br>
                    <p>List salary increments , payroll to prcocess updates</p>
                </div>
            </div>
            <div class="column">
                <div class="box">

                    <p class="has-text-weight-semibold is-size-5">
                        <span class="icon icon-btn">
                            <b-icon icon="star" ></b-icon>
                        </span>Top Performer</p>
                    <br>
                    <br>
                </div>

            </div>
        </div>

        <div class="columns">
            <div class="column">
                <div class="box">
                    <p class="has-text-weight-semibold is-size-5">
                        <span class="icon icon-btn">
                            <b-icon icon="coffee" ></b-icon>
                        </span>Late Comers </p>
                    <br>
                    <p v-if="latecomers == null" class="has-text-centered has-text-grey-light">
                        <span class="icon icon-btn">
                            <b-icon icon="rotate-cw" animation="spin"></b-icon>
                        </span> Loading
                    </p>
                    <table class="table is-fullwidth is-hoverable">
                        <tbody>
                            <tr v-for="row in latecomers">
                                <td>
                                    <span class="is-capitalized is-size-5">{{ row[1].name}}</span>
                                    <br>
                                    <p class="has-text-weight-medium has-text-grey"
                                        v-html="titleCase(parsejson(row[1].company))"></p>
                                </td>
                                <td> <span class="has-text-weight-semibold">
                                        {{ row[1].late_att}}</span> Late Comins
                                    <br>
                                    <span>
                                    {{ row[1].day_att}}</span> Days Attended
                                </td>
                                <td>
                                    <button @click="viewReport(row[0])" class="button is-link is-outlined">
                                            <b-icon icon="file-chart"></b-icon>
<span class="ml-2">

                                        Reports
</span>
                                    </button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>
            <div class="column ">
                <div class="box">
                    <p class="has-text-weight-semibold is-size-5">
                        <span class="icon icon-btn">
                            <b-icon icon="truck" ></b-icon>
                        </span>Early Goers</p>
                    <br>
                    <p v-if="latecomers == null" class="has-text-centered has-text-grey-light">
                        <span class="icon icon-btn">
                            <b-icon icon="rotate-cw" animation="spin"></b-icon>
                        </span> Loading
                    </p>
                    <table class="table is-fullwidth is-hoverable">
                        <tbody>
                            <tr v-for="row in latecomers">
                                <td>
                                    <span class="is-capitalized is-size-5">{{ row[1].name}}</span>
                                    <br>
                                    <p class="has-text-weight-medium has-text-grey"
                                        v-html="titleCase(parsejson(row[1].company))"></p>
                                </td>
                                <td> <span class="has-text-weight-semibold">
                                        {{ row[1].early_att}}</span> Early Going
                                    <br>
                                    {{ row[1].day_att}}</span> Days Attended
                                </td>
                                <td>
                                    <button @click="viewReport(row[0])" class="button is-link is-outlined">
                                            <b-icon icon="file-chart"></b-icon>
<span class="ml-2">
                                        Reports
</span>
                                    </button></td>
                            </tr>
                        </tbody>
                    </table>

                </div>

            </div>
        </div>
    </div>
    </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      firms: [],
      latecomers: null,
      earlygoers: null,
    };
  },
  mounted() {
    let raw = this;
    this.$axios.post("/firms/info").then(function (response) {
      raw.firms = JSON.parse(response.data);
    });
    this.$axios
      .post("transaction/attendence/summary/latecomin")
      .then(function (response) {
        raw.latecomers = response.data.late;
        raw.earlygoers = response.data.early;
      });
  },
  methods: {
    formatedNumber(val) {
      let test = Number(val).toLocaleString("en-IN", {
        style: "currency",
        currency: "INR",
      });
      console.log(test);
      return test;
    },
    parsejson(val) {
      let company = JSON.parse(val);
      return company[0].name + ", " + company[0].location[0].name;
    },
    viewReport(id) {
      window.location.href = "/employee/view/detail/" + String(id);
    },
  },
};
</script>
