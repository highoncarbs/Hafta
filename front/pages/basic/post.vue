<template>
  <div>
    <div class="has-background-white" style="border-top: 1px solid #eee">
      <div
        class="section py-4 pt-5 is-fullwidth is-fullheight"
        :class="{ 'container px-0': $store.state.win }"
      >
        <p class="is-size-5 has-text-weight-bold">Post</p>
        <br />
        <!-- Edit Modal -->
        <div
          class="modal animated fadeIn"
          :class="{ 'is-active': modal == true }"
        >
          <div class="modal-background" @click="modal = !modal"></div>
          <div class="modal-content">
            <div class="card">
              <div class="card-content">
                <div class="content">
                  <p class="has-text-weight-bold is-size-5">Edit Post</p>

                  <b-field
                    labe="Post"
                    :type="{ 'is-danger': edit.errors.name }"
                  >
                    <b-input
                      v-model="edit.name"
                      red="editname"
                      placeholder="Enter Post"
                    ></b-input>
                  </b-field>
                </div>
              </div>
              <footer class="card-footer">
                <a class="card-footer-item" @click="saveEditData">
                  <span class="icon icon-in">
                    <b-icon icon="refresh"></b-icon>
                  </span>
                  Update
                </a>
                <a
                  class="card-footer-item has-text-grey"
                  @click="modal = !modal"
                >
                  <span class="icon icon-in">
                    <b-icon icon="close"></b-icon>
                  </span>
                  Close
                </a>
              </footer>
            </div>

            <button
              class="modal-close is-large"
              aria-label="close"
              @click="modal = !modal"
            ></button>
          </div>
        </div>

        <!-- Entry Form -->

        <form
          id="data_entry"
          class="animated fadeIn"
          novalidate="true"
          @submit="submitData;"
          v-show="view"
        >
          <div class="columns">
            <div class="column">
              <b-field label="Name" :type="{ 'is-danger': form.errors.name }">
                <b-input
                  v-model="form.name"
                  ref="name"
                  placeholder="Enter Name"
                ></b-input>
              </b-field>
              <div class="buttons">
                <button
                  type="submit"
                  @click="submitData"
                  class="button is-black"
                >
                  <b-icon class="icon-in" icon="check" />Save
                </button>

                <button
                  class="button"
                  v-on:click="view = !view"
                  @click="getData"
                >
                  <span class="icon icon-in">
                    <b-icon icon="eye"></b-icon>
                  </span>
                  View
                </button>
              </div>
           
            </div>
          </div>
        </form>

        <!-- Table  -->

        <div v-show="!view" class="animated fadeIn">
          <b-field grouped class="mb-2">
            <b-field>
              <button
                class="button is-black"
                v-on:click="
                  view = !view;
                  form.errors = [];
                "
              >
                <span class="icon icon-in">
                  <b-icon icon="plus"></b-icon>
                </span>
                Add
              </button>
            </b-field>

            <b-field expanded>
              <p class="control">
                <b-select v-model="showItems" icon="filter-variant">
                  <option value="20">20</option>
                  <option value="40">40</option>
                  <option value="60">60</option>
                  <option value="100">100</option>
                </b-select>
              </p>
              <b-input
                @keypress.native.enter="loadAsyncSearch"
                v-model="query_search"
                expanded
                icon="magnify"
                placeholder="Search"
              ></b-input>
            </b-field>
          </b-field>

          <div class id="data_view">
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
                    icon="file-plus"
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
              <b-table-column v-slot="props" label="Name">{{
                props.row.name
              }}</b-table-column>

              <b-table-column v-slot="props" label="">
                <div class="buttons">
                  <button
                    @click="editData(props.row, index)"
                    class="button is-light"
                  >
                    Edit</button
                  ><button
                    @click="deleteData(props.row, index)"
                    class="button is-danger"
                  >
                    <b-icon icon="delete"></b-icon>
                  </button>
                </div>
              </b-table-column>
            </b-table>
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
        errors: [],
        id: null,
        name: null,
      },
      showItems: 20,
      totalItems: 20,
      data: [],
      modal: false,
      edit: {
        errors: [],
        name: null,
        index: null,
      },
    };
  },

  mounted() {
    this.$refs.name.focus();
  },
  methods: {
    checkData(e) {
      this.form.errors = [];

      if (this.form.name) {
        return true;
      }
        if (!this.form.name) {
        this.$set(this.form.errors , 'name' , true )
      }
    },

    submitData(e) {
      var self = this;

      if (this.checkData()) {
        this.$axios
          .post("/master/add/post", this.form)
          .then(function (response) {
            if (response.data.success) {
              self.form.name = null;

              self.$buefy.snackbar.open({
                duration: 4000,
                message: response.data.success,
                type: "is-light",
                position: "is-top-right",
                actionText: "Close",
                queue: true,
                onAction: () => {
                  self.isActive = false;
                },
              });
            } else {
              if (response.data.message) {
                self.$buefy.snackbar.open({
                  duration: 4000,
                  message: response.data.message,
                  type: "is-light",
                  position: "is-top-right",
                  actionText: "Close",
                  queue: true,
                  onAction: () => {
                    self.isActive = false;
                  },
                });
              }
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      }
      e.preventDefault();
    },
    getData(e) {
      const self = this;

      this.$axios
        .get("/master/get/post")
        .then(function (response) {
          self.data = response["data"];
        })
        .catch(function (error) {
          console.log(error);
        });

      e.preventDefault();
    },
    editData(data, index) {
      this.edit.errors = [];

      this.modal = true;
      this.edit.name = data.name;
      this.edit.id = data.id;
      this.edit.index = index;

      //this.$refs.editname.focus();
    },
    saveEditData(e) {
      const self = this;
      let dataList = this.data;
      if (this.edit.name) {
        this.$axios
          .post("/master/edit/post", this.edit)
          .then(function (response) {
            if (response.data.success) {
              dataList = self.data.filter(function (x) {
                return x.id === self.edit.id;
              });
              dataList[0].name = self.edit.name;
              dataList[0].descrip = self.edit.descrip;
              self.modal = !self.modal;

              self.$buefy.snackbar.open({
                duration: 4000,
                message: response.data.success,
                type: "is-light",
                position: "is-top-right",
                actionText: "Close",
                queue: true,
                onAction: () => {
                  self.isActive = false;
                },
              });
            } else {
              if (response.data.message) {
                self.$buefy.snackbar.open({
                  duration: 4000,
                  message: response.data.message,
                  type: "is-light",
                  position: "is-top-right",
                  actionText: "Close",
                  queue: true,
                  onAction: () => {
                    self.isActive = false;
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

      this.edit.errors = [];
      console.log(this.edit.name);

      if (this.edit.name == "") {
        this.edit.errors.push("Post required");
      }

      e.preventDefault();
    },
    deleteData(data, index) {
      let dataList = this.data;
      let self = this;
      this.$axios
        .post("/master/delete/post", data)
        .then(function (response) {
          if (response.data.success) {
            dataList.splice(index, 1);
            self.$buefy.snackbar.open({
              duration: 4000,
              message: response.data.success,
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                self.isActive = false;
              },
            });
          } else {
            self.$buefy.snackbar.open({
              duration: 4000,
              message: response.data.message,
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                self.isActive = false;
              },
            });
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
};
</script>