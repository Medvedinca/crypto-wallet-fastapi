document.addEventListener('DOMContentLoaded', () => {

    const images = document.querySelectorAll('.lazy-img');
  
    const imgObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          imgObserver.unobserve(entry.target);  
        }
      }) 
    });
  
    images.forEach(img => {
      imgObserver.observe(img);
    });
  
  });

  function showModal() {
    let modal = document.getElementById('modal');
    modal.style.display = "block";
  }
  
  function closeModal() {
    let modal = document.getElementById('modal');
    modal.style.display = "none";
  }

  const form = document.getElementById('form');

  form.addEventListener('submit', (event) => {
      event.preventDefault();
  
      const formData = new FormData(form);
  
      fetch('/login', {
          method: 'POST',
          body: formData,
      })
  });