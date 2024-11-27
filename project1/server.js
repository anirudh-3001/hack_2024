const express = require("express");
const connectDB = require("./config/db");

const app = express();
const port = process.env.PORT || 5000;

// Connect to MongoDB
connectDB();

// Middleware to parse JSON bodies
app.use(express.json());

// Import Routes
const userRoutes = require("./src/routes/userRoutes");
const loanRoutes = require("./src/routes/loanRoutes");

// Use Routes
app.use("/api/users", userRoutes);
app.use("/api/loans", loanRoutes);

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
