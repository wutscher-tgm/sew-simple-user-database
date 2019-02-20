<template>
  <tr v-bind:id="'sutdent-'+index">
    <td v-bind:id="index+'-picture'">
      <label class="btn">
        <img v-bind:src="url" style="width:50px; border-radius: 50%" alt="">
        <input type="file" v-bind:id="index+'-picture-input'" v-on:change="updateEditPreviewImage()" accept=".png,.jpg,.jepg" style="display: none">
      </label>
    </td>
    <td v-bind:id="index+'-email'">{{ student.email }}</td>
    <td v-bind:id="index+'-username'">
      <input type="text" class="form-control" v-bind:id="this.index+'-username-input'" v-bind:value="student.username">
    </td>
    <td>
      <div class="btn-group" v-bind:id="index+'-buttons'" role="group" aria-label="Basic example">
        <input type="button" class="btn btn-success" value="submit" v-on:click="sendUpdateStudent()">
      </div>
    </td>
  </tr>
</template>

<script>
  import { EventBus } from '../event-bus.js'
  import axios from 'axios'

  export default {
    name: 'EditStudent',
    props: ['student', 'index'],
    data() {
      return {
        url: 'https://mdbootstrap.com/img/Photos/Others/placeholder-avatar.jpg'
      }
    },
    methods: {
      sendUpdateStudent: function() {
        var data = new FormData();
        var imagefile = document.getElementById(`${this.index}-picture-input`);
        data.append('picture', imagefile.files[0]);
        data.append('email', this.student.email);
        data.append('username', document.getElementById(`${this.index}-username-input`).value);

        console.log(data)
        axios.patch(process.env.BACKEND_SERVER, data,{
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          auth:{
            username: this.$parent.email,
            password: this.$parent.password
          }
        }).then((err, res) => {
          console.log(res);
          console.log(err);
          //location.reload();
        });
		  },
      updatePreviewImage: function () {
        var imagefile = document.querySelector('#addStudentFile');
        this.url = URL.createObjectURL(imagefile.files[0]);
      },
      deleteStudent: function (email) {
        const path = process.env.BACKEND_SERVER;
        axios.delete(path, {email: email}, {
          auth:{
            username: this.$parent.email,
            password: this.$parent.password
          }
        }).then((res) => {
          console.log(res);
          this.getStudents();
        }).catch((error) => {
          console.error(error);
        });
      },
    }
  }
</script>
