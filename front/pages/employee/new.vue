<template>
  <div class="has-background-white" style="border-top: 1px solid #eee">
    <div
      class="section py-4 pt-5 is-fullwidth is-fullheight"
      :class="{ 'container px-0': $store.state.win }"
    >
      <div class="columns">
        <div class="column">
          <div class="level">
            <div class="level-left">
              <p class="is-size-4 has-text-weight-semibold">Employee</p>
            </div>
            <div class="level-right">
              <p class="is-size-6 tag is-link is-light has-text-weight-medium">
                <span class="has-text-weight-semibold mr-2">*</span> Fields are
                required
              </p>
            </div>
          </div>
          <div id="emp_entry">
            <form v-on:submit="submitData" method="POST" novalidate="True">
              <!-- name -->
              <div class="field is-grouped">
                <div class="control">
                  <label for="" class="label">Upload Photo</label>
                  <div
                    class="file has-name is-fullwidth"
                    v-bind:class="formdata.errors.photo ? 'is-danger' : ''"
                  >
                    <label class="file-label">
                      <input
                        class="file-input"
                        type="file"
                        ref="photofile"
                        v-on:change="handleFileUpload('photo')"
                      />
                      <span class="file-cta">
                        <span class="file-icon">
                          <b-icon icon="upload"></b-icon>
                        </span>
                        <span class="file-label"> Choose a file… </span>
                      </span>
                      <span class="file-name">
                        <p
                          v-if="formfiles.photofile"
                          v-html="formfiles.photofile.name"
                        ></p>
                        <p v-if="formfiles.photofile == null">Emp. Photo</p>
                      </span>
                    </label>
                  </div>
                  <small
                    class="has-text-danger is-underline"
                    v-if="formdata.errors.photo"
                    >{{ formdata.errors.photo.error }}</small
                  >
                </div>
                <div class="control is-expanded">
                  <b-field
                    label="Name*"
                    :type="{ 'is-danger': formdata.errors.name }"
                  >
                    <b-input
                      placeholder="Enter Employee Name"
                      v-model="formdata.name"
                    >
                    </b-input>
                  </b-field>
                </div>
              </div>

              <!-- DOB -->
              <b-field grouped>
                <b-field
                  label="Date of Birth*"
                  :type="{ 'is-danger': formdata.errors.dob }"
                >
                  <b-datepicker
                    icon="calendar"
                    placeholder="Select Date"
                    :date-formatter="dobFormatter"
                    v-model="formdata.dob"
                  ></b-datepicker>
                </b-field>
              </b-field>

              <!-- Spouse and Father -->
              <div class="field is-grouped is-fullwidth">
                <div class="control is-expanded">
                  <b-field
                    label="Spouse Name"
                    :type="{ 'is-danger': formdata.errors.spousename }"
                  >
                    <b-input
                      placeholder="Enter Spouse Name"
                      v-model="formdata.spousename"
                    >
                    </b-input>
                  </b-field>
                </div>

                <div class="control is-expanded">
                  <b-field
                    label="Father Name*"
                    :type="{ 'is-danger': formdata.errors.fathername }"
                  >
                    <b-input
                      placeholder="Enter Father Name"
                      v-model="formdata.fathername"
                    >
                    </b-input>
                  </b-field>
                </div>
              </div>

              <!-- Education -->
              <b-field grouped group-multiline>
                <div class="control is-expanded">
                  <b-field expanded label="Education">
                    <b-input
                      placeholder="Enter Education"
                      v-model="formdata.education"
                    ></b-input>
                  </b-field>
                </div>
                <div class="control is-expanded">
                  <b-field expanded label="Contact No.">
                    <b-input
                      placeholder="Enter Contact No."
                      v-model="formdata.contact"
                    ></b-input>
                  </b-field>
                </div>
              </b-field>

              <!-- Current Address -->
              <b-field grouped group-multiline>
                <div class="control is-expanded">
                  <b-field expanded label="Current Address">
                    <b-input
                      placeholder="Enter Address"
                      v-model="formdata.curr_address"
                    ></b-input>
                  </b-field>
                </div>
                <div class="control is-expanded">
                  <b-field expanded label="Current City.">
                    <b-select
                      expanded
                      v-model="formdata.curr_city"
                      placeholder="Select City"
                    >
                      <option disabled>Select City</option>
                      <option
                        :value="item.id"
                        v-for="(item, index) in data_city"
                        :key="'curr_' + index"
                      >
                        {{ item.name }}
                      </option>
                    </b-select>
                  </b-field>
                </div>
              </b-field>

              <!-- Permanent City -->
              <div class="box has-background-light">
                <div class="field">
                  <div class="control">
                    <button class="button is-link" @click="sameAddress">
                      <b-icon icon="content-duplicate"></b-icon>
                      <span class="ml-2"> Same as Current </span>
                    </button>
                  </div>
                </div>
                <b-field grouped group-multiline>
                  <div class="control is-expanded">
                    <b-field expanded label="Permanent Address">
                      <b-input
                        placeholder="Enter Address"
                        v-model="formdata.perm_address"
                      ></b-input>
                    </b-field>
                  </div>
                  <div class="control is-expanded">
                    <b-field expanded label="Permanent City.">
                      <b-select
                        expanded
                        v-model="formdata.perm_city"
                        placeholder="Select City"
                      >
                        <option value="" disabled>Select City</option>
                        <option
                          :value="item.id"
                          v-for="(item, index) in data_city"
                          :key="'perm_' + index"
                        >
                          {{ item.name }}
                        </option>
                      </b-select>
                    </b-field>
                  </div>
                </b-field>
              </div>

              <!-- PAN Details -->
              <div class="field is-grouped is-fullwidth">
                <div class="control is-expanded">
                  <label for="" class="label">PAN No.</label>
                  <input
                    type="text"
                    class="input is-fullwidth"
                    v-model="formdata.pan"
                    placeholder="Enter PAN No."
                  />
                </div>

                <div class="control is-expanded">
                  <label for="" class="label">Upload file</label>
                  <div
                    class="file has-name is-fullwidth"
                    v-bind:class="formdata.errors.pan ? 'is-danger' : ''"
                  >
                    <label class="file-label">
                      <input
                        class="file-input"
                        type="file"
                        ref="panfile"
                        v-on:change="handleFileUpload('pan')"
                      />
                      <span class="file-cta">
                        <span class="file-icon">
                          <b-icon icon="upload"></b-icon>
                        </span>
                        <span class="file-label"> Choose a file… </span>
                      </span>
                      <span class="file-name">
                        <p
                          v-if="formfiles.panfile"
                          v-html="formfiles.panfile.name"
                        ></p>
                        <p v-if="formfiles.panfile == null">PAN Card Copy</p>
                      </span>
                    </label>
                  </div>
                  <small
                    class="has-text-danger is-underline"
                    v-if="formdata.errors.pan"
                    >{{ formdata.errors.pan.error }}</small
                  >
                </div>
              </div>

              <!-- AADHAR -->
              <div class="field is-grouped is-fullwidth">
                <div class="control is-expanded">
                  <label for="" class="label">Aadhar No.</label>
                  <input
                    type="text"
                    class="input is-fullwidth"
                    v-model="formdata.aadhar"
                    placeholder="Enter Aadhar No."
                  />
                </div>

                <div class="control is-expanded">
                  <label for="" class="label">Upload file</label>
                  <div
                    class="file has-name is-fullwidth"
                    v-bind:class="formdata.errors.aadhar ? 'is-danger' : ''"
                  >
                    <label class="file-label">
                      <input
                        class="file-input"
                        type="file"
                        ref="aadharfile"
                        v-on:change="handleFileUpload('aadhar')"
                      />
                      <span class="file-cta">
                        <span class="file-icon">
                          <b-icon icon="upload"></b-icon>
                        </span>
                        <span class="file-label"> Choose a file… </span>
                      </span>
                      <span class="file-name">
                        <p
                          v-if="formfiles.aadharfile"
                          v-html="formfiles.aadharfile.name"
                        ></p>
                        <p v-if="formfiles.aadharfile == null">
                          Aadhar Card Copy
                        </p>
                      </span>
                    </label>
                  </div>
                  <small
                    class="has-text-danger is-underline"
                    v-if="formdata.errors.aadhar"
                    >{{ formdata.errors.aadhar.error }}</small
                  >
                </div>
              </div>

              <!-- Extra Uploads - id , edu. cert -->
              <div class="field is-grouped is-fullwidth">
                <div class="control is-expanded">
                  <label for="" class="label">Upload Extra I.D</label>
                  <div
                    class="file has-name is-fullwidth"
                    v-bind:class="
                      formdata.errors.extraidfile ? 'is-danger' : ''
                    "
                  >
                    <label class="file-label">
                      <input
                        class="file-input"
                        type="file"
                        ref="extraidfile"
                        v-on:change="handleFileUpload('extraidfile')"
                      />
                      <span class="file-cta">
                        <span class="file-icon">
                          <b-icon icon="upload"></b-icon>
                        </span>
                        <span class="file-label"> Choose a file… </span>
                      </span>
                      <span class="file-name">
                        <p
                          v-if="formfiles.extraidfile"
                          v-html="formfiles.extraidfile.name"
                        ></p>
                        <p v-if="formfiles.extraidfile == null">
                          Extra ID Copy
                        </p>
                      </span>
                    </label>
                  </div>
                  <small
                    class="has-text-danger is-underline"
                    v-if="formdata.errors.extraidfile"
                    >{{ formdata.errors.extraidfile.error }}</small
                  >
                </div>

                <div class="control is-expanded">
                  <label for="" class="label">Upload Education Cert.</label>
                  <div
                    class="file has-name is-fullwidth"
                    v-bind:class="
                      formdata.errors.educertfile ? 'is-danger' : ''
                    "
                  >
                    <label class="file-label">
                      <input
                        class="file-input"
                        type="file"
                        ref="educertfile"
                        v-on:change="handleFileUpload('educertfile')"
                      />
                      <span class="file-cta">
                        <span class="file-icon">
                          <b-icon icon="upload"></b-icon>
                        </span>
                        <span class="file-label"> Choose a file… </span>
                      </span>
                      <span class="file-name">
                        <p
                          v-if="formfiles.educertfile"
                          v-html="formfiles.educertfile.name"
                        ></p>
                        <p v-if="formfiles.educertfile == null">
                          Edu. Cert. Copy
                        </p>
                      </span>
                    </label>
                  </div>
                  <small
                    class="has-text-danger is-underline"
                    v-if="formdata.errors.educertfile"
                    >{{ formdata.errors.educertfile.error }}</small
                  >
                </div>
              </div>

              <!-- Ref -->
              <div class="field is-grouped is-fullwidth">
                <div class="control is-expanded">
                  <label for="" class="label">Reference</label>
                  <input
                    type="text"
                    class="input is-fullwidth"
                    v-model="formdata.reference"
                    placeholder="Enter Reference"
                  />
                </div>

                <div class="control is-expanded">
                  <label for="" class="label">Upload Resume</label>
                  <div
                    class="file has-name is-fullwidth"
                    v-bind:class="formdata.errors.resumefile ? 'is-danger' : ''"
                  >
                    <label class="file-label">
                      <input
                        class="file-input"
                        type="file"
                        ref="resumefile"
                        v-on:change="handleFileUpload('resumefile')"
                      />
                      <span class="file-cta">
                        <span class="file-icon">
                          <b-icon icon="upload"></b-icon>
                        </span>
                        <span class="file-label"> Choose a file… </span>
                      </span>
                      <span class="file-name">
                        <p
                          v-if="formfiles.resumefile"
                          v-html="formfiles.resumefile.name"
                        ></p>
                        <p v-if="formfiles.resumefile == null">Resume Copy</p>
                      </span>
                    </label>
                  </div>
                  <small
                    class="has-text-danger is-underline"
                    v-if="formdata.errors.resumefile"
                    >{{ formdata.errors.resumefile.error }}</small
                  >
                </div>
              </div>

              <hr />
              <!-- COmpnay INfo -->
              <div class="box has-background-light">
                <b-field grouped>
                  <b-field label="Date of Appointment ">
                    <b-datepicker
                      icon="calendar"
                      placeholder="Select Date"
                      :date-formatter="dobFormatter"
                      v-model="formdata.dateofapp"
                    ></b-datepicker>
                  </b-field>
                </b-field>
                <b-field grouped group-multiline>
                  <div class="control">
                    <b-field label="Appointment">
                      <b-select
                        expanded
                        placeholder="Select Appointment"
                        v-model="formdata.appointment"
                      >
                        <option disabled>Select Appointment</option>
                        <option
                          :value="item.id"
                          v-for="(item, index) in data_appt"
                          :key="'appt_' + index"
                        >
                          {{ item.name }}
                        </option>
                      </b-select>
                    </b-field>
                  </div>
                  <div class="control">
                    <b-field expanded label="Post">
                      <b-select
                        expanded
                        placeholder="Select Post"
                        v-model="formdata.post"
                      >
                        <option disabled>Select Post</option>
                        <option
                          :value="item.id"
                          v-for="(item, index) in data_post"
                          :key="'post_' + index"
                        >
                          {{ item.name }}
                        </option>
                      </b-select>
                    </b-field>
                  </div>
                  <div class="control">
                    <b-field label="Department">
                      <b-select
                        expanded
                        placeholder="Select Department"
                        v-model="formdata.department"
                      >
                        <option disabled>Select Dept.</option>
                        <option
                          :value="item.id"
                          v-for="(item, index) in data_dept"
                          :key="'dept_' + index"
                        >
                          {{ item.name }}
                        </option>
                      </b-select>
                    </b-field>
                  </div>
                  <div class="control">
                    <b-field label="Company">
                      <b-select
                        expanded
                        placeholder="Select Comapny"
                        v-model="formdata.company"
                      >
                        <option disabled>Select Company</option>
                        <option
                          :value="item.id"
                          v-for="(item, index) in data_company"
                          :key="'comp_' + index"
                        >
                          {{ item.name }}
                        </option>
                      </b-select>
                    </b-field>
                  </div>
                </b-field>

                <div class="field is-grouped is-fullwidth">
                  <div class="control is-expanded">
                    <label class="label">Enter Benefits</label>
                    <b-taginput
                      v-model="formdata.benefits"
                      :data="filteredBenefits"
                      field="name"
                      size="is-normal"
                      autocomplete
                      type="is-black"
                      placeholder="Add a benefit"
                      @typing="getFilteredTags"
                    >
                      <template slot-scope="props">
                        {{ props.option.name }}
                      </template>
                      <template slot="empty"> There are no items </template>
                    </b-taginput>
                  </div>
                </div>
                <hr class="has-background-grey-light" style="height: 1px" />
                <p for="" class="is-size-5">Salary Structure</p>
                <br />
                <label for="" class="label"
                  >Effective Date
                  <br />
                  <p class="has-text-weight-normal">
                    When changing/updating salary , update the date.
                  </p>
                </label>

                <b-field grouped>
                  <b-field>
                    <b-datepicker
                      icon="calendar"
                      placeholder="Select Date"
                      :date-formatter="dobFormatter"
                      v-model="formdata.dateeff"
                    ></b-datepicker>
                  </b-field>
                </b-field>
                <div class="field is-grouped box is-white">
                  <div class="control">
                    <label class="label">Select payment model: </label>
                  </div>
                  <div class="control">
                    <b-radio
                      v-model="formdata.salary_structure"
                      name="month"
                      native-value="month"
                    >
                      Month
                    </b-radio>
                    <b-radio
                      v-model="formdata.salary_structure"
                      name="year"
                      native-value="year"
                    >
                      Year
                    </b-radio>
                  </div>
                </div>

                <div class="field is-grouped is-fullwidth">
                  <div class="control">
                    <b-field
                      label="Basic Pay*"
                      :type="{ 'is-danger': formdata.errors.basicpay }"
                    >
                      <b-input
                        placeholder="Enter Basic Pay"
                        v-model="formdata.basicpay"
                      ></b-input>
                    </b-field>
                  </div>

                  <div class="control">
                    <b-field label="P.F">
                      <b-select placeholder="Select P.F" v-model="formdata.pf">
                        <option value="yes">Yes</option>
                        <option value="no">No</option>
                      </b-select>
                    </b-field>
                  </div>
                  <div class="control">
                    <b-field label="ESI">
                      <b-select placeholder="Select ESI" v-model="formdata.esi">
                        <option value="yes">Yes</option>
                        <option value="no">No</option>
                      </b-select>
                    </b-field>
                  </div>
                </div>
                <br />
                <div class="field is-grouped is-fullwidth">
                  <div class="control is-expanded">
                    <label for="" class="label">Bank Name</label>
                    <input
                      type="text"
                      class="input is-fullwidth"
                      v-model="formdata.bankname"
                      placeholder="Enter Bank Name"
                    />
                  </div>
                  <div class="control is-expanded">
                    <label for="" class="label">Account Number</label>
                    <input
                      type="text"
                      class="input is-fullwidth"
                      v-model="formdata.accnumber"
                      placeholder="Enter Account Number"
                    />
                  </div>
                  <div class="control is-expanded">
                    <label for="" class="label">IFSC Code</label>
                    <input
                      type="text"
                      class="input is-fullwidth"
                      v-model="formdata.ifsccode"
                      placeholder="Enter IFSC Code"
                    />
                  </div>
                </div>
                <br />
                <div class="box is-white">
                  <div class="field is-grouped">
                    <div class="control">
                      <label class="label">Salary Advance </label>
                    </div>
                    <div class="control">
                      <label class="radio">
                        <input
                          type="radio"
                          value="allowed"
                          v-model="formdata.advance"
                        />
                        Allowed
                      </label>
                      <label class="radio">
                        <input
                          type="radio"
                          value="not"
                          v-model="formdata.advance"
                        />
                        Not Allowed
                      </label>
                    </div>
                  </div>
                  <div class="field is-grouped is-multiline">
                    <div class="control">
                      <label for="" class="label">Max. Advance</label>
                      <input
                        type="text"
                        v-model="formdata.advancevalue"
                        placeholder="Enter Max. advance"
                        class="input"
                        :disabled="formdata.advance == 'not' ? true : false"
                      />
                    </div>
                    <div class="control">
                      <label for="" class="label">Number of Advances </label>
                      <input
                        type="text"
                        v-model="formdata.advancenum"
                        placeholder="Enter Advances Allowed"
                        class="input"
                        :disabled="formdata.advance == 'not' ? true : false"
                      />
                    </div>
                  </div>
                </div>

                <div class="field">
                  <div class="control">
                    <label for="" class="label"
                      >Paid Leaves ( in a year )</label
                    >
                    <input
                      type="text"
                      class="input"
                      v-model="formdata.paidleave"
                      placeholder="Enter Paid Leaves"
                    />
                  </div>
                </div>

                <div class="field">
                  <div class="control">
                    <label for="" class="label"
                      >Increment Period ( in months )</label
                    >
                    <input
                      type="text"
                      class="input"
                      v-model="formdata.incrementpr"
                      placeholder="Enter period"
                    />
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="buttons">
                <button class="button is-black">
                  <b-icon icon="check"></b-icon>
                  <span class="ml-2">Save</span>
                </button>
                <button class="button">
                  <b-icon icon="close"></b-icon>
                  <span class="ml-2"> Clear </span>
                </button>
              </div>
            </form>
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
      filteredBenefits: null,
      benefitsList: null,
      submitting: false,
      value: "Save",
      data_city: [],
      data_location: [],
      data_company: [],
      data_appt: [],
      data_post: [],
      data_dept: [],
      data_benefits: [],
      formdata: {
        name: null,
        dob: null,
        spousename: null,
        fathername: null,
        education: null,
        contact: null,
        curr_address: null,
        curr_city: null,
        perm_address: null,
        perm_city: null,
        pan: null,

        aadhar: null,
        reference: null,
        dateofapp: null,
        appointment: null,
        post: null,
        department: null,
        company: null,
        benefits: [],
        dateeff: null,
        salary_structure: "month",
        basicpay: null,
        pf: null,
        esi: null,
        bankname: null,
        accnumber: null,
        ifsccode: null,
        advance: "allowed",

        advancevalue: null,
        advancenum: null,
        paidleave: null,
        incrementpr: null,
        errors: {},
      },
      formfiles: {
        panfile: null,
        aadharfile: null,
        photofile: null,
        extraidfile: null,
        educertfile: null,
        resumefile: null,
      },
      confirmExit: false,
    };
  },
  created() {
    let data = this;
    this.$axios.get("/master/get/benefits").then(function (response) {
      data.filteredBenefits = response.data;
      data.benefitsList = response.data;
      console.log(response.data);
    });
    // if (confirmExit) {
    //   window.onbeforeunload = confirmExit;
    //   function confirmExit() {
    //     this.confirmExit;
    //     return "You have attempted to leave this page.  If you have made any changes to the fields without clicking the Save button, your changes will be lost.  Are you sure you want to exit this page?";
    //   }
    // }
  },
  mounted() {
    this.$axios.get("/master/get/city").then((response) => {
      this.data_city = response.data;
    });
    this.$axios.get("/master/get/location").then((response) => {
      this.data_location = response.data;
    });
    this.$axios.get("/master/get/company").then((response) => {
      this.data_company = response.data;
    });
    this.$axios.get("/master/get/department").then((response) => {
      this.data_dept = response.data;
    });
    this.$axios.get("/master/get/appointment").then((response) => {
      this.data_appt = response.data;
    });
    this.$axios.get("/master/get/post").then((response) => {
      this.data_post = response.data;
    });
    this.$axios.get("/master/get/benefits").then((response) => {
      this.data_benefits = response.data;
    });
  },
  methods: {
    clearData() {
      this.formdata.name = null;
      this.formdata.dob = null;
      this.formdata.spousename = null;
      this.formdata.fathername = null;
      this.formdata.education = null;
      this.formdata.contact = null;
      this.formdata.curr_address = null;
      this.formdata.curr_city = null;
      this.formdata.perm_address = null;
      this.formdata.perm_city = null;
      this.formdata.pan = null;

      this.formdata.aadhar = null;
      this.formdata.reference = null;
      this.formdata.dateofapp = null;
      this.formdata.appointment = null;
      this.formdata.post = null;
      this.formdata.department = null;
      this.formdata.company = null;
      this.formdata.benefits = [];
      this.formdata.dateeff = null;
      this.formdata.salary_structure = null;
      this.formdata.basicpay = null;
      this.formdata.pf = null;
      this.formdata.esi = null;
      this.formdata.advance = "allowed";

      this.formdata.advancevalue = null;
      this.formdata.advancenum = null;
      this.formdata.paidleave = null;
      this.formdata.incrementpr = null;
      this.formdata.errors = {};
      this.formfiles.panfile = null;
      this.formfiles.aadharfile = null;
      this.formfiles.photofile = null;
      this.formfiles.extraidfile = null;
      this.formfiles.educertfile = null;
      this.formfiles.resumefile = null;
    },
    submitData(e) {
      if (this.checkData(e)) {
        let formData = new FormData();

        this.submitting = true;
        this.value = "Saving";

        let self = this;
        formData.append("data", JSON.stringify(self.formdata));

        if (this.formfiles.panfile) {
          formData.append(
            "panfile",
            this.formfiles.panfile,
            this.formfiles.panfile.name
          );
        }
        if (this.formfiles.photofile) {
          formData.append(
            "photofile",
            this.formfiles.photofile,
            this.formfiles.photofile.name
          );
        }
        if (this.formfiles.aadharfile) {
          formData.append(
            "aadharfile",
            this.formfiles.aadharfile,
            this.formfiles.aadharfile.name
          );
        }
        if (this.formfiles.extraidfile) {
          formData.append(
            "extraidfile",
            this.formfiles.extraidfile,
            this.formfiles.extraidfile.name
          );
        }
        if (this.formfiles.educertfile) {
          formData.append(
            "educertfile",
            this.formfiles.educertfile,
            this.formfiles.educertfile.name
          );
        }
        if (this.formfiles.resumefile) {
          formData.append(
            "resumefile",
            this.formfiles.resumefile,
            this.formfiles.resumefile.name
          );
        }
        this.$axios
          .post("/employee/new/add", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then(function (response) {
            if (response.data.success) {
              self.clearData();
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
              self.confirmExit = true;
            }
            if (response.data.message) {
              self.$buefy.snackbar.open({
                indefinate: true,
                message: response.data.message,
                type: "is-warning",
                position: "is-top-right",
                actionText: "Close",
                queue: true,
                onAction: () => {
                  this.isActive = false;
                },
              });
            }

            self.submitting = false;
            self.value = "Save";
          })

          .catch(function (error) {
            duration: 4000,
            self.$buefy.snackbar.open({
              message: "Something went wrong . Please check logs.",
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

        e.preventDefault();
      } else {
        this.$buefy.snackbar.open({
          duration: 4000,
          message: "Please enter the required data , then submit.",
          type: "is-light",
          position: "is-top-right",
          actionText: "Close",
          queue: true,
          onAction: () => {
            this.isActive = false;
          },
        });
      }
    },
    getFilteredTags(text) {
      this.filteredBenefits = this.benefitsList.filter((option) => {
        return (
          option.name.toString().toLowerCase().indexOf(text.toLowerCase()) >= 0
        );
      });
    },
    checkData(e) {
      this.formdata.errors = {};
      if (
        this.formdata.name &&
        this.formdata.dob &&
        this.formdata.fathername &&
        this.formdata.basicpay
      ) {
        return true;
      }
      if (!this.formdata.name) {
        this.$set(this.formdata.errors, "name", "Data required");
      }
      if (!this.formdata.dob) {
        this.$set(this.formdata.errors, "dob", "Data required");
      }
      if (!this.formdata.fathername) {
        this.$set(this.formdata.errors, "fathername", "Data required");
      }
      if (!this.formdata.basicpay) {
        this.$set(this.formdata.errors, "basicpay", "Data required");
      }
      e.preventDefault();
    },
    sameAddress(e) {
      if (this.formdata.curr_address) {
        this.formdata.perm_address = this.formdata.curr_address;
        this.formdata.perm_city = this.formdata.curr_city;
      } else {
        this.$set(
          this.formdata.errors,
          "perm_address",
          "Values not set for Current Address."
        );
      }

      e.preventDefault();
    },
    handleFileUpload(field) {
      if (field == "pan") {
        this.formfiles.panfile = this.$refs.panfile.files[0];

        // this.fileUploadType(this.formfiles.panfile.name, field);
      }
      if (field == "aadhar") {
        this.formfiles.aadharfile = this.$refs.aadharfile.files[0];
        // this.fileUploadType(this.formfiles.aadharfile.name, field);
      }
      if (field == "photo") {
        this.formfiles.photofile = this.$refs.photofile.files[0];
        // this.fileUploadType(this.formfiles.photofile.name, field);
      }
      if (field == "extraidfile") {
        this.formfiles.extraidfile = this.$refs.extraidfile.files[0];
        // this.fileUploadType(this.formfiles.extraidfile.name, field);
      }
      if (field == "educertfile") {
        this.formfiles.educertfile = this.$refs.educertfile.files[0];
        // this.fileUploadType(this.formfiles.educertfile.name, field);
      }
      if (field == "resumefile") {
        this.formfiles.resumefile = this.$refs.resumefile.files[0];
        // this.fileUploadType(this.formfiles.resumefile.name, field);
      }
    },
    fileUploadType(type, field) {
      let allowedTypes = ["pdf", "jpg", "peg", "png"];
      type = type.split(".")[type.length - 1];
      if (allowedTypes.includes(type.toLowerCase())) {
        this.$set(this.formdata.errors, field, null);
        return true;
      } else {
        this.$set(this.formdata.errors, field, {
          error: "Please upload pdf,jpg ,jpeg or png file",
        });

        return false;
      }
    },
  },
};
</script>

<style>
</style>