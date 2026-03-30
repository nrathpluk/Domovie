import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "AIzaSyD1RQ65WGEWqU_DQVlDYBssVQe22cdbh-0",
    authDomain: "domovie-f1515.firebaseapp.com",
    projectId: "domovie-f1515",
    storageBucket: "domovie-f1515.firebasestorage.app",
    messagingSenderId: "867672595818",
    appId: "1:867672595818:web:84fb27ad49e050f3799913",
    measurementId: "G-HG6YZT6FCR"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { app, auth, db };
