function sendApplication(event) {

    event.preventDefault();

    const form = document.getElementById("applyForm");

    const params = {
        name: document.querySelector('input[name="name"]').value,
        email: document.querySelector('input[name="email"]').value,
        phone: document.querySelector('input[name="phone"]').value,
        college: document.querySelector('input[name="college"]').value,
        department: document.querySelector('input[name="department"]').value,
        year: document.querySelector('select[name="year"]').value
    };

    emailjs.send(
        "service_ccfe2ik",
        "template_ltnws5i",
        params
    )
    .then(function(response) {

        console.log("Email sent successfully");

        // Submit form to Flask
        form.removeAttribute("onsubmit");
        form.submit();

    })
    .catch(function(error) {

        console.error("EmailJS Error:", error);

        // Still save application even if email fails
        form.removeAttribute("onsubmit");
        form.submit();

    });
}