<script>
  export let name;
  import { onMount } from "svelte";

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
        userName = data.name;
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

  function handleClick(e) {
    if ((e.type == "click") || (e.code == "Enter")) {
      var today = new Date();
      ws.send(JSON.stringify({ type: "message", 
                              user: userName, 
                              time: today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(),
                              text: inputText}));
    inputText = "";
    }
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
  }

  .chatbox {
    width: 100%;
    height: 50vh;
    padding: 0 1em;
    text-align: left;
    background-color: #eee;
    overflow-y: scroll;
    overscroll-behavior-y: contain;
    scroll-snap-type: y proximity;
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
    {numUsers > 1 ? numUsers : 'You\'re alone'} {numUsers > 1 ? 'users online' : ':/'}
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
</main>
