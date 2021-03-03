<template>
  <div>
    <!-- Mobile Nav -->

    <!-- Burger Navingation  -->

    <!-- Desktop Nav -->

    <nav
      class="level is-mobile is-hidden-touch has-background-black py-2 px-5 mb-0"
      style="border-bottom: 1px solid #eee"
    >
      <div class="level-left">
        <p class="level-item">
          <img src="~/static/logo.svg" width="20px" alt="" />
        </p>
      </div>
      <div class="level-right">
        <div class="level-item">
          <div class="has-dropdown is-hoverable">
            <b-dropdown :triggers="['hover']" aria-role="list">
              <p class="has-text-white" slot="trigger">
                <span class="icon icon-btn">
                  <b-icon icon="chart-pie" class="icon-btn" /> </span
                >General
                <b-icon icon="chevron-down" class="icon-btn" />
              </p>

              <nuxt-link
                v-for="(item, index) in general_items"
                :to="item.to"
                :key="'gen_' + index"
                exact-active-class="is-active"
              >
                <b-dropdown-item aria-role="listitem">
                  {{ item.title }}
                </b-dropdown-item>
              </nuxt-link>
            </b-dropdown>
          </div>
          <!-- <div class="has-dropdown is-hoverable">
            <b-dropdown :triggers="['hover']" aria-role="list">
              <p class="has-text-white" slot="trigger">
                <span class="icon icon-btn">
                  <b-icon icon="view-dashboard" class="icon-btn" /> </span
                >Reports
                <b-icon icon="chevron-down" class="icon-btn" />
              </p>

              <nuxt-link
                v-for="(item, index) in report_items"
                :to="item.to"
                :key="'report_' + index"
                exact-active-class="is-active"
              >
                <b-dropdown-item aria-role="listitem">
                  {{ item.title }}
                </b-dropdown-item>
              </nuxt-link>
            </b-dropdown>
          </div> -->
          <div class="has-dropdown is-hoverable">
            <b-dropdown :triggers="['hover']" aria-role="list">
              <p class="has-text-white" slot="trigger">
                <span class="icon icon-btn">
                  <b-icon icon="swap-vertical-circle" class="icon-btn" /> </span
                >Transactions
                <b-icon icon="chevron-down" class="icon-btn" />
              </p>
              <p class="dropdown-item heading is-size-7 has-text-grey">PAYROLL</p>
              <nuxt-link
                v-for="(item, index) in trans_items.payroll"
                :to="'/transaction' + item.to"
                :key="'trans_' + index"
                exact-active-class="is-active"
              >
                <b-dropdown-item aria-role="listitem">
                  {{ item.title }}
                </b-dropdown-item>
              </nuxt-link>
                <hr class="my-2">
              <p class="dropdown-item heading is-size-7 has-text-grey">HR</p>
              <nuxt-link
                v-for="(item, index) in trans_items.hr"
                :to="'/transaction' + item.to"
                :key="'trans_' + index"
                exact-active-class="is-active"
              >
                <b-dropdown-item aria-role="listitem">
                  {{ item.title }}
                </b-dropdown-item>
              </nuxt-link>
            </b-dropdown>
          </div>
          <div class="has-dropdown is-hoverable">
            <b-dropdown :triggers="['hover']" aria-role="list">
              <p class="has-text-white" slot="trigger">
                <span class="icon icon-btn">
                  <b-icon icon="layers" class="icon-btn" /> </span
                >Basic Master
                <b-icon icon="chevron-down" class="icon-btn" />
              </p>

              <nuxt-link
                v-for="(item, index) in basic_items"
                :to="'/basic' + item.to"
                :key="'basic_' + index"
                exact-active-class="is-active"
              >
                <b-dropdown-item aria-role="listitem">
                  {{ item.title }}
                </b-dropdown-item>
              </nuxt-link>
            </b-dropdown>
          </div>
        </div>
        <nuxt-link to="/employee/new" class="level-item has-text-white mr-6">
          <b-icon icon="account-supervisor-circle" />
          <span class="ml-2"> New Emp. </span>
        </nuxt-link>
        <p class="level-item button is-dark">
          <b-icon icon="exit-to-app"></b-icon>
          <span class="ml-2"> Logout </span>
        </p>
      </div>
    </nav>
    <nav
      class="level is-mobile mb-0 has-background-light py-1 px-4"
      style="border-bottom: 1.5px solid #e9e9e9"
    >
      <div class="level-left">
        <p
          @click="$router.back()"
          class="level-item button is-text has-text-dark"
        >
          <b-icon icon="arrow-left" class="mr-2"></b-icon>
          <span>Back</span>
        </p>
        <p
          class="level-item has-text-dark pl-5"
          v-if="$router.name"
          style="border-left: 1px solid #dbdbdb"
        >
          <span
            v-for="(row, idx) in $route.name.split('-')"
            :key="idx"
            class=""
          >
            <span v-if="row != 'id'"> </span>
            <span class="has-text-weight-semibold" v-else>
              {{ $route.params.id }}
            </span>
            <b-icon
              icon="chevron-right"
              v-show="idx + 1 < $route.name.split('-').length"
              class="icon-btn has-text-grey"
            ></b-icon>
          </span>
        </p>
      </div>
      <div class="level-right">
        <div class="level-item">
          <button @click="$store.commit('TOGGLE_WIN')" class="button is-text">
            <b-icon
              class="mr-2"
              :icon="
                $store.state.win
                  ? 'arrow-expand-all'
                  : 'arrow-collapse-horizontal'
              "
            ></b-icon>
            <span v-html="$store.state.win ? 'Expand' : 'Compact'"></span>
          </button>
        </div>
      </div>
    </nav>
    <transition name="fade">
      <section class="py-0 my-0">
        <nuxt />
      </section>
    </transition>

    <!-- <b-modal
      custom-class="has-overflow"
      trap-focus
      auto-focus
      :active.sync="glb_search"
    >
      <div class="box append-to-modal">
        <div class="control">
          <b-field>
            <template slot="label">
              <span class="has-text-weight-semibold has-text-grey">
                Global Search
              </span>
            </template>
            <b-autocomplete
              custom-class="g_input"
              v-model="g_search"
              placeholder="Search Pages "
              icon="magnify"
              @select="(option) => globalGoTo(option)"
              :data="autocompleteGlbSearch"
            >
              <template slot-scope="props">
                <div>
                  <div class="level is-mobile">
                    <div class="level-left">
                      <div class="level-item">
                        <span
                          class="tag has-text-weight-semibold heading"
                          :class="props.option.color"
                          >{{ props.option.master }}</span
                        >
                      </div>
                      <div class="level-item">
                        <span class="is-size-6">{{ props.option.title }}</span>
                      </div>
                    </div>
                    <div class="level-right">
                      <div
                        class="level-item"
                        v-if="props.option.type == 'path'"
                      >
                        <span class="">
                          <b-icon
                            class="has-text-grey-light"
                            icon="arrow-right-circle"
                          ></b-icon>
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
            </b-autocomplete>
          </b-field>
        </div>
      </div>
    </b-modal> -->
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from "vuex";

