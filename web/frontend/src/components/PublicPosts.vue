<template>
    <div class="row">
        <button v-on:click="sendMessage('hello')">Send Message</button>
        azeaze
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
  sockets: {
    connect() {
      // Fired when the socket connects.
      this.isConnected = true;
      console.log("helos")
    },

    disconnect() {
      this.isConnected = false;
    },

    // Fired when the server sends something on the "messageChannel" channel.
    tofront(data) {
      console.log("!!!!!!!!!!!!", data)
    }
  },
  methods: {
    sendMessage: function(message) {
      this.$socket.emit('chat', "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
      this.axios.get("/toto/tata").then((response) => {
        console.log("AXIOS GET", response.data)
      })
    }
  },
  // created: function() {
  //   console.log("Starting connection to WebSocket Server")
  //   this.connection = new WebSocket("wss://localhost:8000/toto/ws")

  //   this.connection.onmessage = function(event) {
  //     console.log(event);
  //   }

  //   this.connection.onopen = function(event) {
  //     console.log(event)
  //     console.log("Successfully connected to the echo websocket server...")
  //   }

  // }
}
</script>




<style scoped>
</style>
