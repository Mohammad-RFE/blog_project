// static/js/profile_picture_delete.js

document.getElementById('confirm-delete-profile-img-btn')?.addEventListener('click', function () {
    const btn = this;
    const deleteUrl = btn.getAttribute('data-url');

    btn.disabled = true;
    btn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Removing...';

    fetch(deleteUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": DjangoArticleCSRFToken, // استفاده از همان توکن سراسری صفحه
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // ۱. بستن مودال با جاوااسکریپت خالص
            const modalElement = document.getElementById('deleteProfileImgModal');
            if (modalElement) {
                modalElement.classList.remove('show');
                modalElement.style.display = 'none';
                document.querySelector('.modal-backdrop')?.remove();
                document.body.classList.remove('modal-open');
            }

            // ۲. افکت انیمیشن تغییر تصویر به عکس پیش‌فرض و حذف دکمه سطل زباله قرمز
            const imgElement = document.getElementById('user-profile-img');
            const container = document.getElementById('profile-image-container');
            const trashBtn = container?.querySelector('button');

            if (imgElement) {
                imgElement.style.transition = "opacity 0.3s ease";
                imgElement.style.opacity = "0";

                setTimeout(() => {
                    imgElement.src = data.default_url; // قرار دادن عکس پیش‌فرض ارسالی از سرور
                    imgElement.style.opacity = "1";
                    trashBtn?.remove(); // حذف دکمه سطل زباله چون دیگر عکسی نیست
                }, 300);
            }
        } else {
            alert(data.error || "Something went wrong.");
            btn.disabled = false;
            btn.innerText = 'Yes, Remove';
        }
    })
    .catch(error => {
        console.error("Error:", error);
        btn.disabled = false;
        btn.innerText = 'Yes, Remove';
    });
});