export default {
  components: {},
  data() {
    return {
      glb_search: false,
      expanded: false,
      g_search: null,
      basic_items: [
        {
          title: "Company",
          to: "/company",
        },
        {
          title: "Location",
          to: "/location",
        },
        {
          title: "City",
          to: "/city",
        },
        {
          title: "Emp. Category",
          to: "/category",
        },
        {
          title: "Appointment",
          to: "/appointment",
        },
        {
          title: "Department",
          to: "/department",
        },
        {
          title: "Post",
          to: "/post",
        },
        {
          title: "Benefits",
          to: "/benefits",
        },
        {
          title: "Mode of Pay",
          to: "/modeofpay",
        },
        {
          title: "Performance Factor",
          to: "/performance",
        },
        {
          title: "Attendence Rules",
          to: "/attendence",
        },
      ],
      trans_items: {
        payroll: [
          {
            title: "Salary Sheet",
            to: "/salary-sheet",
          },
          {
            title: "Advance",
            to: "/advance",
          },

          {
            title: "Attendence",
            to: "/attendence",
          },
        ],
        hr: [
          {
            title: "Performance",
            to: "/performance",
          },
          {
            title: "Quick Report",
            to: "/quick-report",
          },
        ],
      },

      report_items: [
        {
          title: "Salary Sheet",
          to: "/",
        },
        {
          title: "Advance",
          to: "/",
        },
        {
          title: "Salary Slips",
          to: "/",
        },
        {
          title: "Performance",
          to: "/",
        },
      ],
      general_items: [
        {
          title: "Dashboard",
          to: "/",
        },
        {
          title: "Firms",
          to: "/firms",
        },
        {
          title: "Employees",
          to: "/employee",
        },
      ],
    };
  },
  methods: {
    logoutUser() {
      this.$auth.logout().then(() => {
        this.$router.push("/auth");
      });
    },

    globalGoTo(opt) {
      if (opt.type == "path") {
        this.$router.push(opt.to);
        this.glb_search = false;
      }
    },
    showNav() {},
  },
  computed: {
    // autocompleteGlbSearch() {
    //   if (this.g_search == null) {
    //     return this.all_paths;
    //   } else {
    //     return this.all_paths.filter((option) => {
    //       return (
    //         option.title
    //           .toString()
    //           .toLowerCase()
    //           .indexOf(this.g_search.toLowerCase()) >= 0
    //       );
    //     });
    //   }
    // },
  },
  mounted() {},
};
</script>
<style>
* {
  font-family: "Inter", "Roboto", "Helvetica", "Segoe UI", sans-serif !important;
}
html {
  background-color: whitesmoke !important;
}

.b-sidebar .sidebar-content {
  width: 450px !important;
   z-index:99;
}

.libre {
  font-family: Georgia, Times, "Times New Roman", serif;
  font-weight: 700;
  letter-spacing: -1px;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-active {
  opacity: 0;
}

.icon-btn {
  margin: 0 10px 1px 10px !important;
  vertical-align: middle !important;
  /* color: linear-gradient(#eee , #ccc) */
}
.icon-btn-l {
  margin: 0 10px 1px 1px !important;
  vertical-align: middle !important;
}

.icon-in {
  margin: 0 5px 1px 5px !important;
  vertical-align: middle !important;
}

.is-fullheight {
  min-height: 90vh;
  /* max-height: 100% !important; */
  /* height: 100% !important; */
}
.router-link-active {
  color: green;
}

.button {
  font-family: "Inter", "Roboto", "Helvetica", "Segoe UI", sans-serif !important;
}

.tabs .nuxt-link-active {
  background-color: white !important;
  color: black;
  border: 1px solid #dbdbdb !important;
  /* border-bottom-color: black !important; */
}
.tabs .nuxt-link-active:hover {
  color: black;
  /* border-bottom-color: black; */
}
.has-background-dark-pep {
  background-color: #15161c !important;
}

.g_input {
  border: None !important;
  box-shadow: None !important;
}

.control .autocomplete {
  width: auto !important;
}

.box {
  box-shadow: none !important;
  border: 1px solid #dbdbdb;
}

/* .required{
  width:7px;
  height:7px;
  border-radius:50%;
  background-color: #714dd2;;
  display: inline-block;
  border:1px solid #c1acfa;


}
   */
</style> */