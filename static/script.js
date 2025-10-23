console.log("✅ Script cargado correctamente");

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("passengerForm");
  const resultado = document.getElementById("resultado");

  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // evitar recarga

    const data = {
      Name: document.getElementById("name").value,
      Pclass: parseInt(document.getElementById("pclass").value),
      Sex: document.getElementById("sex").value,
      Age: parseFloat(document.getElementById("age").value),
      Fare: parseFloat(document.getElementById("fare").value),
      Weight: parseFloat(document.getElementById("weight").value)
    };

    resultado.innerHTML = "⏳ Cargando predicción...";

    try {
      const res = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await res.json();

      if (res.ok) {
        resultado.innerHTML = result.message;
      } else {
        resultado.innerHTML = "⚠️ Error: " + result.detail;
      }
    } catch (err) {
      console.error("❌ Error en la conexión:", err);
      resultado.innerHTML = "❌ Error de conexión con la API";
    }
  });
});