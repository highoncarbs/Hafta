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
          <div class="level is-mobile">
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
      <b-sidebar
        mobile="fullwidth"
        type="is-white"
        :fullheight="true"
        :overlay="true"
        :right="true"
        :open.sync="showRemarks"
      >
        <div class="my-4 px-4" v-if="remarks_id != null">
          <div class="level is-mobile">
            <div class="left-left">
              <div class="level-item">
                <p class="has-text-weight-medium is-size-5">Add Remarks</p>
              </div>
            </div>
            <div class="left-right">
              <div class="level-item">
                <p @click="showRemarks = !showRemarks" class="delete"></p>
              </div>
            </div>
          </div>
          <hr class="my-2" />
          <p class="is-size-4 has-text-weight-bold">{{salarySheet[remarks_id].employee[0].name}}</p>
          <br />
          <div class="level">
            <div class="level-left">
                              <div>
<p class="heading">COMPANY</p>

              <div class="level-item"><span class="is-size-5">{{titleCase(salarySheet[remarks_id].employee[0].company[0].name)}}</span></div>
            </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <div>
<p class="heading">SALARY</p>
                          <p class="is-size-5">{{formatedNumber(salarySheet[remarks_id].net_payable)}}</p>
                </div>
</div>
            </div>
          </div>
          
          <b-field >
            <div class="control">
              <b-field label="Remarks" >
                <b-input type="textarea" placeholder="Add Remarks or Salary Payment Note" v-model="salarySheet[remarks_id].remarks"></b-input>
              </b-field>
            </div>
          
          </b-field>
        <button class="button is-black" @click="resetRemark">Save & Close</button>
        </div>
      </b-sidebar>
       <b-sidebar
      mobile="fullwidth"
      type="is-white"
      :fullheight="true"
      :overlay="true"
      :right="true"
      :open.sync="showSide"
    >
      <div class="my-4 px-4">
        <p
          v-if="employee_adv_deets != null"
          class="has-text-weight-medium is-size-5"
        >
          Advances for {{ this.employee_adv_deets.name }}
        </p>
        <hr class="my-2" />
        <b-table
          :data="advance_list.filter((item) => item.trans == 'credit')"
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
          <b-table-column label="Amt." v-slot="props">{{
            formatedNumber(props.row.advanceamt)
          }}</b-table-column>
          <b-table-column label="Ded." v-slot="props"
            >{{ formatedNumber(props.row.deduction) }} /
            <span class="has-text-grey has-text-weight-medium">{{
              props.row.deduction_period
            }}</span></b-table-column
          >
        </b-table>
      </div>
    </b-sidebar>
    <b-sidebar
      mobile="fullwidth"
      type="is-white"
      :fullheight="true"
      :overlay="true"
      :right="true"
      :open.sync="showLedger"
    >
      <div class="my-4 px-4">
        <p
          v-if="employee_adv_deets != null"
          class="has-text-weight-medium is-size-5"
        >
          Advance Ledger for {{ this.employee_adv_deets.name }}
        </p>
        <hr class="my-2" />
        <p>
          <span class="has-text-weight-semibold has-text-grey">Balance</span>
          <span class="is-pulled-right">
            {{ formatedNumber(getTotalCredit() - getTotalDebit()) }}
          </span>
        </p>
        <br />
        <b-table :data="advance_list" :empty="advance_list.length == 0">
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
            <span v-if="props.row.trans == 'debit'" class="is-pulled-right">
              {{ formatedNumberNoCurr(props.row.advanceamt) }}
            </span>
          </b-table-column>
          <b-table-column centered label="Credit" v-slot="props">
            <span v-if="props.row.trans == 'credit'" class="is-pulled-right">
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
            <td class="has-text-right">{{ formatedNumberNoCurr(getTotalDebit()) }}</td>
            <td class="has-text-right">{{ formatedNumberNoCurr(getTotalCredit()) }}</td>
          </template>
        </b-table>
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
          <div class="level is-mobile my-0">
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
            class="notification is-info has-text-white"
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
            <!-- <p>No further changes will be saved. You can <b>Print</b>  this sheet or <b>select empolyees</b>  for whom you want the slips.</p> -->
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
                }}
                <br>
                <button @click="viewRemarks(props.index)" class="button tag heading is-rounded is-info">
                  <b-icon icon="plus" size="is-small" class=" mr-2"></b-icon>
                  Add Remarks</button>
                  <p class="is-size-7 has-text-grey" v-for="row in props.row.remarks.split('\n')">{{row}}</p>
                
                </b-table-column>
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
                      :key="index+'_ded_mnth'"
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
                }}
                <hr class="my-1">
                <b-numberinput
                      :controls="false"
                      v-model.number="props.row.paidamt"
                      controls-rounded
                    ></b-numberinput>
                <p class="heading mt-2">PENDING</p>
                <p>{{ formatedNumber(props.row.net_payable - props.row.paidamt)}}
                </p>
                  <span v-if="props.row.net_payable - props.row.paidamt<0">
                    <button @click="giveAdvance(props.row.employee[0].id, Math.abs(props.row.net_payable - props.row.paidamt))" class="mt-1 button tag heading is-black is-rounded">
                      <b-icon size="is-small" class="mr-1" icon="plus"></b-icon>
                      <span>
                      Advance
                      </span>
                      </button>
                  </span>
                </b-table-column>
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
      <b-modal v-model="showAdvModal">
      <div v-if="employee_adv_deets != null" class="box pt-0 px-0">
        <div
          class="box has-background-link has-text-white"
          v-if="
            employee_adv_deets != null && employee_adv_deets.advance == 'not'
          "
        >
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <div class="media">
                  <div class="media-left">
                    <b-icon icon="information" class="has-text-white"></b-icon>
                  </div>
                  <div class="media-content">
                    <p>
                      This employee has not been allowed advance. <br />
                      If you'd like to change that , please edit employee's
                      details.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <button class="button">Edit</button>
              </div>
            </div>
          </div>
        </div>
        <div
          v-if="
            advance_list.length >= employee_adv_deets.advancenum &&
            employee_adv_deets.advance != 'not'
          "
          class="notification has-background-warning has-text-black"
        >
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <div class="media">
                  <div class="media-left">
                    <b-icon icon="alert-circle" class="has-text-black"></b-icon>
                  </div>
                  <div class="media-content">
                    <p class="has-text-weight-medium">
                      Employee has reached the allowed advance limit. <br />
                      If you'd like to increase advance limit , please edit
                      Employee details.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <button class="button">Edit</button>
              </div>
            </div>
          </div>
        </div>
        <div :class="{ 'is-hidden': advSuccess }"
          class=" success-bg notification has-text-centered has-background-link-light"
        >
          <b-icon
            size="is-large"
            class="has-text-link"
            icon="check-decagram"
          ></b-icon>

          <p class="is-size-5 mt-4 has-text-link-dark">
            Advance given to {{titleCase(employee_adv_deets.name)}}

          </p>
          <p class="is-size-5 has-text-weight-bold has-text-link-dark">
{{formatedNumber(advSuccessAmt)}}
          </p>
        </div>
  <div>
        <div class="px-4 mt-3">
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <p class="is-size-5 mt-4 has-text-weight-semibold">
                  New Advance
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

                <button @click="showLedger = !showLedger" class="button is-link is-light">
                  <span >
                    <!-- TODO: Triggers Side bar for Advances List -->
                    Show Ledger
                  </span>
                </button>
                <button @click="showSide = !showSide" class="button is-link">
                  <b-icon icon="table-eye"></b-icon>
                  <span class="ml-2">
                    <!-- TODO: Triggers Side bar for Advances List -->
                    View Advances
                  </span>
                </button>
                </div>
              </div>
            </div>
          </div>

          <table
            class="table is-fullwidth is-boxed"
            v-if="employee_adv_deets != null"
          >
            <tr>
              <td>
                <b-field>
                  <template #label>
                    <span class="heading">BASIC PAY</span>
                  </template>
                  <p class="has-text-black has-text-weight-semibold">
                    {{
                      Number(employee_adv_deets.basicpay).toLocaleString(
                        "en-IN"
                      )
                    }}
                  </p>
                </b-field>
              </td>
              <td>
                <b-field>
                  <template #label>
                    <span class="heading">ADVANCE</span>
                  </template>
                  <p class="has-text-black">
                    {{ titleCase(employee_adv_deets.advance) }}
                  </p>
                </b-field>
              </td>
              <td>
                <b-field>
                  <template #label>
                    <span class="heading">NO. OF ADVANCE</span>
                  </template>
                  <p class="has-text-black">
                    <span class="has-text-weight-semibold has-text-black">{{
                      advance_list.filter((item) => item.trans == "credit")
                        .length
                    }}</span>
                    / {{ employee_adv_deets.advancenum }}
                  </p>
                </b-field>
              </td>
              <td>
                <b-field>
                  <template #label>
                    <span class="heading">Total Allowed</span>
                  </template>
                  <p
                    class="has-text-black"
                    v-if="employee_adv_deets.advancevalue != null"
                  >
                    {{
                      employee_adv_deets.advancevalue.toLocaleString("en-IN")
                    }}
                  </p>
                  <p v-else class="has-text-grey">None</p>
                </b-field>
              </td>
              <td>
                <b-field>
                  <template #label>
                    <span class="heading">OUTSTANDING</span>
                  </template>
                  <p class="has-text-black has-text-weight-semibold">
                    {{ getOutstandingAdvance() }}
                  </p>
                </b-field>
              </td>
            </tr>
          </table>
          <b-field grouped group-multiline>
            <div class="control">
              <b-field label="Date">
                <b-datepicker
                  :disabled="set_disabled"
                  v-model="form.date"
                  :dob-formatter="dobFormatter"
                >
                </b-datepicker>
              </b-field>
            </div>
            <div class="control">
              <b-field label="Amount">
                <b-input
                  :disabled="set_disabled"
                  v-model="form.advanceamt"
                  placeholder="Enter Amount"
                ></b-input>
              </b-field>
            </div>
          </b-field>
          <p class="mt-4 has-text-grey has-text-weight-medium is-size-5">
            Security
          </p>
          <hr class="my-2" />
          <b-field grouped group-multiline>
            <div class="control">
              <b-field label="Cheque No.">
                <b-input
                  :disabled="set_disabled"
                  v-model="form.cheque_no"
                  placeholder="Enter Amount"
                ></b-input>
              </b-field>
            </div>
            <div class="control">
              <b-field label="Letter">
                <b-radio
                  :disabled="set_disabled"
                  v-model="form.letter"
                  native-value="yes"
                  >Yes</b-radio
                >
                <b-radio
                  :disabled="set_disabled"
                  v-model="form.letter"
                  native-value="no"
                  >No</b-radio
                >
              </b-field>
            </div>
          </b-field>
          <b-field grouped group-multiline>
            <div class="control">
              <b-field label="Deduction Amount">
                <b-input
                  :disabled="set_disabled"
                  v-model="form.deduction"
                  placeholder="Enter Amount"
                ></b-input>
              </b-field>
            </div>
            <div class="control">
              <b-field label="Period">
                <b-radio
                  :disabled="set_disabled"
                  v-model="form.deduction_period"
                  native-value="month"
                  >Month</b-radio
                >
                <b-radio
                  :disabled="set_disabled"
                  v-model="form.deduction_period"
                  native-value="year"
                  >Year</b-radio
                >
              </b-field>
            </div>
          </b-field>
          <button
            :disabled="set_disabled"
            @click="submitData"
            class="button is-black"
          >
            <b-icon icon="check"></b-icon>
            <span class="ml-3">Save</span>
          </button>
  </div>
          <button @click="showAdvModal = !showAdvModal" :class="{ 'is-hidden': advSuccess }" class="button is-link is-fullwidth ">
            <b-icon icon="check"></b-icon>
            <span class="ml-3">Done</span>
          </button>
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
      calc: {
        period: null,
        pay: null,
        time: null,
        final: null,
      },
       showSide: false,
      showLedger: false,
      form: {
        date: null,
        advanceamt: null,
        cheque_no: null,
        letter: null,
        deduction: null,
        deduction_period: null,
        errors: {},
      },
       advance_list: [],
             employee_adv_deets: null,

      advSuccess: true,
      set_disabled: false,
      advSuccessAmt: null,
       showAdvModal: false,
      showAdvLedger: false,
      remarks_id: null,
      showCalc: false,
      showRemarks: false,
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
      return tota;
    },
      submitData(e) {
      let self = this;
      if (this.checkData()) {
        console.log(this.form.errors.length);
        if (Object.keys(this.form.errors).length == 0) {
          this.submitting = true;
          this.value = "Saving";

          let formdata = {
            emp_id: this.employee_adv_deets.id,
            adv_total: this.employee_adv_deets.adv_total,
            data: this.form,
            // company_id: this.company,
            month: this.month,
          };
          console.log(formdata);
          this.$axios
            .post("/transaction/advance/save", formdata)
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

                this.advSuccessAmt = Object.freeze(this.form.advanceamt)
                this.form.advanceamt = 0;
                this.form.date = null;
                this.form.deduction = null;
                this.form.deduction_period = null;
                this.form.cheque_no = null;
                this.form.letter = null;
                this.advSuccess = true
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
              this.value = "Save";
            })
            .catch(function (error) {
              // RUn error
              console.error(error);
            });
          this.submitting = false;
          this.value = "Save";
        }
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
      giveAdvance(emp_id , pending) {
      this.$axios
        .get("/transaction/advance/employee/" + emp_id)
        .then((response) => {
          this.employee_adv_deets = response.data;
          this.form.advanceamt = pending
          this.form.date = this.month
          this.showAdvModal = !this.showAdvModal;
          this.$axios
            .get("/transaction/advance/get/" + emp_id)
            .then((response) => {
              this.advance_list = response.data;
              if (
                this.advance_list.length >= this.employee_adv_deets.advancenum
              ) {
                this.set_disabled = true;
              } else {
                this.set_disabled = false;
              }
            });
        });
    },
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
      localStorage.setItem("selecteddata", null);
      localStorage.setItem("selecteddata", JSON.stringify(formdata));
      window.open("/print/salary-sheet-selected", "_blank", [], true);
    },
    viewRemarks(data){
      this.showRemarks = !this.showRemarks
      this.remarks_id = data
    },
    resetRemark(){
      this.showRemarks = !this.showRemarks
      this.remarks_id = null

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