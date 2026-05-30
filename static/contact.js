// ================= EMAILJS INIT =================
emailjs.init("jtE8FkpgExx-fvRCF");

// CHANGE THESE
const SERVICE_ID = "service_fzvji3j";
const CONTACT_TEMPLATE_ID = "template_feban4a";
const SLOT_TEMPLATE_ID = "template_ye7ulzy";

// ================= CONTACT FORM =================
document.getElementById("contactForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const params = {
    name: contact_name.value,
    email: contact_email.value,
    message: contact_message.value,
  };

  emailjs.send(SERVICE_ID, CONTACT_TEMPLATE_ID, params)
    .then(() => {
      alert("Message sent successfully!");
      this.reset();
    })
    .catch(err => {
      alert("Failed to send message");
      console.error(err);
    });
});

// ================= SLOT FORM =================
document.getElementById("slotForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const params = {
    name: slot_name.value,
    email: slot_email.value,
    date: slot_date.value,
    purpose: slot_purpose.value,
  };

  emailjs.send(SERVICE_ID, SLOT_TEMPLATE_ID, params)
    .then(() => {
      alert("Slot booked successfully!");
      this.reset();
    })
    .catch(err => {
      alert("Failed to book slot");
      console.error(err);
    });
});
