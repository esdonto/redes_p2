<script>
  console.log("oi")
  export let name;
  import { onMount } from "svelte";

  let nameInput;
  let textInput;
  let messages = [];
  let inputText = "";
  let userName = "";
  let numUsers = 0;

  onMount(() => {
    textInput.focus();
  });
  const ws = new WebSocket("ws://localhost:8765");

  ws.onopen = function () {
    console.log("WebSocket Client conectado");
  };

  ws.onmessage = function (e) {
    console.log("Received: " + e.data);
    let data = JSON.parse(e.data);
    if (data.type == "message"){
      if ((userName === "") && (data.text == "Valid name!")){
        userName = data.name
      }
      messages = [...messages, data];
    }
    else if (data.type == "users"){
      numUsers = data.count;
    }
    else {
      console.error("unsupported event", data);
    }
  };

  function handleClick() {
    var today = new Date();
    ws.send(JSON.stringify({ type: "message", 
                             user: userName, 
                             time: today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(),
                             text: inputText}));
    inputText = "";
  }

</script>

<style>
  * {
    box-sizing: border-box;
  }

  main {
    width: calc(100% - 30px);
    text-align: center;
    padding: 1em;
    max-width: 1240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
    margin-top: 0.5em;
  }

  .chatbox {
    width: 100%;
    height: 50vh;
    padding: 0 1em;
    text-align: left;
    background-color: #333;
    overflow-y: scroll;
    overscroll-behavior-y: contain;
    scroll-snap-type: y proximity;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    background-image: url("skull.png");
    background-position: center;
    background-size: cover;
  }

  .chatbox p {
    margin-top: 0.5em;
    margin-bottom: 0;
    padding-bottom: 0.5em;
  }

  .chatbox > p:last-child {
    scroll-snap-align: end;
  }

  .inputbox {
    display: flex;
    margin-top: 0.5em;
  }

  .inputbox input {
    flex-grow: 1;
  }
</style>

<main>
  <h1>{name}</h1>
  <p>
    {numUsers > 1 ? numUsers : 'As always,'} {numUsers > 1 ? 'users online' : 'You\'re alone'}
  </p>
  <div class="chatbox">
    {#each messages as message}
      <p><small>{message.time}</small> <b>{message.user}:</b> {message.text}</p>
    {/each}
  </div>
  <form class="inputbox">
    <input type="text" bind:this={textInput} bind:value={inputText} />
    <button type="submit" on:click|preventDefault={handleClick}>Send</button>
  </form>
  <img src="https://media1.tenor.com/images/ec18da69bd006a92e5b3a234218308f6/tenor.gif" alt="Doot doot!"  height="135">
  <img src="https://media1.tenor.com/images/a369655bae5b5f8e8de548e631e80d19/tenor.gif" alt="Skeleton dance!"  height="135">
  <img src="https://media1.tenor.com/images/b4e13cf94fa51818aea8a520d21d0f49/tenor.gif"  alt="Spooky dance!"  height="135">
  <img src="https://media1.giphy.com/media/YwAgyCddum3K0/giphy.gif"  alt="Classic skeleton dance!"  height="135">
  <img src="https://media2.giphy.com/media/W3aGUCaO3mXdK/giphy.gif"  alt="Classic skeleton dance!"  height="135">
</main>
