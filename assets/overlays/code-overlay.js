<script>
document.querySelectorAll('.code-overlay').forEach(el => {
  const text = el.textContent;
  el.textContent = '';
  let index = 0;

  function typeStep() {
    el.textContent += text[index];
    index++;
    if(index < text.length) {
      setTimeout(typeStep, 40); // adjust typing speed
    } else {
      setTimeout(() => {
        el.textContent = '';
        index = 0;
        typeStep();
      }, 2000); // pause before looping
    }
  }

  typeStep();
});
</script>
