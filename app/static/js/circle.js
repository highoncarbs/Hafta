<template>
<span>
  <svg width="44px" height="44px" viewBox="0 0 44 44" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <title>My Icon</title>
    <desc>Created with Sketch.</desc>
    <defs></defs>
    <g id="icons" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
        <g id="Artboard" transform="translate(-90.000000, -64.000000)">
            <circle id="Oval-7" :stroke="color" cx="7" cy="22" r="2"></circle>
        </g>
    </g>
  </svg>
</span>
</template>

<script>
export default {
  name: 'ub-circle-icon',
  props: [
    'color',
  ],
};
</script>

<style lang="scss" scoped>
</style>