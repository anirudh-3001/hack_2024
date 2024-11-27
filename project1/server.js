const express = require("express");
const app = express();
const port = 5000;

// Middleware to parse JSON bodies
app.use(express.json());

// Sample route
app.get("/", (req, res) => {
  res.send("Hello, Blockchain Micro-Loan Platform!");
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

