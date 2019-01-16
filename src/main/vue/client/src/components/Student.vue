<template>
  <tr v-bind:id="'student-'+index">
    <td v-bind:id="index+'-picture'"><img width="50px" style="border-radius: 50%;"
                                          v-bind:src="'data:image/jpeg;base64,'+student.picture"/></td>
    <td v-bind:id="index+'-email'">{{ student.email }}</td>
    <td v-bind:id="index+'-username'">{{ student.username }}</td>
    <td>
      <div class="btn-group" v-bind:id="index+'-buttons'" role="group" aria-label="Basic example">
        <button type="button" class="btn btn-warning" v-on:click="updateStudent()">Edit</button>
        <button type="button" class="btn btn-danger" v-on:click="deleteStudent()">Delete</button>
      </div>
    </td>
  </tr>
</template>

<script>
  import { EventBus } from '../event-bus.js'
  export default {
    name: 'Student',
    props: ['student', 'index'],
    methods: {
      updateStudent: function () {
        EventBus.$emit('updateStudent', this.index);
      },
      deleteStudent: function (email) {
        const path = `http://localhost:5000/students?email=${email}`;
        axios.delete(path).then((res) => {
          console.log(res);
          this.getStudents();
        }).catch((error) => {
          console.error(error);
        });
      },
    }
  }
</script>
