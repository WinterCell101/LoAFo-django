<script>
    document.addEventListener('DOMContentLoaded', function() {
        // 1. Set the current year
        const yearSpan = document.getElementById('current-year');
        if (yearSpan) {
            yearSpan.textContent = new Date().getFullYear();
        }

        // 2. Glow Cursor Logic (Only triggers on hover)
        document.addEventListener('mousemove', (e) => {
            const footer = document.querySelector('footer');
            const glow = document.getElementById('footer-glow');

            if (footer && glow) {
                const rect = footer.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                glow.style.setProperty('--x', `${x}px`);
                glow.style.setProperty('--y', `${y}px`);
            }
        });
    });
</script>