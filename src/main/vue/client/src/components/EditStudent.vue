<template>
  <span>
    <td>
    <label class="btn">
      <img v-bind:src="url" style="width:50px; border-radius: 50%" alt="">
      <input type="file" id="addStudentFile" v-on:change="updatePreviewImage()" accept=".png,.jpg,.jepg"
             style="display: none">
    </label>
    </td>
    <td><input type="email" name="email" class="form-control" id="addStudentEmail" v-model="addStudentInput.email"
               placeholder="Enter email"></td>
    <td><input type="text" name="username" class="form-control" id="addStudentUsername" v-model="addStudentInput.name"
               placeholder="Enter username"></td>
    <td>
      <div class="btn-group" role="group" aria-label="Basic example">
        <button type="button" v-on:click="addStudent()" class="btn btn-success">Upload</button>
        <button type="button" class="btn btn-danger">Cancel</button>
      </div>
    </td>
  </span>
</template>

<script>
  export default {
    name: 'EditStudent',
    props: ['student'],
    methods: {}
  }
</script>
