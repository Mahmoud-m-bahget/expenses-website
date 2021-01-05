const usernameField=document.querySelector('#usernameField');
const feedbackArea=document.querySelector('.invalid-feedback');
const emailField=document.querySelector('#emailField');
const EmailfeedbackArea=document.querySelector('.EmailfeedbackArea');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput')
const passowrdField = document.querySelector('#passwordField')
const submitBtn = document.querySelector('.submit-btn')
showpasswordToggle=document.querySelector('.showpasswordToggle')


const hendelToggleInput=(e)=>{
    if(showpasswordToggle.textContent==="SHOW"){
        showpasswordToggle.textContent='HIDE';
        passowrdField.setAttribute("type",'text');

    }else{
        showpasswordToggle.textContent='SHOW';
        passowrdField.setAttribute("type",'password')


    }

}
showpasswordToggle.addEventListener('click',hendelToggleInput)

emailField.addEventListener('keyup',(e)=>{
    const emailval = e.target.value;
    console.log(emailval)
    emailField.classList.remove("is-invalid");
EmailfeedbackArea.style.display = "none";

feedbackArea.innerHTML=emailval;
emailField.classList.remove("is-valid");



if (emailval.length > 0) {
        fetch("/authentication/validate-email",{
            body: JSON.stringify({email:emailval}),
            method: "POST",
        })
        .then((res)=>res.json())
        .then((data)=>{
            if (data.email_error){
                submitBtn.disabled = true
                emailField.classList.add("is-invalid");
                EmailfeedbackArea.style.display = "block";
                EmailfeedbackArea.style.color = "red";

                EmailfeedbackArea.innerHTML=`<p>${data.email_error}</p>`;
            }else{
                emailField.classList.add("is-valid");
                submitBtn.removeAttribute('disabled')

            }
        });
    };
});





usernameField.addEventListener('keyup',(e)=>{
    const usernameVal = e.target.value;
    usernameSuccessOutput.style.display = 'block'
    if (usernameVal <=0){
        usernameSuccessOutput.style.display = 'none'

    }

    usernameSuccessOutput.textContent=`checking ${usernameVal}`
    
usernameField.classList.remove("is-invalid");
feedbackArea.style.display = "none";

usernameField.classList.remove("is-valid");


    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username",{
            body: JSON.stringify({username:usernameVal}),
            method: "POST",
        })
        .then((res)=>res.json())
        .then((data)=>{
            usernameSuccessOutput.style.display = 'none'
            if (data.username_error){
                submitBtn.disabled = true
                usernameField.classList.add("is-invalid");
                feedbackArea.style.display = "block";
                feedbackArea.style.color = "red";

                feedbackArea.innerHTML=`<p>${data.username_error}</p>`;
            }else{
                usernameField.classList.add("is-valid");
                submitBtn.removeAttribute('disabled')

            }
        });
    };
});

