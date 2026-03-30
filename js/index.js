import { db } from './firebase-config.js';
import { collection, getDocs, query, limit } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

window.addEventListener("load", async () => {
  // --- Animation Fade ---
  document.querySelectorAll(".fade").forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight) {
      el.classList.add("show");
    }
  });

  // --- Fetch Firebase Data ---
  try {
      // 1. ตีไปที่ Collection ชื่อ "movies"
      const moviesRef = collection(db, "movies");
      
      // 2. ดึงข้อมูลมา 1 รายการ
      const q = query(moviesRef, limit(1));
      const querySnapshot = await getDocs(q);

      if (!querySnapshot.empty) {
          const doc = querySnapshot.docs[0];
          const data = doc.data();

          // 3. เอาข้อมูลไปยัดใส่กล่องต่างๆ ใน index.html
          // เช็คชื่อตัวแปร (Field) ที่อยู่ใน Firestore ว่าพิมพ์ไว้ว่าอะไรบ้าง
          if(data.title) {
              document.getElementById("movie-title").innerText = data.title;
          } else if(data.name) {
              document.getElementById("movie-title").innerText = data.name;
          }
          
          if(data.description) {
              document.getElementById("movie-desc").innerText = data.description;
          } else if (data.detail) {
              document.getElementById("movie-desc").innerText = data.detail;
          }
          
          // ถ้ามีการระบุลิงก์รูป (imageUrl หรือ posterUrl) ให้นำมาแทนที่
          if(data.imageUrl) {
              document.getElementById("movie-poster").src = data.imageUrl;
          } else if(data.posterUrl) {
              document.getElementById("movie-poster").src = data.posterUrl;
          }
          
      } else {
          // ไม่พบเอกสารใดๆ เลยใน Collection "movies"
          console.warn("ไม่พบรายการภาพยนตร์ในระบบ Firebase Firestore เลย");
          document.getElementById("movie-title").innerText = "Inception (หาข้อมูลไม่เจอ)";
          document.getElementById("movie-desc").innerText = "โปรดเข้าไปใน Firebase เลือก Firestore Database => สร้าง Collection ชื่อ 'movies' แล้วตั้งค่า Field: title และ description ให้ครบถ้วนเพื่อให้หน้านี้มีข้อมูล";
      }
  } catch (error) {
      console.error("ดึงข้อมูล Firebase ผิดพลาด: ", error);
      document.getElementById("movie-title").innerText = "ข้อผิดพลาดระบบการเชื่อมต่อ";
      document.getElementById("movie-desc").innerText = error.message;
  }
});
