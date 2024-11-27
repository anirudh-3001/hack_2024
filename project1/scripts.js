document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("credit-form");
    const scoreElement = document.getElementById("score");
    const resultSection = document.getElementById("result");
  
    form.addEventListener("submit", (e) => {
      e.preventDefault();
  
      const utility = parseFloat(document.getElementById("utility").value) || 0;
      const financial = parseFloat(document.getElementById("financial").value) || 0;
      const trust = parseFloat(document.getElementById("trust").value) || 0;
  
      const creditScore = Math.round(
        utility * 0.4 + financial * 10 * 0.35 + trust * 10 * 0.25
      );
  
      scoreElement.textContent = creditScore;
      resultSection.classList.remove("hidden");
    });
  });
  