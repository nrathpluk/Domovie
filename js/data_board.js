import { auth, db } from './firebase-config.js';
import { collection, addDoc, onSnapshot, query, orderBy, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";
import { onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";

document.addEventListener("DOMContentLoaded", () => {
    const authLink = document.getElementById("authLink");
    const reviewFormSection = document.getElementById("reviewFormSection");
    const loginPrompt = document.getElementById("loginPrompt");
    const reviewForm = document.getElementById("reviewForm");
    const reviewsContainer = document.getElementById("reviewsContainer");
    const postMessage = document.getElementById("postMessage");
    
    let currentUser = null;

    // 1. Check Auth State
    onAuthStateChanged(auth, (user) => {
        if (user) {
            currentUser = user;
            // ตั้งค่า Navbar เป็น ออกจากระบบ
            authLink.innerHTML = `<a href="#" id="logoutBtn" style="color: #ff6b6b;">ออกจากระบบ (${user.email})</a>`;
            document.getElementById("logoutBtn").addEventListener("click", (e) => {
                e.preventDefault();
                signOut(auth).then(() => {
                    window.location.reload();
                });
            });

            // แสดงฟอร์มซ่อนการเตือน
            reviewFormSection.style.display = "block";
            loginPrompt.style.display = "none";
        } else {
            currentUser = null;
            authLink.innerHTML = `<a href="login.html">เข้าสู่ระบบ</a>`;
            reviewFormSection.style.display = "none";
            loginPrompt.style.display = "block";
        }
    });

    // 2. Load Reviews from Firestore (Realtime)
    const reviewsRef = collection(db, "reviews");
    const q = query(reviewsRef, orderBy("createdAt", "desc"));

    onSnapshot(q, (snapshot) => {
        reviewsContainer.innerHTML = "";
        
        if(snapshot.empty) {
            reviewsContainer.innerHTML = "<p style='color: #888; text-align: center; width: 100%;'>ยังไม่มีรีวิวในขณะนี้ เป็นคนแรกที่รีวิวสิ!</p>";
            return;
        }

        snapshot.forEach((doc) => {
            const data = doc.data();
            const dateStr = data.createdAt ? new Date(data.createdAt.toDate()).toLocaleDateString('th-TH') : "เมื่อสักครู่";
            
            const reviewHtml = `
                <div class="review-card">
                    <div class="review-header">
                        <div class="movie-title">${data.movieTitle}</div>
                        <div class="reviewer-name">${dateStr}</div>
                    </div>
                    <div class="review-text">
                        ${data.content}
                    </div>
                    <div style="margin-top: 15px; font-size: 12px; color: #f5c76a;">
                        โดย: ${data.authorEmail}
                    </div>
                </div>
            `;
            reviewsContainer.innerHTML += reviewHtml;
        });
    }, (error) => {
        console.error("Error loading reviews: ", error);
        reviewsContainer.innerHTML = `<p style="color: #ff6b6b; text-align: center; width: 100%;">ไม่สามารถโหลดข้อมูลได้ (อาจจะยังไม่ได้ตั้งค่า Firebase) ${error.message}</p>`;
    });

    // 3. Handle Form Submit (Save to Firestore)
    reviewForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        if(!currentUser) return;

        const movieTitle = document.getElementById("movieTitle").value;
        const reviewContent = document.getElementById("reviewContent").value;
        const submitBtn = reviewForm.querySelector("button");
        
        submitBtn.disabled = true;
        submitBtn.textContent = "กำลังโพสต์...";

        try {
            await addDoc(collection(db, "reviews"), {
                movieTitle: movieTitle,
                content: reviewContent,
                authorUid: currentUser.uid,
                authorEmail: currentUser.email,
                createdAt: serverTimestamp()
            });

            // Reset form
            reviewForm.reset();
            postMessage.textContent = "โพสต์รีวิวสำเร็จ!";
            postMessage.style.display = "block";
            postMessage.style.color = "#4CAF50";
            
            setTimeout(() => {
                postMessage.style.display = "none";
            }, 3000);
            
        } catch (error) {
            console.error("Error adding document: ", error);
            postMessage.textContent = "เกิดข้อผิดพลาด: " + error.message;
            postMessage.style.display = "block";
            postMessage.style.color = "#ff6b6b";
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "โพสต์รีวิว";
        }
    });
});
