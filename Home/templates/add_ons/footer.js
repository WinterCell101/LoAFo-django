<script>
    document.addEventListener('DOMContentLoaded', function() {
        const yearSpan = document.getElementById('current-year');
        if (yearSpan) yearSpan.textContent = new Date().getFullYear();

        // Cursor glow on footer hover
        document.addEventListener('mousemove', (e) => {
            const footer = document.querySelector('footer');
            const glow = document.getElementById('footer-glow');
            if (footer && glow) {
                const rect = footer.getBoundingClientRect();
                glow.style.setProperty('--x', `${e.clientX - rect.left}px`);
                glow.style.setProperty('--y', `${e.clientY - rect.top}px`);
            }
        });
    });
</script>
