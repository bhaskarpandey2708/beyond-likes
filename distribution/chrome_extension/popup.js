fetch("http://localhost:8888/v1/health")
  .then(res => res.json())
  .then(data => {
    const el = document.getElementById("ext-status");
    if (data.status === "HEALTHY") {
      el.innerText = "Online :8888";
      el.style.color = "#3fb950";
    }
  })
  .catch(() => {
    const el = document.getElementById("ext-status");
    el.innerText = "Offline";
    el.style.color = "#f85149";
    el.style.borderColor = "rgba(248,81,73,0.3)";
  });
