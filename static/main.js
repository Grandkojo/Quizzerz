let isFirstLoad = true; // Flag to check if it's the first load

    function toggleNav() {
        var sidebar = document.getElementById("mySidebar");
        if (sidebar.style.left === "0px") {
            sidebar.style.left = "-200px";
        } else {
            sidebar.style.left = "0px";
        }
    }

    function adjustSidebar() {
        var sidebar = document.getElementById("mySidebar");
        if (window.innerWidth > 768) {
            sidebar.style.left = "0";
            document.getElementById("main").style.marginLeft = "200px";
        } else {
            sidebar.style.left = "-200px";
            document.getElementById("main").style.marginLeft = "0";
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        const activeUrl = sessionStorage.getItem('activeUrl');
        if (activeUrl) {
            loadContentByUrl(activeUrl);
            setActiveLink(activeUrl);
        } else {
            if (isFirstLoad) {
                var dashboardLink = document.querySelector('.nav-link[data-url="{{ url_for('admin_bp.dashboard') }}"]');
                if (dashboardLink) {
                    dashboardLink.click();
                }
                isFirstLoad = false;
            }
        }
    });

    function loadContent(element) {
        const url = element.getAttribute('data-url');
        sessionStorage.setItem('activeUrl', url);

        setActiveLink(url);
        loadContentByUrl(url);
    }

    function setActiveLink(url) {
        document.querySelectorAll('.nav-item a').forEach(function(item) {
            item.classList.remove('active', 'text-primary');
            if (item.getAttribute('data-url') === url) {
                item.classList.add('active', 'text-primary');
            }
        });
    }

    function loadContentByUrl(url) {
        fetch(url)
            .then(response => response.text())
            .then(data => {
                document.getElementById('content').innerHTML = data;
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    window.addEventListener('resize', adjustSidebar);

    adjustSidebar();
    
    function clickMe(){
        alert("I'm clicked");
        console.log("I'm clicked")
    }