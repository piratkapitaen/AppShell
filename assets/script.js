(function () {
  const script = document.createElement("script");
  script.src = "https://www.paypal.com/sdk/js?client-id=BAAWAOqAD6m4SPWNLVO65C9HPuMESSl1wBkoZpRkKj3xqbN_yGRrgFF9r6P7XC1LfhINJdcslYu2djh3FE&components=hosted-buttons&disable-funding=venmo&currency=EUR";
  script.crossOrigin = "anonymous";
  script.async = true;

  script.onload = function () {
    // Sobald das SDK geladen ist, rendere den Button
    if (paypal && paypal.HostedButtons) {
      paypal.HostedButtons({
        hostedButtonId: "M8R5865HUP2VE", // Deine echte PayPal Button-ID
        onApprove: function () {
          // Aktuellen Zeitstempel speichern
          const now = new Date().toISOString();
          localStorage.setItem("paid_at", now);
          console.log("✅ Payment successful, saved:", now);

          // Seite neu laden (optional)
          location.reload();
        },
      }).render("#paypal-container-M8R5865HUP2VE");
    }
  };

  document.head.appendChild(script);
  
  
})();



function renderPayPalButton() {
  if (!document.querySelector("#paypal-container-M8R5")) return;
  if (document.querySelector("#paypal-container-M8R5").hasChildNodes()) return;

  if (window.paypal && paypal.HostedButtons) {
    paypal.HostedButtons({
      hostedButtonId: "M8R5",
    }).render("#paypal-container-M8R5");
  }
}

// Beobachte Änderungen im DOM
const observer = new MutationObserver(() => {
  renderPayPalButton();
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
});

// Falls initial vorhanden
document.addEventListener("DOMContentLoaded", renderPayPalButton);
