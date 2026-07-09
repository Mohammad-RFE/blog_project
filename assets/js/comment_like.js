// static/js/comment_like.js

// ۱. به محض لود شدن کل صفحه، وضعیت قلب‌هایی که از قبل لایک شده‌اند را مشخص می‌کنیم
document.addEventListener("DOMContentLoaded", function() {
    // خواندن لیست آیدی‌ها از متغیری که در HTML تعریف خواهیم کرد
    const userLikedComments = window.DjangoUserLikedComments || [];

    document.querySelectorAll('.like-comment-btn').forEach(btn => {
        const commentId = parseInt(btn.getAttribute('data-comment-id'));
        if (userLikedComments.includes(commentId)) {
            const icon = btn.querySelector('i');
            icon.classList.remove('fa-heart-o');
            icon.classList.add('fa-heart');
            btn.style.color = "#e74c3c";
        }
    });
});

// ۲. پردازش کلیک روی دکمه‌های لایک به صورت آژاکس
document.addEventListener('click', function(event) {
    const btn = event.target.closest('.like-comment-btn');
    if (!btn) return;

    // بررسی وضعیت لاگین از روی متغیر گلوبال HTML
    if (window.DjangoUserIsAuthenticated === "False") {
        alert("Please log in to like comments!");
        return;
    }

    const url = btn.getAttribute('data-url');
    const icon = btn.querySelector('i');
    const countSpan = btn.querySelector('.like-count');

    btn.style.pointerEvents = "none";

    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": window.DjangoCommentCSRFToken, // خواندن توکن از HTML
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            countSpan.innerText = data.total_likes;

            if (data.liked) {
                icon.classList.remove('fa-heart-o');
                icon.classList.add('fa-heart');
                btn.style.color = "#e74c3c";
            } else {
                icon.classList.remove('fa-heart');
                icon.classList.add('fa-heart-o');
                btn.style.color = "#aaa";
            }
        }
        btn.style.pointerEvents = "auto";
    })
    .catch(error => {
        console.error("Error:", error);
        btn.style.pointerEvents = "auto";
    });
});