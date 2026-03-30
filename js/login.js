import { auth } from './firebase-config.js';
import { signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";

document.addEventListener("DOMContentLoaded", () => {
    // ใส่เอฟเฟกต์เฟด
    document.querySelectorAll(".fade").forEach(el => {
        el.classList.add("show");
    });

    const loginForm = document.getElementById("loginForm");
    const emailInput = document.getElementById("emailInput");
    const passwordInput = document.getElementById("passwordInput");
    const errorMessage = document.getElementById("errorMessage");

    loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        
        const email = emailInput.value;
        const password = passwordInput.value;
        
        signInWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                // เข้าสู่ระบบสำเร็จ
                const user = userCredential.user;
                console.log("เข้าสู่ระบบเรียบร้อย", user);
                // นำไปสู่หน้าหลัก
                window.location.href = "main.html";
            })
            .catch((error) => {
                // เกิดข้อผิดพลาด
                const errorCode = error.code;
                const errorMessageTxt = error.message;
                
                // แปลงข้อผิดพลาดเป็นภาษาไทยให้เข้าใจง่าย
                if(errorCode === 'auth/invalid-credential' || errorCode === 'auth/user-not-found' || errorCode === 'auth/wrong-password') {
                    errorMessage.textContent = "อีเมลหรือรหัสผ่านไม่ถูกต้อง";
                } else if(errorCode === 'auth/invalid-email') {
                    errorMessage.textContent = "รูปแบบอีเมลไม่ถูกต้อง";
                } else {
                    errorMessage.textContent = "เกิดข้อผิดพลาด: " + errorMessageTxt;
                }
                
                errorMessage.style.display = "block";
            });
    });
});
