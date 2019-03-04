'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  //BACKEND_SERVER: '"localhost:5000/"'
  BACKEND_SERVER: '"https://sew.projects.rwutscher.com/students"'
})
