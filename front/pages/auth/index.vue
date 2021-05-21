<template>
  <div class="">
    <section class=" hero my-0 is-fullwidth">
      <div class="hero-head">
        <div class="level is-mobile my-0 py-2 px-4">
        
            <div class="level-left">
              <div class="level-item">
                <figure class="image"  style="width: 100px;filter:invert(100%)">
                  <img src="~/static/type-logo.svg" alt="" />
                </figure>
              </div>
              <div class="level-item">
                <div>

                <!-- <p href="https://github.com/highoncarbs/hafta" class="pt-3 has-text-weight-medium heading has-text-grey">
                  Multi Location <br> Inventory & Production <br> Management
                </p> -->
                </div>
              </div>
            </div>
            <div class="level-right">

              <a href="" class="has-text-right  heading has-text-dark  level-item">
                PRODUCT OF <br> PEPLUM STUDIO
              </a>
            </div>
          
        </div>
      </div>
      <hr class="my-1">
      <!-- <hr class="has-background-grey-lighter" style="height: 1px" /> -->
      <div class="hero-body" style="margin-top: 5rem">
        <div class="container">
          <div class="columns is-centered">
            <div class="column is-one-third-desktop is-centered">
              <!-- <p class="heading ml-0 mt-3 pl-2 has-text-grey has-text-weight-bold has-text-black ">
                For Jai Texart
              </p> -->
              <br />
              <br />
              <p class="is-size-5 has-text-grey">
              <span class="has-text-weight-bold">
                  Welcome back.
                </span>
                <br />Please login in to continue
              </p>
              <br />
              <p
                class="has-text-weight-bold has-text-danger"
                v-if="login_error"
              >
                <b-icon icon="account-alert" class></b-icon>
                <span style="margin-left: 0.5rem"
                  >Invalid login username & password</span
                >
              </p>
              <div class style="margin-top: 1rem">
                <b-field
                  :type="{ 'is-danger': error.username }"
                  label="Username"
                >
                  <b-input
                    v-model="username"
                    icon="account"
                    placeholder="Enter Username"
                  />
                </b-field>
                <b-field
                  :type="{ 'is-danger': error.password }"
                  label="Password"
                >
                  <b-input
                    type="password"
                    v-model="password"
                    icon="lock"
                    placeholder="Enter Password"
                  />
                </b-field>

                <div class="control" style="margin-bottom: 10px">
                  <button
                    native-type="submit"
                    @click="login"
                    :disabled="isSubmitting"
                    class="button is-black is-fullwidth"
                  >
                    <span v-if="!isSubmitting">Log In</span>
                    <span v-if="isSubmitting">Logging In ...</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  layout: "empty",
  data() {
    return {
      isSubmitting: false,
      username: "",
      password: "",
      error: {},
      login_error: false,
    };
  },
  mounted() {
    if (this.$auth.loggedIn) {
      this.$router.push("/");
    }
  },
  methods: {
    checkData() {
      this.error = {};
      if (this.username && this.password) {
        return true;
      }

      if (!this.username) {
        this.$set(this.error, "username", true);
      }
      if (!this.password) {
        this.$set(this.error, "password", true);
      }
    },
    login() {
      this.login_error = false;
      if (this.checkData()) {
        let formData = { username: this.username, password: this.password };
        this.isSubmitting = true;
        this.$auth
          .loginWith("local", { data: formData })
          .then((response) => {})
          .catch((error) => {
            this.login_error = true;
            this.$buefy.snackbar.open({
              duration: 4000,
              message: "Unable to login",
              type: "is-light",
              position: "is-top",
              actionText: "Close",
              queue: true,
              onAction: () => {
                this.isActive = false;
              },
            });
            console.log(error);
          })
          .finally(() => {
            this.isSubmitting = false;
          });
      }
    },
  },
};
</script>
<style >
html {
  background-color: white !important;
}
</style>