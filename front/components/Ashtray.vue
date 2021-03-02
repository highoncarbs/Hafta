<template>
  <div>
        <div id="triggerBtn">
          <b-dropdown
            position="is-top-left"
            append-to-body
            aria-role="menu"
            trap-focus
          >
            <a
              class="button is-danger"
              slot="trigger"
              slot-scope="{ active }"
              role="button"
            >
              <b-icon icon="bug"></b-icon>
              <span>Report Bugs</span>
            </a>

            <b-dropdown-item
              aria-role="menu-item"
              class="is-marginless is-paddingless my-0 py-0 px-0 mx-0"
              :focusable="false"
              custom
            >
              <div style="width: 400px">
                <div class="danger-bg">
                  <p
                    class="is-size-5 has-text-white has-text-centered has-text-weight-bold"
                    style="position: relative"
                  >
                    Something broken ? Help us out
                  </p>
                  <p
                    class="has-text-centered has-text-white"
                    style="position: relative"
                  >
                    Add Bug report title & description
                  </p>
                </div>
                <div style="padding: 1rem 1.5rem">
                  <b-field label="Title">
                    <b-input
                      type="text"
                      placeholder="Report Title"
                      v-model="title"
                    ></b-input>
                  </b-field>
                  <b-field label="Description">
                    <b-input
                      type="textarea"
                      v-model="description"
                      placeholder="Enter a word or two about how the software broke."
                    ></b-input>
                  </b-field>
                  <div class="mt-4">
                    <div class="level is-mobile">
                      <div class="level-left">
                        <div class="level-item">
                          <button @click="sendReport" class="button is-danger">
                            <span>Submit Report</span>
                          </button>
                        </div>
                      </div>
                      <div class="level-right">
                        <div class="level-item">
                          <button @click="view = !view" class="button">
                            Close
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </b-dropdown-item>
          </b-dropdown>
        </div>
    <!-- <button
      id="triggerBtn"
      @click="view = !view"
      class="button button-shadow is-danger has-text-danger-light"
    >
      <b-icon icon="bug"></b-icon>
      <span>Report Bugs</span>
    </button> -->
  </div>
