(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });
    
    
    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const $dropdownToggle = $(".dropdown-toggle");
    const $dropdownMenu = $(".dropdown-menu");
    const showClass = "show";
    
    $(window).on("load resize", function() {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
            function() {
                const $this = $(this);
                $this.addClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "true");
                $this.find($dropdownMenu).addClass(showClass);
            },
            function() {
                const $this = $(this);
                $this.removeClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "false");
                $this.find($dropdownMenu).removeClass(showClass);
            }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Modal Video
    $(document).ready(function () {
        var $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });
        console.log($videoSrc);

        $('#videoModal').on('shown.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })

        $('#videoModal').on('hide.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc);
        })
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        margin: 24,
        dots: true,
        loop: true,
        nav : false,
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });
    
})(jQuery);

document.addEventListener('DOMContentLoaded', function () {
    var tableModal = document.getElementById('tableModal');
    var modalBodyContent = document.getElementById('modalBodyContent');

    tableModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // Button that triggered the modal
        var table_number = button.getAttribute('data-table-number'); // Extract info from data-* attributes
        
        fetch(`/counter/api/get_table_receipt/${table_number}/`)
            // .then(response => response.json())
            .then(response => {
                console.log('Response status:', response.status); // Log status
                return response.json();
            })
            .then(data => {
                console.log('Data received:', data);
                if (data.error) {
                    modalBodyContent.innerHTML = `<p>${data.error}</p>`;
                } else {
                    const now = new Date();
                    const currentDate = now.toLocaleDateString('en-US', { 
                        year: 'numeric', month: 'long', day: 'numeric' 
                    });
                    var receiptHTML = `
                        <div class="receipt-header">
                            <h1>Restaurant Name</h1>
                            <p>1234 Restaurant St, Food City</p>
                            <p>Phone: (123) 456-7890</p>
                        </div>
                        <div class="customer-info">
                            
                            <p><strong>Table No:</strong> ${table_number}</p>
                            <p><strong>Date:</strong> ${currentDate}</p>
                        </div>
                        <table class="order-table">
                            <thead>
                                <tr>
                                    <th>Item</th>
                                    <th>Qty</th>
                                    <th>Price</th>
                                    <th>Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.items.map(item => `
                                    <tr>
                                        <td>${item.item}</td>
                                        <td>${item.qty}</td>
                                        <td>${item.price}</td>
                                        <td>${item.total}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                        <div class="total-section">
                            <p><strong>Subtotal:</strong> ${data.subtotal}</p>
                            <p><strong>Tax (8%):</strong> ${data.tax}</p>
                            <p><strong>Total:</strong> ${data.total}</p>
                        </div>
                        <div class="receipt-footer">
                            <p>Thank you for dining with us!</p>
                            <p>Visit Again!</p>
                        </div>
                    `;
                    modalBodyContent.innerHTML = receiptHTML;
                }
            })
            .catch(error => {
                console.error('Error fetching receipt data:', error);
            });
    });
});
