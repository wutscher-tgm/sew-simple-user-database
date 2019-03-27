<template>
  <tr v-bind:id="'sutdent-'+index">
    
  </tr>
</template>

<script>
  import { EventBus } from '../event-bus.js'
  import axios from 'axios'

  export default {
    name: 'EditStudent',
    props: ['student', 'index', 'parent'],
    data() {
      return {
        
      }
    },
  }
</script>
