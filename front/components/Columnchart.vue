 <template >
  <div class="columnchart_container">
    <span
      class="cols is-uppercase is-size-7 has-text-weight-semibold"
      v-for="(box, index) in datalist" :key="index"
      :data-tooltip="getTooltip(box, index)"
      :style="{ height: setHeight(box) }"
    >
      {{ box.performance_items[0].performance.name}}
      <br />
      <small>WEIGHT: {{ box.performance_items[0].performance.weight}} </small>
    </span>
  </div>
</template>

<script>
export default {
    data: function () {
    return {
      colorval: [],
      factors: this.datalist,
    };
  },
   props: {
    datalist: {
      type: Array,
      default: () => [],
    },
  },
  mounted() {
    let raw = this;
    this.datalist.forEach(function (item) {
      raw.colorval.push(Number(item) / 30);
    });
  },
  methods: {
    setHeight(data) {
      let val = data.performance_items[0]
      console.log('----H--', val)
      return (Number(val.obt_score) / val.performance.score) * 100 + "px";
    },
    getTooltip(data, index) {
      let factor = data.performance_items[0]
      console.log('----F--', factor)
      return (
        factor.obt_score +
        "/" +
        factor.performance.score +
        " " +
        factor.performance.name
      );
    },
  },
};
</script>

<style>
.cols {
  /* padding: 9px; */
  height: 12px;
  margin: 2px !important;
  /* background-color: grey; */
  /* font-size: 0 !important; */
  background-color: aquamarine !important;
  padding: 5px;
  display: inline-block;
}

[data-tooltip] {
  position: relative;
  z-index: 2;
  cursor: pointer;
}

/* Hide the tooltip content by default */
[data-tooltip]:before,
[data-tooltip]:after {
  visibility: hidden;
  -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=0)";
  filter: progid: DXImageTransform.Microsoft.Alpha(Opacity=0);
  opacity: 0;
  pointer-events: none;
}

/* Position tooltip above the element */
[data-tooltip]:before {
  position: absolute;
  bottom: 100%;
  left: 50%;
  margin-bottom: 5px;
  margin-left: -80px;
  padding: 7px;
  width: 160px;
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 3px;
  background-color: #000;
  background-color: hsla(0, 0%, 20%, 0.9);
  color: #fff;
  content: attr(data-tooltip);
  text-align: center;
  font-size: 14px;
  line-height: 1.2;
}

/* Triangle hack to make tooltip look like a speech bubble */
[data-tooltip]:after {
  position: absolute;
  bottom: 100%;
  left: 50%;
  margin-left: -5px;
  width: 0;
  border-top: 5px solid #000;
  border-top: 5px solid hsla(0, 0%, 20%, 0.9);
  border-right: 5px solid transparent;
  border-left: 5px solid transparent;
  content: " ";
  font-size: 0;
  line-height: 0;
}

/* Show tooltip content on hover */
[data-tooltip]:hover:before,
[data-tooltip]:hover:after {
  visibility: visible;
  -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=100)";
  filter: progid: DXImageTransform.Microsoft.Alpha(Opacity=100);
  opacity: 1;
}
</style>