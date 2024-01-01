function sendMail(){
    let parms ={
        name : document.getelementById("name").value,
        email : document.getelementById("email").value,
        subject : document.getelementById("subject").value,
        message : document.getelementById("message").value,
    }

    emailjs.send("service_5wr48mf","template_ghrb405",parms).then(alert("Email sent!"))
}