document.querySelectorAll("[data-character-counter]").forEach((field) => {
  const counter = document.getElementById(field.dataset.characterCounter);
  const update = () => {
    counter.textContent = `${field.value.length}/${field.maxLength}`;
  };
  field.addEventListener("input", update);
  update();
});

document.querySelectorAll("[data-busy-form]").forEach((form) => {
  form.addEventListener("submit", () => {
    if (!form.checkValidity()) return;
    const button = form.querySelector('button[type="submit"]');
    const status = form.querySelector(".submit-status");
    button.disabled = true;
    button.dataset.originalText = button.textContent;
    button.textContent = "Обрабатываем…";
    if (status) status.textContent = "Запрос отправлен. Пожалуйста, подождите.";
  });
});

const imageInput = document.querySelector("[data-image-input]");
const imagePreview = document.querySelector("[data-image-preview]");
if (imageInput && imagePreview) {
  imageInput.addEventListener("change", () => {
    const [file] = imageInput.files;
    if (!file) {
      imagePreview.hidden = true;
      return;
    }
    const image = imagePreview.querySelector("img");
    image.src = URL.createObjectURL(file);
    image.onload = () => URL.revokeObjectURL(image.src);
    imagePreview.hidden = false;
  });
}

