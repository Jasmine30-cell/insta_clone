function login() {
    const username = document.querySelector('input[type="text"]').value;
    const password = document.querySelector('input[type="password"]').value;
  
    if (username && password) {
      alert(`Logged in as ${username}`);
    } else {
      alert("Please enter both username and password.");
    }
  }
  