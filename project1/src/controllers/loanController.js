const Loan = require("../models/loanModel");
const User = require("../models/userModel");

// Create a loan
exports.createLoan = async (req, res) => {
  try {
    const { userId, loanAmount } = req.body;

    const user = await User.findById(userId);
    if (!user) return res.status(404).json({ error: "User not found" });

    if (loanAmount > user.maxLoanLimit)
      return res.status(400).json({ error: "Loan exceeds max limit" });

    const loan = new Loan({ userId, loanAmount });
    user.loanBalance += loanAmount;
    await user.save();
    await loan.save();

    res.status(201).json({ message: "Loan created successfully", loan });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Update daily repayment
exports.updateRepayment = async (req, res) => {
  try {
    const { userId, dailySales } = req.body;

    const user = await User.findById(userId);
    if (!user) return res.status(404).json({ error: "User not found" });

    const repayment = Math.min(dailySales * 0.1, user.loanBalance);
    user.loanBalance -= repayment;
    await user.save();

    res.status(200).json({ message: "Repayment updated", remainingBalance: user.loanBalance });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
