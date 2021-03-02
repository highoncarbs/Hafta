<template>
  <div>
       <div class="has-background-white" style="border-top: 1px solid #eee">
    <div
      class="section py-4 pt-5 is-fullwidth is-fullheight"
      :class="{ 'container px-0': $store.state.win }"
    >
    <!-- Edit Modal -->
    <div class="modal animated is-active fadeIn" v-show="modal">
      <div class="modal-background" @click="modal = !modal"></div>
      <div class="modal-content">
        <div class="box">
          <div v-if="edit.mssg" class="notification animated fadeIn"></div>
          <form id="data_entry" novalidate="true" @submit="saveEditData">
            <p class="is-size-5">Edit Attendence Rules</p>
            <br />
            <div class="field is-grouped is-grouped-multiline">
              <div class="control">
                <label for="" class="label">Late Come In</label>
                <input
                  type="text"
                  class="input"
                  ref="name"
                  v-model="edit.late_comin"
                  v-bind:class="[edit.errors.late_comin ? 'is-danger' : '']"
                  placeholder="Number of Late Comins"
                />
              </div>
              <div class="control">
                <label for="" class="label">Actual Days</label>
                <input
                  type="text"
                  class="input"
                  v-model="edit.late_comin_day"
                  v-bind:class="[edit.errors.late_comin_day ? 'is-danger' : '']"
                  placeholder="Actual Pay Day"
                />
              </div>
            </div>
            <div class="field is-grouped is-grouped-multiline">
              <div class="control">
                <label for="" class="label">Early Going</label>
                <input
                  type="text"
                  class="input"
                  v-model="edit.early_going"
                  v-bind:class="[edit.errors.early_going ? 'is-danger' : '']"
                  placeholder="Number of Early Going"
                />
              </div>
              <div class="control">
                <label for="" class="label">Actual Days</label>
                <input
                  type="text"
                  class="input"
                  v-model="edit.early_going_day"
                  v-bind:class="[
                    edit.errors.early_going_day ? 'is-danger' : '',
                  ]"
                  placeholder="Actual Pay Day"
                />
              </div>
            </div>
            <br />
            <div class="field is-grouped">
              <p class="control">
                <a class="button is-black" @click="saveEditData"
                  ><span class="icon icon-btn icon-btn-in"
                    ><b-icon icon="plus"></b-icon></span
                  >Save
                </a>
              </p>

              <p class="control">
                <a class="button" @click="modal = !modal"
                  ><span class="icon icon-btn icon-btn-in"
                    ><b-icon icon="x"></b-icon></span
                  >Cancel
                </a>
              </p>
              <div class="control" v-if="Object.keys(edit.errors).length != 0">
                <p class="has-text-danger is-underline">
                  Please fix the errors
                </p>
              </div>
            </div>
          </form>
        </div>
        <button
          class="modal-close is-large"
          aria-label="close"
          @click="modal = !modal"
        ></button>
      </div>
    </div>

    <!-- Entry Form -->

    <form id="data_entry" novalidate="true" @submit="submitData;" v-show="view">
      <p for="" class="is-size-5 has-text-weight-semibold">Attendence Rules</p>
      <br />
      <div class="box is-narrow">
        <p>
          <span class="icon icon-btn">
            <b-icon icon="information"></b-icon>
          </span>
          This section defines how to translate <u class="has-text-weight-semibold">late come ins</u> and
          <u class="has-text-weight-semibold">early goings</u> into actual pay days.
        </p>
        <hr style="margin: 1rem" />
        <p>
          <b
            >For e.g <br />
            - 3 early goings would translate to 0.5 day ( half-day).</b
          >
          <br />
          <b> - 5 Late Come Ins would translate to 1 day.</b>
        </p>
      </div>
      <div class="field is-grouped is-grouped-multiline">
        <div class="control">
          <label for="" class="label">Late Come In</label>
          <input
            type="text"
            class="input"
            ref="name"
            v-model="form.late_comin"
            v-bind:class="[form.errors.late_comin ? 'is-danger' : '']"
            placeholder="Number of Late Comins"
          />
        </div>
        <div class="control">
          <label for="" class="label">Actual Days</label>
          <input
            type="text"
            class="input"
            v-model="form.late_comin_day"
            v-bind:class="[form.errors.late_comin_day ? 'is-danger' : '']"
            placeholder="Actual Pay Day"
          />
        </div>
      </div>
      <div class="field is-grouped is-grouped-multiline">
        <div class="control">
          <label for="" class="label">Early Going</label>
          <input
            type="text"
            class="input"
            v-model="form.early_going"
            v-bind:class="[form.errors.early_going ? 'is-danger' : '']"
            placeholder="Number of Early Going"
          />
        </div>
        <div class="control">
          <label for="" class="label">Actual Days</label>
          <input
            type="text"
            class="input"
            v-model="form.early_going_day"
            v-bind:class="[form.errors.early_going_day ? 'is-danger' : '']"
            placeholder="Actual Pay Day"
          />
        </div>
      </div>
      <div class="field is-grouped is-grouped-multiline">
        <div class="control">
          <button type="submit" @click="submitData" class="button is-black">
            <span class="icon icon-btn icon-btn-in"
              ><b-icon icon="plus"></b-icon
            ></span>
            Save
          </button>
        </div>
        <div class="control">
          <button class="button" v-on:click="view = !view" @click="getData">
            <span class="icon icon-btn icon-btn-in"
              ><b-icon icon="eye"></b-icon
            ></span>
            View
          </button>
        </div>
        <div class="control" v-if="Object.keys(form.errors).length != 0">
          <p class="has-text-danger is-underline">Please fix the errors</p>
        </div>
      </div>
    </form>

    <!-- Table  -->

    <div v-show="!view">
      <div class="control">
        <button
          class="button"
          v-on:click="
            view = !view;
            form.errors = [];
          "
        >
          <span class="icon icon-btn icon-btn-in"
            ><b-icon icon="eye"></b-icon
          ></span>
          View
        </button>
      </div>
      <br />
      <div class="table-container" id="data_view">
        <table class="table is-bordered is-fullwidth">
          <thead>
            <tr>
              <th>Late Come In</th>
              <th>Late Come In -> Actual Days</th>
              <th>Early Going</th>
              <th>Early Going -> Actual Days</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in data" v-bind:index="index" :key="index">
              <td colspan="1">{{ row.late_comin }}</td>
              <td colspan="1">{{ row.late_comin_day }}</td>
              <td colspan="1">{{ row.early_going }}</td>
              <td colspan="1">{{ row.early_going_day }}</td>
              <td>
                <div class="buttons">
                  <div class="button" @click="editData(row)">Edit</div>
                  <div class="dropdown">
                    <div class="dropdown is-hoverable">
                      <div class="dropdown-trigger">
                        <button
                          class="button is-danger"
                          aria-haspopup="true"
                          aria-controls="dropdown-menu4"
                        >
                          <span>Delete</span>
                        </button>
                      </div>
                      <div
                        class="dropdown-menu"
                        style="z-index: 10"
                        id="dropdown-menu4"
                        role="menu"
                      >
                        <div class="dropdown-content has-background-light">
                          <p class="dropdown-item">Are you sure ?</p>
                          <hr class="dropdown-divider" />

                          <a class="dropdown-item">
                            <div class="buttons">
                              <div
                                class="button is-danger is-small"
                                @click="deleteData(row, index)"
                              >
                                Delete
                              </div>
                              <div class="button is-small">Cancel</div>
                            </div>
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </td>
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
  data() {
    return {
      view: true,
      form: {
        errors: {},
        id: null,
        late_comin: null,
        late_comin_day: null,
        early_going: null,
        early_going_day: null,
      },
      data: null,
      modal: false,
      edit: {
        errors: {},
        id: null,
        late_comin: null,
        late_comin_day: null,
        early_going: null,
        early_going_day: null,
      },
      confirm: false,
      ascending: false,
      sortColumn: "",
    };
  },
  mounted() {
   
    // this.focusInput();
  },
  methods: {
    focusInput() {
      this.$refs.name.focus();
    },
    checkData(e) {
      this.form.errors = {};

      if (!this.form.early_going) {
        this.$set(this.form.errors, "early_going", "Data required");
      }
      if (!this.form.early_going_day) {
        this.$set(this.form.errors, "early_going_day", "Data required");
      }
      if (!this.form.late_comin) {
        this.$set(this.form.errors, "late_comin", "Data required");
      }
      if (!this.form.late_comin_day) {
        this.$set(this.form.errors, "late_comin_day", "Data required");
      }

      if (Object.keys(this.form.errors).length === 0) {
        return true;
      } else {
        return false;
      }
    },

    submitData(e) {
      let formdata = this;

      if (this.checkData()) {
        this.$axios
          .post("/master/add/attendence_rules", this.form)
          .then(function (response) {
            if (response.data.success) {
              formdata.$buefy.snackbar.open({
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
            } else {
              formdata.$buefy.snackbar.open({
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
            console.log(error);
          });
      }
      e.preventDefault();
      this.focusInput();
    },
    getData(e) {
      const formdata = this;

      this.$axios
        .get("/master/get/attendence_rules")
        .then(function (response) {
          console.log(response);
          formdata.data = response["data"];
        })
        .catch(function (error) {
          console.log(error);
        });

      e.preventDefault();
    },
    editData(data) {
      this.edit.errors = [];

      this.modal = true;
      this.edit.late_comin = data.late_comin;
      this.edit.early_going = data.early_going;
      this.edit.late_comin_day = data.late_comin_day;
      this.edit.early_going_day = data.early_going_day;
      this.edit.id = data.id;
    },
    saveEditData(e) {
      const formdata = this;
      var data = this.data;

      this.edit.errors = {};
      if (this.edit.early_going == "") {
        this.$set(this.edit.errors, "early_going", "Data required");
      }
      if (this.edit.early_going_day == "") {
        this.$set(this.edit.errors, "early_going_day", "Data required");
      }
      if (this.edit.late_comin == "") {
        this.$set(this.edit.errors, "late_comin", "Data required");
      }
      if (this.edit.late_comin_day == "") {
        this.$set(this.edit.errors, "late_comin_day", "Data required");
      }

      if (Object.keys(this.edit.errors).length == 0) {
        console.log("error free");

        this.$axios
          .post("/master/edit/attendence_rules", formdata.edit)
          .then(function (response) {
            console.log(response.data);
            if (response.data.success) {
              data = data.filter(function (x) {
                return x.id === formdata.edit.id;
              });
              data[0].early_going = formdata.edit.early_going;
              data[0].early_going_day = formdata.edit.early_going_day;
              data[0].late_comin = formdata.edit.late_comin;
              data[0].late_comin_day = formdata.edit.late_comin_day;

              formdata.modal = !formdata.modal;

              formdata.$buefy.snackbar.open({
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
            } else {
              if (response.data.message) {
                formdata.$buefy.snackbar.open({
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
            }
          })

          .catch(function (error) {
            console.log(error);
          });
        return true;
      }

      e.preventDefault();
    },
    deleteData(data, index) {
      // const removeId = data.id;
      let formdata = this;

      var datalist = this.data;

      this.$axios
        .post("/master/delete/attendence_rules", data)
        .then(function (response) {
          if (response.data.success) {
            datalist.splice(index, 1);
            formdata.$buefy.snackbar.open({
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
          }
        })
        .catch(function (error) {
          console.log(error);
          formdata.$buefy.snackbar.open({
            duration: 4000,
            message: error,
            type: "is-light",
            position: "is-top-right",
            actionText: "Close",
            queue: true,
            onAction: () => {
              this.isActive = false;
            },
          });
        });
    },
  },
};
</script>

<style>
</style>