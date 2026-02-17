document.addEventListener("DOMContentLoaded", () => {
  const carousel = document.querySelector(".carousel");
  if (!carousel) return;

  const slides = Array.from(carousel.querySelectorAll(".carousel__slide"));
  const prevBtn = carousel.querySelector("#prevBtn");
  const nextBtn = carousel.querySelector("#nextBtn");
  const dotsWrap = carousel.querySelector("#carouselDots");

  if (slides.length === 0 || !prevBtn || !nextBtn || !dotsWrap) {
    console.warn("Carousel missing slides/buttons/dots. Check your HTML IDs/classes.");
    return;
  }

  let currentIndex = 0;

  function showSlide(index) {
    currentIndex = (index + slides.length) % slides.length;

    slides.forEach((slide, i) => {
      slide.classList.toggle("is-active", i === currentIndex);
    });

    const dots = Array.from(dotsWrap.querySelectorAll(".carousel__dot"));
    dots.forEach((dot, i) => {
      dot.classList.toggle("is-active", i === currentIndex);
    });
  }

  // Build dots
  dotsWrap.innerHTML = "";
  slides.forEach((_, i) => {
    const dot = document.createElement("button");
    dot.type = "button";
    dot.className = "carousel__dot";
    dot.addEventListener("click", () => showSlide(i));
    dotsWrap.appendChild(dot);
  });

  prevBtn.addEventListener("click", () => showSlide(currentIndex - 1));
  nextBtn.addEventListener("click", () => showSlide(currentIndex + 1));

  showSlide(0);
});

