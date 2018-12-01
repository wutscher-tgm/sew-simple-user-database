<template>
  <div class="hello">
    <h1>Simple User Database</h1>

    <table class="table">
      <thead>
        <tr>
          <th scope="col">Picture</th>
          <th scope="col">Email</th>
          <th scope="col">Username</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr>

          <td>
            <label class="btn">
              <img v-bind:src="url" style="width:50px; border-radius: 50%" alt="">
              <input type="file" id="addStudentFile" v-on:change="updatePreviewImage()" accept=".png,.jpg,.jepg" style="display: none">
            </label>
          </td>
          <td><input type="email" name="email" class="form-control" id="addStudentEmail" v-model="addStudentInput.email" placeholder="Enter email"></td>
          <td><input type="text" name="username" class="form-control" id="addStudentUsername" v-model="addStudentInput.name" placeholder="Enter username"></td>
          <td>
            <div class="btn-group" role="group" aria-label="Basic example">
              <button type="button" v-on:click="addStudent()" class="btn btn-success">Upload</button>
              <button type="button" class="btn btn-danger">Cancel</button>
            </div>
          </td>
        </tr>

        <!--
        <form class="md-form">

      </form>
        -->

        <tr v-for="student in students">
          <td><img width="50px" style="border-radius: 50%;" v-bind:src="'data:image/jpeg;base64,'+student.picture" /></td>
          <td>{{ student.email }}</td>
          <td>{{ student.username }}</td>
          <td>
            <div class="btn-group" role="group" aria-label="Basic example">
              <button type="button" class="btn btn-primary">Edit</button>
              <button type="button" class="btn btn-danger">Delete</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'HelloWorld',
  data () {
    return {
        students: null,
        url: 'https://mdbootstrap.com/img/Photos/Others/placeholder-avatar.jpg',
        addStudentInput: {
          name: '',
          email: '',
          picture: ''
        }
    }
  },
  methods:{
    getStudents() {
      const path = 'http://localhost:5000/students';
      axios.get(path)
        .then((res) => {
          this.students = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addStudent: function() {

      var data = new FormData();
      var imagefile = document.querySelector('#addStudentFile');
      data.append('picture', imagefile.files[0]);
      console.log(imagefile.files[0]);
      const path = `http://localhost:5000/students?email=${this.addStudentInput.email}&username=${this.addStudentInput.name}`;
      axios.post(path, data,{
        headers: {
            'Content-Type': 'multipart/form-data'
        }
      }).then((res) => {
        console.log(res);
        this.getStudents();
      }).catch((error) => {
        console.error(error);
      });
    },
    updatePreviewImage: function(){
      var imagefile = document.querySelector('#addStudentFile');
      this.url = URL.createObjectURL(imagefile.files[0]);
    }
  },
  created(){
    this.getStudents()
  }
}
</script>
