// static/js/comment_reply.js

/**
 * تنظیم فرم برای حالت ریپلای روی یک کامنت خاص
 * @param {string|number} commentId - آیدی کامنتی که لایک/ریپلای می‌شود
 * @param {string} username - نام کاربری فردی که ریپلای می‌گیرد
 */
function setReply(commentId, username) {
    const parentIdInput = document.getElementById('parent_id');
    const formTitle = document.getElementById('form-title');
    const cancelBtn = document.getElementById('cancel-reply-btn');
    const commentBody = document.getElementById('comment-body');
    const formSection = document.getElementById('comment-form-section');

    if (parentIdInput) parentIdInput.value = commentId;
    if (formTitle) formTitle.innerText = "Reply to @" + username;
    if (cancelBtn) cancelBtn.style.display = "inline-block";
    if (commentBody) commentBody.focus();

    // اسکرول نرم به سمت فرم کامنت
    if (formSection) {
        formSection.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * لغو حالت ریپلای و بازگرداندن فرم به حالت کامنت اصلی
 */
function cancelReply() {
    const parentIdInput = document.getElementById('parent_id');
    const formTitle = document.getElementById('form-title');
    const cancelBtn = document.getElementById('cancel-reply-btn');

    if (parentIdInput) {
        parentIdInput.value = "";
        parentIdInput.setAttribute('value', '');
    }
    if (formTitle) formTitle.innerText = "Your comment";
    if (cancelBtn) cancelBtn.style.display = "none";
}