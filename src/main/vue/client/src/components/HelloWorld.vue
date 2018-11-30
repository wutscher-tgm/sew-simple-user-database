<template>
  <div class="hello">
    <h1>Simple User Database</h1>
    <button type="button" class="btn btn-success" data-toggle="modal" data-target="#createNew">+Create</button>
    <div class="modal" tabindex="-1" role="dialog" id="createNew">
      <div class="modal-dialog modal-lg" role="document">

          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Create new</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <div class="form-group custom-file">
                <input type="file" name="picture" class="custom-file-input" id="addStudentFile">
                <label class="custom-file-label" for="addStudentFile">Choose file</label>
              </div>
              <div class="form-group">
                <label for="addStudentUsername">Username</label>
                <input type="text" name="username" class="form-control" id="addStudentUsername" v-model="addStudentInput.name" placeholder="Enter username">
              </div>
              <div class="form-group">
                <label for="addStudentEmail">Email address</label>
                <input type="email" name="email" class="form-control" id="addStudentEmail" v-model="addStudentInput.email" placeholder="Enter email">
              </div>
            </div>
            <div class="modal-footer">
              <input type="button" v-on:click="addStudent()" class="btn btn-primary" value="Create">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
      </div>
    </div>

    <table class="table">
      <thead>
        <tr>
          <th scope="col">Picture</th>
          <th scope="col">Name</th>
          <th scope="col">Email</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students">
          <td><img src="" alt=""></td>
          <td>{{ student.username }}</td>
          <td>{{ student.email }}</td>
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
      const path = 'http://localhost:5000/students';
      var data = new FormData();
      var imagefile = document.querySelector('#addStudentFile');
      data.append('picture', imagefile.files[0]);
      data.append('email', this.addStudentInput.email);
      data.append('username', this.addStudentInput.name);
      console.log(data.entries());
      console.log(`email: ${this.addStudentInput.email}\nusername: ${this.addStudentInput.name}`);
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
    }
  },
  created(){
    this.getStudents()
  }
}
</script>
