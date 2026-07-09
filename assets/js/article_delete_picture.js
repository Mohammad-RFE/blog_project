// static/js/article_delete_picture.js

document.addEventListener("DOMContentLoaded", function () {

    const fileInput = document.getElementById('id_cover');
    const currentImageBox = document.getElementById('current-image-box');
    const uploadFileBox = document.getElementById('upload-file-box');
    const cancelBtn = document.getElementById('cancel-change-image-btn');

    // ترفند لمس/کلیک روی فضای متنی باکس آپلود
    document.getElementById('dropzone-clickable-area')?.addEventListener('click', function() {
        fileInput?.click();
    });

    // ۱. تایید حذف آژاکسی عکس از داخل مودال (بدون جی‌کوئری)
    document.getElementById('confirm-delete-img-btn')?.addEventListener('click', function () {
        const btn = this;
        const deleteCoverUrl = btn.getAttribute('data-url');

        if (!deleteCoverUrl || deleteCoverUrl.includes('/0/')) return;

        btn.disabled = true;
        btn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Deleting...';

        fetch(deleteCoverUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": DjangoCoverCSRFToken,
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // بستن مودال با جاوااسکریپت خالص
                const modalElement = document.getElementById('deleteImageModal');
                if (modalElement) {
                    $(modalElement).modal('hide'); // بستن مودال طبق ساختار بوت‌استرپ
                }

                cancelBtn?.classList.add('d-none');

                // انیمیشن محو شدن عکس و ظاهر شدن باکس با CSS خالص
                if (currentImageBox) {
                    currentImageBox.style.transition = "opacity 0.3s ease";
                    currentImageBox.style.opacity = "0";

                    setTimeout(() => {
                        currentImageBox.remove();
                        if (uploadFileBox) {
                            uploadFileBox.classList.remove('d-none');
                            uploadFileBox.style.opacity = "0";
                            uploadFileBox.style.transition = "opacity 0.3s ease";
                            setTimeout(() => { uploadFileBox.style.opacity = "1"; }, 50);
                        }
                    }, 300);
                }
            } else {
                alert(data.error || "Something went wrong.");
                btn.disabled = false;
                btn.innerHTML = 'Yes, Delete';
            }
        })
        .catch(error => {
            console.error("Error:", error);
            btn.disabled = false;
            btn.innerHTML = 'Yes, Delete';
        });
    });

    // ۲. مدیریت دکمه Change Image (سازگار با تاچ موبایل)
    document.getElementById('change-image-trigger-btn')?.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        if (currentImageBox && uploadFileBox) {
            currentImageBox.classList.add('d-none');
            uploadFileBox.classList.remove('d-none');
            cancelBtn?.classList.remove('d-none');
        }
    });

    // ۳. مانیتور کردن انتخاب فایل
    fileInput?.addEventListener('change', function () {
        const fileNameSlot = document.getElementById('chosen-file-name');
        if (fileNameSlot) {
            const fileName = this.files[0] ? this.files[0].name : "";
            fileNameSlot.innerText = fileName ? "Selected File: " + fileName : "";
        }
    });

    // ۴. مدیریت دکمه لغو تغییر عکس (سازگار با تاچ موبایل)
    cancelBtn?.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        const fileNameSlot = document.getElementById('chosen-file-name');

        if (currentImageBox && uploadFileBox) {
            if (fileInput) fileInput.value = "";
            if (fileNameSlot) fileNameSlot.innerText = "";

            uploadFileBox.classList.add('d-none');
            currentImageBox.classList.remove('d-none');
            this.classList.add('d-none');
        }
    });

});