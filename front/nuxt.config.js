const config= {
  // static_path: process.env.NODE_ENV !== 'production' ? 'http://127.0.0.1:8888' : 'http://api.jaitexart.org/static',
  // static_base: process.env.NODE_ENV !== 'production' ? 'http://127.0.0.1:5555/static/uploads' : 'https://saas-space.ams3.cdn.digitaloceanspaces.com/',
  apiserver: process.env.NODE_ENV !== 'production' ? '127.0.0.1' : 'h-api.jaitexart.org',
  apiserver_port: process.env.NODE_ENV !== 'production' ? '5234' : '80',
}

export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
 
 
  head: {
    title: 'Hafta',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/Logo-b.svg' },
      { rel: 'preconnect',  href: 'https://fonts.gstatic.com' },
      { rel: 'stylesheet', type: 'text/css', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' },
    ]
  },
  ssr:false,
  // head: {
  //   title: 'front',
  //   htmlAttrs: {
  //     lang: 'en'
  //   },
  //   meta: [
  //     { charset: 'utf-8' },
  //     { name: 'viewport', content: 'width=device-width, initial-scale=1' },
  //     { hid: 'description', name: 'description', content: '' }
  //   ],
  //   link: [
  //     { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
  //   ]
  // },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '~/plugins/extras.js','~/plugins/inter.js'
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    '@nuxtjs/html-validator'

  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/buefy
    ['nuxt-buefy'],
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth',

  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  auth: {
    strategies: {
      local: {
        // redirect: {
        //   login: '/auth',
        //   logout: '/',
        //   home: '/',
        //   callback: '/auth'
        // },
        redirect: {
          login: '/auth',
          logout: '/',
          callback: '/auth',
          home: '/'
        },
        endpoints: {
          login: { url: '/auth/login', method: 'post', propertyName: 'token' },
          logout: { url: '/auth/logout', method: 'delete' },
          user: { url: '/auth/user', method: 'get', propertyName: 'user' }
        },
        // tokenRequired: true,
        // tokenType: '',
        // globalToken: true,
        // autoFetchUser: true
      }
    }
  },
  axios: {
    host:  config.apiserver,
    port:  config.apiserver_port,
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  }
}
