import { auth } from './firebase-config.js';
import { createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";

window.addEventListener("load", () => {
  document.querySelectorAll(".fade").forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight) {
      el.classList.add("show");
    }
  });

  const registForm = document.getElementById("registForm");
  const emailInput = document.getElementById("emailInput");
  const passwordInput = document.getElementById("passwordInput");
  const confirmPasswordInput = document.getElementById("confirmPasswordInput");
  const errorMessage = document.getElementById("errorMessage");

  if(registForm) {
      registForm.addEventListener("submit", (e) => {
          e.preventDefault();
          
          const email = emailInput.value;
          const password = passwordInput.value;
          const confirmPassword = confirmPasswordInput.value;
          
          if(password !== confirmPassword) {
              errorMessage.textContent = "รหัสผ่านไม่ตรงกัน";
              errorMessage.style.display = "block";
              return;
          }
          
          if(password.length < 6) {
              errorMessage.textContent = "รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร";
              errorMessage.style.display = "block";
              return;
          }

          createUserWithEmailAndPassword(auth, email, password)
              .then((userCredential) => {
                  // สมัครสมาชิกสำเร็จ
                  const user = userCredential.user;
                  console.log("สมัครสมาชิกเรียบร้อย", user);
                  // เมื่อสมัครเสร็จให้ไปหน้าล็อคอิน
                  window.location.href = "login.html";
              })
              .catch((error) => {
                  const errorCode = error.code;
                  const errorMessageTxt = error.message;
                  
                  if(errorCode === 'auth/email-already-in-use') {
                      errorMessage.textContent = "อีเมลนี้มีผู้ใช้งานแล้ว";
                  } else if(errorCode === 'auth/invalid-email') {
                      errorMessage.textContent = "รูปแบบอีเมลไม่ถูกต้อง";
                  } else {
                      errorMessage.textContent = "เกิดข้อผิดพลาด: " + errorMessageTxt;
                  }
                  
                  errorMessage.style.display = "block";
              });
      });
  }
});
