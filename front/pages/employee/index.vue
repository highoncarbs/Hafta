<template>
  <div>
    <div class="has-background-white" style="border-top: 1px solid #eee">
      <div
        class="section py-4 pt-5 is-fullwidth is-fullheight"
        :class="{ 'container px-0': $store.state.win }"
      >
        <!-- <transition name="fade"> -->
        <p class="is-size-5 has-text-weight-bold">Employees</p>
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
              <option :key="item.id" v-for="item in company_list" :value="item.id">{{titleCase(item.name)}}</option>
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
              <button
                @click="$router.push('/employee/view/' + props.row.id)"
                class="button is-link is-light"
              >
                <b-icon icon="pencil"></b-icon>
              </button>
              <button                 @click="$router.push('/employee/profile/' + props.row.id)"
 class="button is-link">
                <b-icon icon="eye"></b-icon>
              </button>
              <!-- <button class="button">
                <b-icon icon="poll-box"></b-icon>
              </button> -->
            </div>
          </b-table-column>
        </b-table>
      </div>
    </div>

    <b-modal v-model="showEmp">
      <div class="box">
        <p class="is-size-5 has-text-weight-bold">New Advance</p>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      data: [],
      showEmp: false,
      loading: false,
      query: null,
      showItems: 20,
      totalItems: null,
      currentPage: 1,
      filter_company: null,
      filter_advance: null,
      employee: null,
      company_list: [],
    };
  },
  mounted() {
    this.loadAsyncData();
    let self = this
    this.$axios.get('/master/get/company').then(response => {
      self.company_list = response.data
    })
  },
  methods: {
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
</style>