</template>
<script>
export default {
  data() {
    return {
      view: false,
      title: "",
      token: "9708d4e676ee9b8348f6fd0411fd02f857441862",
      description: "",
      payload: [],
    };
  },
  mounted() {
    if (console.everything === undefined) {
      console.everything = [];

      console.defaultLog = console.log.bind(console);
      console.log = function () {
        console.everything.push({
          type: "log",
          datetime: Date().toLocaleString(),
          value: Array.from(arguments),
        });
        console.defaultLog.apply(console, arguments);
      };
      console.defaultError = console.error.bind(console);
      console.error = function () {
        console.everything.push({
          type: "error",
          datetime: Date().toLocaleString(),
          value: Array.from(arguments),
        });
        console.defaultError.apply(console, arguments);
      };
      console.defaultWarn = console.warn.bind(console);
      console.warn = function () {
        console.everything.push({
          type: "warn",
          datetime: Date().toLocaleString(),
          value: Array.from(arguments),
        });
        console.defaultWarn.apply(console, arguments);
      };
      console.defaultDebug = console.debug.bind(console);
      console.debug = function () {
        console.everything.push({
          type: "debug",
          datetime: Date().toLocaleString(),
          value: Array.from(arguments),
        });
        console.defaultDebug.apply(console, arguments);
      };
    }
  },
  methods: {
    sendReport() {
      this.payload.push({ location: window.location });
      //   this.payload.push({ logs: console.everything.splice(-5) });

      console.log(console.everything);
      if (typeof console._commandLineAPI !== "undefined") {
        console.API = console._commandLineAPI; //chrome
        consoel.log(console.API);
      }
      let temp_payload = {
        title: this.title,
        body: this.description + "\n `" + JSON.stringify(this.payload) + "`",
        labels: ["ashtray"],
      };
      let headers = {
        "Content-type": "Application/json",
        Authorization: `token ${this.token}`,
      };
      this.$axios
        .post(
          "https://api.github.com/repos/highoncarbs/production/issues",
          temp_payload,
          {
            headers: {
              "Content-type": "Application/json",

              Authorization: `token ${this.token}`,
            },
          }
        )
        .then((response) => {
          this.title = "";
          this.description = "";
          this.payload = [];
          this.$buefy.snackbar.open({
            duration: 4000,
            message: "Report Submitted",
            type: "is-light",
            position: "is-top-right",
            actionText: "Close",
            queue: true,
            onAction: () => {
              this.isActive = false;
            },
          });
          this.view = false;
        })
        .catch((error) => {
          this.$buefy.snackbar.open({
            duration: 4000,
            message: "Unable to submit Report",
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
#triggerBtn {
  position: fixed;
  bottom: 15px;
  right: 15px;
  z-index: 99999;
}

.danger-bg {
  position: relative;
  border-radius: 5px 5px 0 0;
  background-color: #ff3860;
  background-image: url("data:image/svg+xml,%3Csvg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M9 0h2v20H9V0zm25.134.84l1.732 1-10 17.32-1.732-1 10-17.32zm-20 20l1.732 1-10 17.32-1.732-1 10-17.32zM58.16 4.134l1 1.732-17.32 10-1-1.732 17.32-10zm-40 40l1 1.732-17.32 10-1-1.732 17.32-10zM80 9v2H60V9h20zM20 69v2H0v-2h20zm79.32-55l-1 1.732-17.32-10L82 4l17.32 10zm-80 80l-1 1.732-17.32-10L2 84l17.32 10zm96.546-75.84l-1.732 1-10-17.32 1.732-1 10 17.32zm-100 100l-1.732 1-10-17.32 1.732-1 10 17.32zM38.16 24.134l1 1.732-17.32 10-1-1.732 17.32-10zM60 29v2H40v-2h20zm19.32 5l-1 1.732-17.32-10L62 24l17.32 10zm16.546 4.16l-1.732 1-10-17.32 1.732-1 10 17.32zM111 40h-2V20h2v20zm3.134.84l1.732 1-10 17.32-1.732-1 10-17.32zM40 49v2H20v-2h20zm19.32 5l-1 1.732-17.32-10L42 44l17.32 10zm16.546 4.16l-1.732 1-10-17.32 1.732-1 10 17.32zM91 60h-2V40h2v20zm3.134.84l1.732 1-10 17.32-1.732-1 10-17.32zm24.026 3.294l1 1.732-17.32 10-1-1.732 17.32-10zM39.32 74l-1 1.732-17.32-10L22 64l17.32 10zm16.546 4.16l-1.732 1-10-17.32 1.732-1 10 17.32zM71 80h-2V60h2v20zm3.134.84l1.732 1-10 17.32-1.732-1 10-17.32zm24.026 3.294l1 1.732-17.32 10-1-1.732 17.32-10zM120 89v2h-20v-2h20zm-84.134 9.16l-1.732 1-10-17.32 1.732-1 10 17.32zM51 100h-2V80h2v20zm3.134.84l1.732 1-10 17.32-1.732-1 10-17.32zm24.026 3.294l1 1.732-17.32 10-1-1.732 17.32-10zM100 109v2H80v-2h20zm19.32 5l-1 1.732-17.32-10 1-1.732 17.32 10zM31 120h-2v-20h2v20z' fill='%23ffffff' fill-opacity='0.45' fill-rule='evenodd'/%3E%3C/svg%3E");
  padding: 1rem 0.5rem;
}
.danger-bg-foot {
  /* background-color: hsl(347, 90%, 96%); */
  padding: 1rem 1.5rem;
}

.danger-bg::before {
  background: linear-gradient(
    45deg,
    rgba(255, 56, 96, 0.7) 0%,
    rgba(255, 56, 96, 1) 100%
  );
  border-radius: 5px 5px 0 0;
  color: white;
  opacity: 1;
  position: absolute;
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

/* .button-shadow{
    box-shadow: 4px 4px 0px pink !important;
    transition: 0.2s all ease-in;
}
.button-shadow:hover{
    box-shadow: 1px 1px 0px pink !important;
} */
</style>