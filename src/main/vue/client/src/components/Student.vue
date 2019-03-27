<template>
  <tr v-bind:id="'student-'+index">
    <td v-if="!editing" v-bind:id="index+'-picture'">
      <img
        width="50px"
        style="border-radius: 50%;"
        v-bind:src="'data:image/jpeg;base64,'+student.picture"
      >
    </td>
    <td v-if="!editing" v-bind:id="index+'-email'">{{ student.email }}</td>
    <td v-if="!editing" v-bind:id="index+'-username'">{{ student.username }}</td>

    <!-- Editing -->
    <td v-if="editing" v-bind:id="index+'-picture'">
      <label class="btn">
        <img v-bind:src="url" style="width:50px; border-radius: 50%" alt>
        <input
          type="file"
          v-bind:id="index+'-picture-input'"
          v-on:change="updateEditPreviewImage()"
          accept=".png, .jpg, .jepg"
          style="display: none"
        >
      </label>
    </td>
    <td v-if="editing" v-bind:id="index+'-email'">{{ student.email }}</td>
    <td v-if="editing" v-bind:id="index+'-username'">
      <input
        type="text"
        class="form-control"
        v-bind:id="this.index+'-username-input'"
        v-bind:value="student.username"
      >
    </td>

    <td>
      <div class="btn-group" v-bind:id="index+'-buttons'" role="group" aria-label="Basic example">
        <button v-if="!editing" type="button" class="btn btn-warning" v-on:click="updateStudent()">Edit</button>
        <button v-if="editing" type="button" class="btn btn-success" v-on:click="sendUpdateStudent()">Submit</button>
        <button type="button" class="btn btn-danger" v-on:click="deleteStudent()">Delete</button>
      </div>
    </td>
  </tr>
</template>

<script>
import EditStudent from "@/components/EditStudent";
import axios from "axios";
export default {
  name: "Student",
  props: ["student", "index"],
  data() {
    return {
      editing: false,
      url: 'https://mdbootstrap.com/img/Photos/Others/placeholder-avatar.jpg'
    };
  },
  components: {
    EditStudent: EditStudent
  },
  methods: {
    setEditable: function() {
      let image = document.getElementById(`#${this.index}-picture`);
      let email = document.getElementById(`#${this.index}-email`);
      let username = document.getElementById(`#${this.index}-username`);

      //image.innerHTML('<label class="btn"><img v-bind:src="url" style="width:50px; border-radius: 50%" alt=""><input type="file" v-bind:id="index+'-picture-input'" v-on:change="updateEditPreviewImage()" accept=".png,.jpg,.jepg" style="display: none"></label>')
    },
    setUneditable: function() {},
    updateStudent: function() {
      this.editing = true
    },
    deleteStudent: function() {
      const path = process.env.BACKEND_SERVER; //+'?email='+this.student.email;
      let data = {
        email: this.student.email
      };
      axios
        .delete(path, { data: data })
        .then(res => {
          console.log(res);
          this.$parent.getStudents();
        })
        .catch(error => {
          console.error(error);
        });
    },
    sendUpdateStudent: function() {
      var data = new FormData();
      var imagefile = document.getElementById(`${this.index}-picture-input`);
      data.append("picture", imagefile.files[0]);
      data.append("email", this.student.email);
      data.append(
        "username",
        document.getElementById(`${this.index}-username-input`).value
      );

      console.log(data);
      axios
        .patch(process.env.BACKEND_SERVER, data, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
          auth: {
            username: this.parent.email,
            password: this.parent.password
          }
        })
        .then((err, res) => {
          console.log(res);
          console.log(err);
          //location.reload();
        });
    },
    updatePreviewImage: function() {
      var imagefile = document.querySelector("#addStudentFile");
      this.url = URL.createObjectURL(imagefile.files[0]);
    },
    deleteStudent: function(email) {
      const path = process.env.BACKEND_SERVER;
      axios
        .delete(
          path,
          { email: email },
          {
            auth: {
              username: this.parent.email,
              password: this.parent.password
            }
          }
        )
        .then(res => {
          console.log(res);
          this.parent.getStudents();
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>
