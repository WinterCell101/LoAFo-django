<script>
    tailwind.config = {
        darkMode: 'class', // This tells the CDN to look for the 'dark' class
        theme: {
            extend: {
                // You can also put your custom rounding here!
                borderRadius: {
                    'card': '2.5rem',
                },
                boxShadow: {
                    'glow' : '0 0 20px 5px rgba(0, 102, 255, 0.6)'
                }
            }
        }
    }

    // Check for saved theme or system preference before the page even renders
    if (localStorage.getItem('theme') === 'dark' ||
        (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
    if (localStorage.getItem('theme') === 'dark' ||
        (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
</script>