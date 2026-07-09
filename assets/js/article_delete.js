// static/js/article_delete.js

let articleIdToDelete = null;
let deleteArticleUrl = null;

// ۱. گوش دادن به کلیک سطل زباله با جاوااسکریپت خالص (بدون $)
document.addEventListener('click', function(event) {
    // پیدا کردن دکمه‌ای که کلیک شده (یا آیکون داخل آن)
    const btn = event.target.closest('.open-delete-modal-btn');

    if (btn) {
        articleIdToDelete = btn.getAttribute('data-article-id');
        deleteArticleUrl = btn.getAttribute('data-url');
        console.log("🟢 کلیک روی سطل زباله | آدرس حذف:", deleteArticleUrl);
    }
});

// ۲. پردازش نهایی حذف با زدن دکمه تایید داخل مودال
document.getElementById('confirm-delete-article-btn')?.addEventListener('click', function() {
    console.log("🟡 دکمه Yes, Delete داخل مودال کلیک شد.");

    if (!articleIdToDelete || !deleteArticleUrl) {
        console.error("🔴 خطا: اطلاعات مقاله یافت نشد!");
        return;
    }

    const btn = this;
    btn.disabled = true;
    btn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Deleting...';

    fetch(deleteArticleUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": DjangoArticleCSRFToken,
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("🟢 حذف در بک‌آند موفق بود.");

            // بستن مودال با جاوااسکریپت خالص و حذف لایه تاریک پشت آن
            const modalElement = document.getElementById('deleteArticleModal');
            if (modalElement) {
                modalElement.classList.remove('show');
                modalElement.style.display = 'none';
                document.querySelector('.modal-backdrop')?.remove();
                document.body.classList.remove('modal-open');
                document.body.style.removeProperty('padding-right');
            }

            // افکت انیمیشن محو شدن کارت با جاوااسکریپت خالص (CSS Transition)
            const card = document.getElementById(`article-card-${articleIdToDelete}`);
            if (card) {
                card.style.transition = "opacity 0.4s ease";
                card.style.opacity = "0";

                setTimeout(() => {
                    card.remove();
                    console.log("🟢 کارت مقاله از DOM حذف شد.");

                    // اگر مقاله‌ای نمانده بود صفحه را رفرش کن
                    if (document.querySelectorAll('.article-row-box').length === 0) {
                        location.reload();
                    }
                }, 400);
            }
        } else {
            alert(data.error || "Something went wrong.");
            btn.disabled = false;
            btn.innerText = 'Yes, Delete';
        }
    })
    .catch(error => {
        console.error("🔴 خطا در ارتباط با سرور:", error);
        btn.disabled = false;
        btn.innerText = 'Yes, Delete';
    });
});