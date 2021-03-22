<template>
    <div class="row">
        <button v-on:click="sendMessage('hello')">Send Message</button>
        llllllllllllazeazelllllll
    </div>
</template>



<script>
export default {
  name: "PublicPosts",
  data: function() {
    return {
      connection: null
    }
  },
  methods: {
    sendMessage: function(message) {
      console.log("Hello")
      console.log(this.connection);
      this.connection.send(message);
    }
  },
  created: function() {
    console.log("Starting connection to WebSocket Server")
    this.connection = new WebSocket("wss://localhost:8000/toto/ws")

    this.connection.onmessage = function(event) {
      console.log(event);
    }

    this.connection.onopen = function(event) {
      console.log(event)
      console.log("Successfully connected to the echo websocket server...")
    }

  }
}
</script>




<style scoped>
</style>