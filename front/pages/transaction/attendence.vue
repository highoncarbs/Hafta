<template>
  <div>
    <div class="has-background-white" style="border-top: 1px solid #eee">
      <div
        class="section py-4 pt-5 is-fullwidth is-fullheight"
        :class="{ 'container px-0': $store.state.win }"
      >
        <!-- <transition name="fade"> -->
        <div v-if="showView">
          <p class="is-size-5 has-text-weight-bold">Attendence</p>
          <br />
          <div class="columns">
            <div
              class="column is-3"
              v-for="(item, index) in data_company"
              :key="index"
            >
              <div class="box">
                <p class="tag heading is-rounded  is-warning mb-4" v-if="item.status == 'pending'">
                  <span class="dot-warning"></span>
                  pending - {{ new Date().toLocaleString('default', { month: 'short' })}}
                </p>
                <p class="tag heading is-rounded is-info mb-4" v-if="item.status == 'done'">
                  <span class="dot-link"></span>
                  Attendence Done - {{ new Date().toLocaleString('default', { month: 'short' })}}
                </p>
                <p class="is-size-4 has-text-weight-bold">
                  {{ titleCase(item.name) }}
                </p>
                <hr class="my-2">
                <p class="is-size-5 mt-2">{{ item.num }} Employees</p>
                <p class="is-size-5 is-family-monospace">INR {{ item.payout.toLocaleString('en-IN') }}</p>
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
                  @click="getEmployee(item)"
                  class="button is-fullwidth is-link"
                >
                  Enter Attendence
                </button>
              </div>
            </div>
          </div>
        </div>
        <!-- </transition> -->
        <div v-if="!showView">
          <button class="button mb-4" @click="showView = !showView">
            <b-icon icon="chevron-left"></b-icon>
            <span>Back to Firms</span>
          </button>
          <br />
         <p class="tag heading is-rounded is-warning mb-4" v-if="company.status == 'pending'">
                  <span class="dot-warning"></span>
                  pending - {{ new Date().toLocaleString('default', { month: 'short' })}}
                </p>
                <p class="tag heading is-rounded is-info mb-4" v-if="company.status == 'done'">
                  <span class="dot-link"></span>
                  Attendence Done - {{ new Date().toLocaleString('default', { month: 'short' })}}
                </p>
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
                  <p class="heading">ATTENDENCE FOR</p>
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

          <!-- <div
            class="box has-background-warning-light py-2 hast-text-warning-dark"
            v-if="attendenceList.length != 0"
          >
            <div class="level">
              <div class="level-left">
                <p
                  v-if="attendenceList.length > 4"
                  class="has-text-weight-bold"
                >
                  Data already entered for :
                  {{ attendenceList.length }} employees
                </p>
                <p v-else>
                    <b-icon icon="information"></b-icon>
                  <span
                    
                  >
                    Pre filled data has already been added
                  </span>
                </p>
              </div>
              <div class="level-right">
                <div class="butttons">
                  <button class="button " @click="attModal = !attModal">
                    View
                  </button>
                  <button
                    class="button is-warning is-dark"
                    @click="showEditTable = !showEditTable"
                  >
                  </button>
                </div>
              </div>
            </div>
          </div> -->

          <p
            v-if="isLoading"
            class="has-text-centered is-size-4 has-text-grey-light"
          >
            <br />
            <span class="icon icon-btn">
              <feather type="rotate-cw" animation="spin"></feather>
            </span>
            Loading
          </p>
          <b-field
            grouped
            group-multiline
            v-if="data && data.length != 0 && !showEditTable"
          >
            <b-input
              expanded
              icon="magnify"
              placeholder="Search Employees"
              v-model="searchQuery"
            ></b-input>
            <p class="control">
              <button
                class="button"
                @click="
                  () => {
                    searchQuery = '';
                  }
                "
              >
                Clear
              </button>
            </p>
          </b-field>
          <b-table :data="filteredList" :empty="filteredList.length == 0">
            <!-- <b-table-column label="ID" feild="id">{{ props.row.id}}</b-table-column> -->
            <b-table-column label="" v-slot="props">
              <button
                class="button is-link is-light"
                @click="employeeDetail(props.row.id)"
              >
                <b-icon icon="information" class=""></b-icon>
              </button>
            </b-table-column>
            <b-table-column label="Name" v-slot="props">{{
              props.row.name
            }}</b-table-column>
            <b-table-column
              label="Department"
              v-slot="props"
              class="has-text-grey-light"
            >
              <span
                class="has-text-grey"
                v-if="props.row.department.length == 0"
              >
                None
              </span>
              <span v-else>
                {{ props.row.department[0].name }}
              </span>
            </b-table-column>
            <b-table-column
              label="Post"
              v-slot="props"
              class="has-text-grey-light"
            >
              <span class="has-text-grey" v-if="props.row.post.length == 0">
                None
              </span>
              <span v-else>
                {{ props.row.post[0].name }}
              </span>
            </b-table-column>
            <b-table-column label="Days Attended 30 DAYS" v-slot="props">
              <b-field
                :type="{
                  'is-danger':
                    errors[props.row.id] != undefined &&
                    errors[props.row.id].daysatt == true,
                }"
              >
                <b-input
                  v-model.number="props.row.daysatt"
                  placeholder="Days Attended"
                ></b-input>
              </b-field>
            </b-table-column>
            <b-table-column label="Late Come In" v-slot="props">
              <b-field
                :type="{
                  'is-danger':
                    errors[props.row.id] != undefined &&
                    errors[props.row.id].latecomin == true,
                }"
              >
                <b-input
                  v-model.number="props.row.latecomin"
                  placeholder="Late Come In"
                ></b-input>
              </b-field>
            </b-table-column>
            <b-table-column label="Early Going" v-slot="props">
              <b-field
                :type="{
                  'is-danger':
                    errors[props.row.id] != undefined &&
                    errors[props.row.id].earlygoing == true,
                }"
              >
                <b-input
                  v-model.number="props.row.earlygoing"
                  placeholder="Early Going"
                ></b-input>
              </b-field>
            </b-table-column>
            <b-table-column label="PF" v-slot="props">
              <b-field
                :type="{
                  'is-danger':
                    errors[props.row.id] != undefined &&
                    errors[props.row.id].pf == true,
                }"
              >
                <b-input
                  :disabled="props.row.pf == 'no'"
                  v-model.number="props.row.pfval"
                  placeholder="PF"
                ></b-input>
              </b-field>
            </b-table-column>
            <b-table-column label="ESI" v-slot="props">
              <b-field
                :type="{
                  'is-danger':
                    errors[props.row.id] != undefined &&
                    errors[props.row.id].esi == true,
                }"
              >
                <b-input
                  :disabled="props.row.esi == 'no'"
                  v-model.number="props.row.esival"
                  placeholder="EDI"
                ></b-input>
              </b-field>
            </b-table-column>
            <b-table-column label="TDS" v-slot="props">
              <b-field>
                <b-input
                  v-model.number="props.row.tdsval"
                  placeholder="TDS"
                ></b-input>
              </b-field>
            </b-table-column>
            <b-table-column label="Other Deduction" v-slot="props">
              <b-field>
                <b-input
                  v-model.number="props.row.other_deduction"
                  placeholder="Other Deduction"
                ></b-input>
              </b-field>
            </b-table-column>
          </b-table>
          <br />
          <div class="buttons">
            <button class="button is-black" @click="submitData" >
              <b-icon icon="check"></b-icon>
              <span class="ml-2"> Save </span>
            </button>
          </div>

          <!-- Employee Detail  Popup-->
          <b-modal v-model="detailModal">
            <div class="box">
              <p v-if="empDetail == null" class="has-text-grey">
                <span class="icon icon-btn">
                  <feather
                    type="rotate-cw"
                    animation="spin"
                    animation-speed="slow"
                  ></feather>
                </span>
                Fetching data
              </p>
              <div v-if="empDetail != null" class="animated fadeIn">
                <div class="level is-mobile">
                  <div class="level-left">
                    <h2 class="is-size-5 has-text-weight-medium">
                      {{ empDetail.name }}
                    </h2>
                  </div>
                  <div class="level-right">
                    <div class="level-item">
                      <a href="" class="button">
                        <b-icon icon="pencil"></b-icon>

                        <span class="ml-2"> Edit </span>
                      </a>
                    </div>
                    <div class="level-item">
                      <a href="" class="button is-black">
                        <b-icon icon="file-chart"></b-icon>

                        <span class="ml-2"> Report </span>
                      </a>
                    </div>
                  </div>
                </div>

                <table class="table is-bordered is-fullwidth">
                  <thead>
                    <tr>
                      <td colspan="2">
                        <small class="has-text-weight-semibold"> NAME</small>

                        <p>{{ empDetail.name }}</p>
                      </td>
                      <td colspan="1">
                        <small class="has-text-weight-semibold">
                          DATE OF BIRTH</small
                        >

                        <p>{{ formatedDate(empDetail.dob) }}</p>
                      </td>
                      <td colspan="1">
                        <small class="has-text-weight-semibold">
                          FATHER'S NAME</small
                        >
                        <p>{{ empDetail.fathername }}</p>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="2">
                        <small class="has-text-weight-semibold">CONTACT</small>
                        <p
                          v-html="
                            empDetail.contact != undefined
                              ? empDetail.contact
                              : 'None'
                          "
                        ></p>
                      </td>
                      <td colspan="1">
                        <small class="has-text-weight-semibold">
                          SPOUSE NAME</small
                        >

                        <p
                          v-html="
                            empDetail.spousename != undefined
                              ? empDetail.spousename
                              : 'None'
                          "
                        ></p>
                      </td>
                      <td colspan="1">
                        <small class="has-text-weight-semibold">
                          EDUCATION</small
                        >

                        <p
                          v-html="
                            empDetail.education != undefined
                              ? empDetail.education
                              : 'None'
                          "
                        ></p>
                      </td>
                    </tr>
                  </thead>
                  <tbody>
                    <tr></tr>
                    <tr>
                      <td colspan="2">
                        <small class="has-text-weight-semibold"
                          >CURRENT ADDRESS</small
                        >
                        <p
                          v-html="
                            empDetail.curr_address != undefined
                              ? empDetail.curr_address
                              : 'None'
                          "
                        ></p>
                        <p
                          v-html="
                            empDetail.curr_city != undefined
                              ? empDetail.curr_city
                              : 'None'
                          "
                        ></p>
                      </td>
                      <td colspan="2">
                        <small class="has-text-weight-semibold">
                          PERMANENT ADDRESS</small
                        >

                        <p
                          v-html="
                            empDetail.perm_address != undefined
                              ? empDetail.perm_address
                              : 'None'
                          "
                        ></p>
                        <p
                          v-html="
                            empDetail.perm_city != undefined
                              ? empDetail.perm_city
                              : 'None'
                          "
                        ></p>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="1">
                        <small class="has-text-weight-semibold">
                          AADHAR NO</small
                        >

                        <p
                          v-html="
                            empDetail.aadahr != undefined
                              ? empDetail.aadhar
                              : 'None'
                          "
                        ></p>
                      </td>
                      <td colspan="2">
                        <small class="has-text-weight-semibold">PAN NO</small>
                        <p
                          v-html="
                            empDetail.pan != undefined ? empDetail.pan : 'None'
                          "
                        ></p>
                      </td>

                      <td colspan="1">
                        <small class="has-text-weight-semibold">
                          REFERENCE</small
                        >

                        <p
                          v-html="
                            empDetail.reference != undefined
                              ? empDetail.reference
                              : 'None'
                          "
                        ></p>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="4">
                        <small class="has-text-weight-semibold">
                          DATE OF APPOINTMENT</small
                        >

                        <p
                          v-html="
                            empDetail.dateofapp != undefined
                              ? formatedDate(empDetail.dateofapp)
                              : 'None'
                          "
                        ></p>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="1">
                        <small class="has-text-weight-semibold">
                          APPOINTMENT</small
                        >

                        <p
                          v-html="
                            empDetail.appointment != undefined
                              ? empDetail.appointment
                              : 'None'
                          "
                        ></p>
                      </td>
                      <td colspan="1">
                        <small class="has-text-weight-semibold">POST</small>
                        <p
                          v-html="
                            empDetail.post != undefined
                              ? empDetail.post
                              : 'None'
                          "
                        ></p>
                      </td>

                      <td colspan="1">
                        <small class="has-text-weight-semibold">
                          DEPARTMENT</small
                        >

                        <p
                          v-html="
                            empDetail.department != undefined
                              ? empDetail.department
                              : 'None'
                          "
                        ></p>
                      </td>
                      <td colspan="1">
                        <small class="has-text-weight-semibold"> COMPANY</small>

                        <p
                          v-html="
                            empDetail.company != undefined
                              ? empDetail.company
                              : 'None'
                          "
                        ></p>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="4">
                        <small class="has-text-weight-semibold">
                          BENEFITS</small
                        >

                        <p
                          v-html="
                            empDetail.company != undefined
                              ? empDetail.company
                              : 'None'
                          "
                        ></p>
                      </td>
                    </tr>
                    <tr class="has-background-light">
                      <td colspan="4">
                        <p class="is-size-6 has-text-weight-semibold">
                          SALARY STRUCTURE
                        </p>
                      </td>
                    </tr>
                    <tr class="has-background-light">
                      <td colspan="2">
                        <small class="has-text-weight-semibold">
                          EFFECTIVE DATE</small
                        >

                        <p
                          v-html="
                            empDetail.dateeff != undefined
                              ? formatedDate(empDetail.dateeff)
                              : 'None'
                          "
                        ></p>
                      </td>
                      <td colspan="2">
                        <small class="has-text-weight-semibold">
                          PAYMENT MODEL</small
                        >

                        <p
                          v-html="
                            empDetail.salary_structure != undefined
                              ? empDetail.salary_structure
                              : 'None'
                          "
                        ></p>
                      </td>
                    </tr>
                    <tr class="has-background-light">
                      <td colspan="2">
                        <small class="has-text-weight-semibold">
                          BASIC PAY</small
                        >

                        <p
                          v-html="
                            empDetail.basicpay != undefined
                              ? formatedNumber(empDetail.basicpay)
                              : 'None'
                          "
                        ></p>
                      </td>
                      <td colspan="1">
                        <small class="has-text-weight-semibold">P.F</small>
                        <p
                          v-html="
                            empDetail.pf != undefined ? empDetail.pf : 'None'
                          "
                        ></p>
                      </td>

                      <td colspan="1">
                        <small class="has-text-weight-semibold"> ESI</small>

                        <p
                          v-html="
                            empDetail.esi != undefined ? empDetail.esi : 'None'
                          "
                        ></p>
                      </td>
                    </tr>
                    <tr class="has-background-light">
                      <td colspan="1">
                        <small class="has-text-weight-semibold">
                          SALARY ADVANCE</small
                        >

                        <p
                          v-html="
                            empDetail.advance != undefined
                              ? empDetail.advance
                              : 'None'
                          "
                        ></p>
                      </td>
                      <td colspan="2">
                        <small class="has-text-weight-semibold"
                          >MAX. ADVANCE</small
                        >
                        <p
                          v-html="
                            empDetail.advancevalue != undefined
                              ? formatedNumber(empDetail.advancevalue)
                              : 'None'
                          "
                        ></p>
                      </td>

                      <td colspan="1">
                        <small class="has-text-weight-semibold"> ESI</small>

                        <p
                          v-html="
                            empDetail.advancenum != undefined
                              ? empDetail.advancenum
                              : 'None'
                          "
                        ></p>
                      </td>
                    </tr>
                    <tr class="has-background-light">
                      <td colspan="2">
                        <small class="has-text-weight-semibold"
                          >PAID LEAVES</small
                        >
                        <small>IN A YEAR</small>

                        <p
                          v-html="
                            empDetail.paidleave != undefined
                              ? empDetail.paidleave
                              : 'None'
                          "
                        ></p>
                      </td>
                      <td colspan="2">
                        <small class="has-text-weight-semibold"
                          >INCREMENT PERIOD</small
                        >
                        <small>IN MONTHS</small>

                        <p
                          v-html="
                            empDetail.incrementpr != undefined
                              ? empDetail.incrementpr
                              : 'None'
                          "
                        ></p>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </b-modal>
          <!-- <div :class="{ 'is-active' : detailModal }" class="modal  ">
            <div class="modal-background animated fadeIn" @click="detailModal = !detailModal"></div>
            <div class="modal-content animated fadeIn ">

                <div class="box">

                    <p v-if="empDetail == null " class="has-text-grey">
                        <span class="icon icon-btn">
                            <feather type="rotate-cw" animation="spin" animation-speed="slow"></feather>
                        </span>
                        Fetching data
                    </p>
                    <div v-if="empDetail != null " class="animated fadeIn">
                        <div class="level is-mobile">
                            <div class="level-left">
                                <h2 class="is-size-5 has-text-weight-medium"> {{ empDetail.name }} </h2>

                            </div>
                            <div class="level-right">
                                <div class="level-item">
                                    <a href="" class="button"><span class="icon icon-btn">
                                            <feather type="edit" size="1.3rem"></feather>
                                        </span> Edit</a>
                                </div>
                                <div class="level-item">
                                    <a href="" class="button is-black"><span class="icon icon-btn">
                                            <feather type="bar-chart-2" size="1.3rem"></feather>
                                        </span> Report</a>

                                </div>


                            </div>
                        </div>

                        <table class="table is-bordered is-fullwidth">
                            <thead>
                                <tr>
                                    <td colspan="2">
                                        <small class="has-text-weight-semibold"> NAME</small>

                                        <p> {{ empDetail.name }}</p>
                                    </td>
                                    <td colspan="1">
                                        <small class="has-text-weight-semibold"> DATE OF BIRTH</small>

                                        <p>{{ formatedDate(empDetail.dob) }} </p>
                                    </td>
                                    <td colspan="1">

                                        <small class="has-text-weight-semibold"> FATHER'S NAME</small>
                                        <p>{{ empDetail.fathername }}
                                        </p>

                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="2">

                                        <small class="has-text-weight-semibold">CONTACT</small>
                                        <p v-html=" empDetail.contact != undefined ? empDetail.contact : 'None'">
                                        </p>
                                    </td>
                                    <td colspan="1">
                                        <small class="has-text-weight-semibold"> SPOUSE NAME</small>

                                        <p v-html=" empDetail.spousename != undefined ? empDetail.spousename : 'None'">
                                        </p>

                                    </td>
                                    <td colspan="1">
                                        <small class="has-text-weight-semibold"> EDUCATION</small>

                                        <p v-html=" empDetail.education != undefined ? empDetail.education : 'None'">
                                        </p>

                                    </td>

                                </tr>
                            </thead>
                            <tbody>
                                <tr>

                                </tr>
                                <tr>
                                    <td colspan="2">

                                        <small class="has-text-weight-semibold">CURRENT ADDRESS</small>
                                        <p
                                            v-html=" empDetail.curr_address != undefined ? empDetail.curr_address : 'None'">
                                        </p>
                                        <p v-html=" empDetail.curr_city != undefined ? empDetail.curr_city : 'None'">
                                        </p>
                                    </td>
                                    <td colspan="2">
                                        <small class="has-text-weight-semibold"> PERMANENT ADDRESS</small>

                                        <p
                                            v-html=" empDetail.perm_address != undefined ? empDetail.perm_address : 'None'">
                                        </p>
                                        <p v-html=" empDetail.perm_city != undefined ? empDetail.perm_city : 'None'">
                                        </p>

                                    </td>
                                </tr>
                                <tr>
                                <tr>
                                    <td colspan="1">
                                        <small class="has-text-weight-semibold"> AADHAR NO</small>

                                        <p v-html=" empDetail.aadahr != undefined ? empDetail.aadhar : 'None'">
                                        </p>

                                    </td>
                                    <td colspan="2">

                                        <small class="has-text-weight-semibold">PAN NO</small>
                                        <p v-html=" empDetail.pan != undefined ? empDetail.pan : 'None'">
                                        </p>
                                    </td>

                                    <td colspan="1">
                                        <small class="has-text-weight-semibold"> REFERENCE</small>

                                        <p v-html=" empDetail.reference != undefined ? empDetail.reference : 'None'">
                                        </p>

                                    </td>

                                </tr>
                                </tr>
                                <tr>
                                    <td colspan="4">
                                        <small class="has-text-weight-semibold"> DATE OF APPOINTMENT</small>

                                        <p
                                            v-html="empDetail.dateofapp != undefined ?  formatedDate(empDetail.dateofapp) : 'None'">
                                        </p>

                                    </td>

                                </tr>
                                <tr>
                                    <td colspan="1">
                                        <small class="has-text-weight-semibold"> APPOINTMENT</small>

                                        <p
                                            v-html=" empDetail.appointment != undefined ? empDetail.appointment : 'None'">
                                        </p>

                                    </td>
                                    <td colspan="1">

                                        <small class="has-text-weight-semibold">POST</small>
                                        <p v-html=" empDetail.post != undefined ? empDetail.post : 'None'">
                                        </p>
                                    </td>

                                    <td colspan="1">
                                        <small class="has-text-weight-semibold"> DEPARTMENT</small>

                                        <p v-html=" empDetail.department != undefined ? empDetail.department : 'None'">
                                        </p>

                                    </td>
                                    <td colspan="1">
                                        <small class="has-text-weight-semibold"> COMPANY</small>

                                        <p v-html=" empDetail.company != undefined ? empDetail.company : 'None'">
                                        </p>

                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="4">
                                        <small class="has-text-weight-semibold"> BENEFITS</small>

                                        <p v-html=" empDetail.company != undefined ? empDetail.company : 'None'">
                                        </p>

                                    </td>
                                </tr>
                                <tr class="has-background-light">
                                    <td colspan="4">
                                        <p class="is-size-6 has-text-weight-semibold">SALARY STRUCTURE</p>

                                    </td>

                                </tr>
                                <tr class="has-background-light">
                                    <td colspan="2">
                                        <small class="has-text-weight-semibold"> EFFECTIVE DATE</small>

                                        <p
                                            v-html="empDetail.dateeff != undefined ?  formatedDate(empDetail.dateeff) : 'None'">
                                        </p>
                                    </td>
                                    <td colspan="2">
                                        <small class="has-text-weight-semibold"> PAYMENT MODEL</small>

                                        <p
                                            v-html="empDetail.salary_structure != undefined ?  empDetail.salary_structure : 'None'">
                                        </p>
                                    </td>
                                </tr>
                                <tr class="has-background-light">
                                    <td colspan="2">
                                        <small class="has-text-weight-semibold"> BASIC PAY</small>

                                        <p
                                            v-html=" empDetail.basicpay != undefined ? formatedNumber(empDetail.basicpay) : 'None'">
                                        </p>

                                    </td>
                                    <td colspan="1">

                                        <small class="has-text-weight-semibold">P.F</small>
                                        <p v-html=" empDetail.pf != undefined ? empDetail.pf : 'None'">
                                        </p>
                                    </td>

                                    <td colspan="1">
                                        <small class="has-text-weight-semibold"> ESI</small>

                                        <p v-html=" empDetail.esi != undefined ? empDetail.esi : 'None'">
                                        </p>

                                    </td>
                                </tr>
                                <tr class="has-background-light">
                                    <td colspan="1">
                                        <small class="has-text-weight-semibold"> SALARY ADVANCE</small>

                                        <p v-html=" empDetail.advance != undefined ? empDetail.advance : 'None'">
                                        </p>

                                    </td>
                                    <td colspan="2">

                                        <small class="has-text-weight-semibold">MAX. ADVANCE</small>
                                        <p
                                            v-html=" empDetail.advancevalue != undefined ? formatedNumber(empDetail.advancevalue) : 'None'">
                                        </p>
                                    </td>

                                    <td colspan="1">
                                        <small class="has-text-weight-semibold"> ESI</small>

                                        <p v-html=" empDetail.advancenum != undefined ? empDetail.advancenum : 'None'">
                                        </p>

                                    </td>
                                </tr>
                                <tr class="has-background-light">

                                    <td colspan="2">
                                        <small class="has-text-weight-semibold">PAID LEAVES</small>
                                        <small>IN A YEAR</small>

                                        <p v-html=" empDetail.paidleave != undefined ? empDetail.paidleave : 'None'">
                                        </p>

                                    </td>
                                    <td colspan="2">

                                        <small class="has-text-weight-semibold">INCREMENT PERIOD</small>
                                        <small>IN MONTHS</small>

                                        <p
                                            v-html=" empDetail.incrementpr != undefined ? empDetail.incrementpr : 'None'">
                                        </p>
                                    </td>

                                </tr>
                            </tbody>

                        </table>


                    </div>

                </div>
                <button class="modal-close is-large" @click="detailModal = !detailModal"></button>

            </div>

        </div> -->

          <!-- Attendence detail List popup -->

          <!-- <div v-if="attModal" :class="{ 'is-active' : attModal }" class="modal  ">
            <div class="modal-background animated fadeIn" @click="attModal = !attModal"></div>
            <div class="modal-content animated fadeIn ">

                <div class="box is-fullwidth ">
                    <div class="table-container">
                        <table class="table is-fullwidth is-bordered">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Days Attended</th>
                                    <th>Late Come in</th>
                                    <th>Early Going</th>
                                    <th>PF</th>
                                    <th>ESI</th>
                                    <th>TDS</th>
                                    <th>Other Deduction</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="row in attendenceList">
                                    <td> {{ row.employee[0].id }} </td>
                                    <td> {{ row.employee[0].name }} </td>
                                    <td>{{ row.daysatt }} / <span class=" has-text-grey-light"> 30</span> </td>
                                    <td> {{ row.latecomin }} </td>
                                    <td> {{ row.earlygoing }} </td>
                                    <td> {{ row.pf }} </td>
                                    <td> {{ row.esi }} </td>
                                    <td> {{ row.tds }} </td>
                                    <td> {{ row.other_deduction }} </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                </div>
                <button class="modal-close is-large" @click="attModal = !attModal"></button>

            </div>

        </div> -->
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
      data_company: [
        
      ],
      data: null,
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

    this.$axios.get('/master/get/company/detail').then( response => {
      this.data_company = response.data
      this.data_company.forEach( (item) => {
        this.$axios.post('/transaction/attendence/status', {'id':item.id , 'date': new Date()}).then (response =>{
          this.$set(item , 'status', response.data.status)
        })
      })
    })
  },
  computed: {
    //  TODO:   load on click only - FIX
    filteredList() {
      if (this.data.length != 0) {
        if (this.searchQuery != "") {
          return this.data.filter((data) => {
            return data.name
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase());
          });
        }

        return this.data;
      }
      return this.data;
    },
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
    employeeDetail(id) {
      this.detailModal = !this.detailModal;
      let self = this;
      this.$axios
        .post("/employee/get/profile/" + String(id))
        .then(function (response) {
          self.empDetail = response.data;
        });
    },
    getAttendence(company) {
      let self = this;
      let attendenceform = { company: company, date: this.month };
      this.$axios
        .post("/transaction/attendence/get", attendenceform)
        .then(function (response) {
          self.showView = !self.showView;

          self.attendenceList = [];
          self.attendenceList = response.data;

          // Removes data from dataList if item present in AttendenceList
          self.attendenceList.forEach(function (item) {
            if (self.dataList.length != 0)
              self.dataList.forEach(function (check, index) {
                if (check.id == item.employee[0].id) {
                  check.daysatt = item.daysatt
                  check.latecomin = item.latecomin
                  check.earlygoing = item.earlygoing
                  check.pfval = item.pf
                  check.esival = item.esi
                  check.tdsval = item.tds
                  check.att_id = item.id
                  check.other_deduction = item.other_deduction
                }
              });
          });

          self.data = self.dataList;
        });
    },
    getEmployee(company) {
      let self = this;
      this.errors = [];
      this.data = null;
      this.dataList = [];
      this.company = company;
      this.attModal = false;
      this.showEditTable = false;
      if (this.month) {
        this.isLoading = true;
        this.$axios
          .get("/employee/get/by/company/" + company.id)
          .then(function (response) {
            console.log(response.data);
            // self.data = JSON.parse(response.data)
            self.dataList = response.data;
            self.getAttendence(company.id);
            self.isLoading = false;
          });

        //    Need to pop emps whose data is already been filled
      } else {
        this.$set(
          this.errors,
          "submit",
          "Please select both company and month."
        );
      }
      //   e.preventDefault();
    },
    updateData(e) {
      let self = this;
      let formdata = {
        company: this.company,
        date: this.month,
        data: this.attendenceList,
      };
      this.$axios
        .post("/transaction/attendence/update", self.attendenceList)
        .then(function (response) {
          console.log(response);
          if (response.data.success) {
            self.$buefy.snackbar.open({
              duration: 5000,
              message: response.data.success,
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                this.isActive = false;
              },
            });
          }

          if (response.data.message) {
            self.$buefy.snackbar.open({
              duration: 8000,
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

      e.preventDefault();
    },
    submitData() {
      let self = this;

      if (this.checkData()) {
        this.submitting = true;
        this.value = "Saving";
        let formdata = {
          company: this.company,
          date: this.month,
          data: this.filteredList,
        };
        console.log(formdata);
        this.$axios
          .post("/transaction/attendence/save", formdata)
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

              self.getAttendence(this.company.id);
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
          })
          .catch(function (error) {
            // RUn error
            console.error(error);
          });
      }
      this.submitting = false;
      this.value = "Save";
    },
    checkData() {
      this.errors = [];
      let raw = this;
      let rawError = this.errors;
      this.dataList.forEach(function (item) {
        if (item.daysatt == undefined) {
          if (rawError[item.id]) {
            raw.$set(rawError[item.id], "daysatt", true);
          } else {
            raw.$set(rawError, item.id, {});
            raw.$set(rawError[item.id], "daysatt", true);
          }
        }
        if (item.latecomin == undefined) {
          if (rawError[item.id]) {
            raw.$set(rawError[item.id], "latecomin", true);
          } else {
            raw.$set(rawError, item.id, {});
            raw.$set(rawError[item.id], "latecomin", true);
          }
        }
        if (item.earlygoing == undefined) {
          if (rawError[item.id]) {
            raw.$set(rawError[item.id], "earlygoing", true);
          } else {
            raw.$set(rawError, item.id, {});
            raw.$set(rawError[item.id], "earlygoing", true);
          }
        }

        // Reconsider how to set this up

        // if(item.pfval == null || item.pfval == undefined ){
        //     this.$set(this.errors , 'pfval' , 'Please fill out P.F . Set <b>0</b> for None/Null')
        // }
        // if(item.esival== null || item.esival == undefined ){
        //     this.$set(this.errors , 'esival' , 'Please fill out ESI . Set <b>0</b> for None/Null')
        // }
      });

      if (Object.keys(this.errors).length == 0) {
        return true;
      } else {
        return false;
      }
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
  background-color: hsl(0, 0%, 100%);
}
</style>